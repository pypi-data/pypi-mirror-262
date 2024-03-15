from __future__ import annotations

import pickle
from copy import copy
from typing import Optional, Literal

import mosaik  # type: ignore
import mosaik_api_v3  # type: ignore

from vessim.actor import Actor
from vessim.controller import Controller
from vessim.storage import Storage, StoragePolicy, DefaultStoragePolicy
from vessim.util import Clock


class Microgrid:
    def __init__(
        self,
        world: mosaik.World,
        clock: Clock,
        actors: list[Actor],
        controllers: list[Controller],
        storage: Optional[Storage] = None,
        storage_policy: Optional[StoragePolicy] = None,
        step_size: int = 1,  # global default
    ):
        self.actors = actors if actors is not None else []
        self.controllers = controllers if controllers is not None else []
        self.storage = storage
        self.storage_policy = storage_policy
        self.step_size = step_size

        actor_names_and_entities = []
        for actor in actors:
            actor_step_size = actor.step_size if actor.step_size else step_size
            actor_sim = world.start("Actor", clock=clock, step_size=actor_step_size)
            # We initialize all actors before the grid simulation to make sure that
            # there is already a valid p_delta at step 0
            actor_entity = actor_sim.Actor(actor=actor)
            actor_names_and_entities.append((actor.name, actor_entity))

        grid_sim = world.start("Grid", step_size=step_size)
        grid_entity = grid_sim.Grid(storage=storage, policy=storage_policy)
        for actor_name, actor_entity in actor_names_and_entities:
            world.connect(actor_entity, grid_entity, "p")

        for controller in controllers:
            controller.start(self, clock)
            controller_step_size = controller.step_size if controller.step_size else step_size
            controller_sim = world.start("Controller", step_size=controller_step_size)
            controller_entity = controller_sim.Controller(controller=controller)
            world.connect(grid_entity, controller_entity, "p_delta")
            for actor_name, actor_entity in actor_names_and_entities:
                world.connect(
                    actor_entity, controller_entity, ("state", f"actor.{actor_name}")
                )

    def pickle(self) -> bytes:
        """Returns a Dict with the current state of the microgrid for monitoring."""
        cp = copy(self)
        cp.controllers = []  # controllers are not needed and often not pickleable
        return pickle.dumps(cp)

    def finalize(self):
        """Clean up in case the simulation was interrupted.

        Mosaik already has a cleanup functionality but this is an additional safety net
        in case the user interrupts the simulation before entering the mosiak event loop.
        """
        for controller in self.controllers:
            controller.finalize()


class Environment:
    COSIM_CONFIG = {
        "Actor": {
            "python": "vessim.actor:_ActorSim",
        },
        "Controller": {
            "python": "vessim.controller:_ControllerSim",
        },
        "Grid": {"python": "vessim.cosim:_GridSim"},
    }

    def __init__(self, sim_start):
        self.clock = Clock(sim_start)
        self.microgrids = []
        self.world = mosaik.World(self.COSIM_CONFIG)  # type: ignore

    def add_microgrid(
        self,
        actors: Optional[list[Actor]] = None,
        controllers: Optional[list[Controller]] = None,
        storage: Optional[Storage] = None,
        storage_policy: Optional[StoragePolicy] = None,
        step_size: int = 1,  # global default
    ):
        microgrid = Microgrid(
            self.world,
            self.clock,
            actors if actors is not None else [],
            controllers if controllers is not None else [],
            storage,
            storage_policy,
            step_size
        )
        self.microgrids.append(microgrid)
        return microgrid

    def run(
        self,
        until: Optional[int] = None,
        rt_factor: Optional[float] = None,
        print_progress: bool | Literal["individual"] = True,
    ):
        if until is None:
            # there is no integer representing infinity in python
            until = float("inf") # type: ignore
        try:
            self.world.run(
                until=until, rt_factor=rt_factor, print_progress=print_progress
            )
        except Exception as e:
            if str(e).startswith("Simulation too slow for real-time factor"):
                return
            for microgrid in self.microgrids:
                microgrid.finalize()
            raise


class _GridSim(mosaik_api_v3.Simulator):
    META = {
        "type": "time-based",
        "models": {
            "Grid": {
                "public": True,
                "params": ["storage", "policy"],
                "attrs": ["p", "p_delta"],
            },
        },
    }

    def __init__(self):
        super().__init__(self.META)
        self.eid = "Grid"
        self.step_size = None
        self.storage = None
        self.policy = None
        self.p_delta = 0.0
        self._last_step_time = 0

    def init(self, sid, time_resolution=1.0, **sim_params):
        self.step_size = sim_params["step_size"]
        return self.meta

    def create(self, num, model, **model_params):
        assert num == 1, "Only one instance per simulation is supported"
        self.storage = model_params["storage"]
        self.policy = model_params["policy"]
        if self.policy is None:
            self.policy = DefaultStoragePolicy()
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        p_delta = sum(inputs[self.eid]["p"].values())
        if self.storage is None:
            self.p_delta = p_delta
        else:
            assert self.policy is not None
            self.p_delta = self.policy.apply(self.storage, p_delta, self.step_size)
        return time + self.step_size

    def get_data(self, outputs):
        return {self.eid: {"p_delta": self.p_delta}}

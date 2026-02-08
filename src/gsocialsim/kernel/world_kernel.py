from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
import random

from gsocialsim.agents.agent import Agent
from gsocialsim.analytics.analytics import Analytics
from gsocialsim.evolution.evolutionary_system import EvolutionarySystem
from gsocialsim.kernel.sim_clock import SimClock
from gsocialsim.kernel.event_scheduler import EventScheduler
from gsocialsim.kernel.world_context import WorldContext
from gsocialsim.kernel.stimulus_ingestion import StimulusIngestionEngine
from gsocialsim.kernel.events import (
    DayBoundaryEvent,
    StimulusIngestionEvent,
    AgentActionEvent,
    AllocateAttentionEvent,
)
from gsocialsim.networks.network_layer import NetworkLayer
from gsocialsim.physical.physical_world import PhysicalWorld
from gsocialsim.social.global_social_reality import GlobalSocialReality


@dataclass
class AgentPopulation:
    agents: Dict[str, Agent] = field(default_factory=dict)

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.id] = agent

    def replace(self, exited_agent_id: str, newborn_agent: Agent) -> None:
        if exited_agent_id in self.agents:
            del self.agents[exited_agent_id]
        self.add_agent(newborn_agent)

    def get(self, agent_id: str, default=None):
        return self.agents.get(agent_id, default)

    def __getitem__(self, agent_id: str) -> Agent:
        return self.agents[agent_id]

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self.agents

    def items(self):
        return self.agents.items()

    def keys(self):
        return self.agents.keys()

    def values(self):
        return self.agents.values()


@dataclass
class WorldKernel:
    seed: int
    clock: SimClock = field(default_factory=SimClock)
    rng: random.Random = field(init=False)

    agents: AgentPopulation = field(default_factory=AgentPopulation)
    analytics: Analytics = field(default_factory=Analytics)

    gsr: GlobalSocialReality = field(default_factory=GlobalSocialReality)

    network: NetworkLayer = field(default_factory=NetworkLayer)
    physical_world: PhysicalWorld = field(default_factory=PhysicalWorld)
    evolutionary_system: EvolutionarySystem = field(default_factory=EvolutionarySystem)
    stimulus_engine: StimulusIngestionEngine = field(default_factory=StimulusIngestionEngine)
    scheduler: EventScheduler = field(default_factory=EventScheduler)

    world_context: WorldContext = field(init=False)

    # Internal state: ensures we seed the run loop exactly once
    _started: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            analytics=self.analytics,
            gsr=self.gsr,
            network=self.network,
            clock=self.clock,
            physical_world=self.physical_world,
            evolutionary_system=self.evolutionary_system,
            stimulus_engine=self.stimulus_engine,
            scheduler=self.scheduler,
            agents=self.agents,
        )

    def _schedule_agent_loops(self, agent_id: str) -> None:
        """
        Schedule the recurring per-agent loop events for a given agent.
        """
        self.scheduler.schedule(AgentActionEvent(timestamp=self.clock.t, agent_id=agent_id))
        self.scheduler.schedule(AllocateAttentionEvent(timestamp=self.clock.t, agent_id=agent_id))

    def start(self) -> None:
        """
        Seeds the initial events to start the simulation.

        This is real functionality: a kernel that can step forward should
        have its run-loop seeded. We allow calling start() explicitly,
        but we also auto-start on first step() for a sane public API.
        """
        if self._started:
            return

        self._started = True

        # First day boundary at end of day 0 (relative to current clock)
        self.scheduler.schedule(DayBoundaryEvent(timestamp=self.clock.t + self.clock.ticks_per_day))

        # Start ingestion immediately
        self.scheduler.schedule(StimulusIngestionEvent(timestamp=self.clock.t))

        # Start agent loops immediately for existing agents
        for agent_id in self.agents.agents.keys():
            self._schedule_agent_loops(agent_id)

    def step(self, num_ticks: int = 1) -> None:
        """
        Authoritative simulation advance.

        Guarantees:
          - The clock advances by exactly num_ticks (even if no events exist).
          - Events are applied in timestamp order.
          - No event with timestamp > target_tick is applied.
          - If the kernel hasn't started, it auto-starts once.
        """
        if num_ticks <= 0:
            return

        # Real functionality: stepping a kernel implies the run loop exists.
        if not self._started:
            self.start()

        target_tick = self.clock.t + num_ticks

        while True:
            next_event = self.scheduler.get_next_event()

            # No events left: advance time to the target and stop.
            if next_event is None:
                remaining = target_tick - self.clock.t
                if remaining > 0:
                    self.clock.advance(remaining)
                return

            # Event is at/after end of window: put it back, advance to target, stop.
            if next_event.timestamp >= target_tick:
                self.scheduler.schedule(next_event)
                remaining = target_tick - self.clock.t
                if remaining > 0:
                    self.clock.advance(remaining)
                return

            # Advance to event time
            delta = next_event.timestamp - self.clock.t
            if delta > 0:
                self.clock.advance(delta)

            # Apply event at current time
            next_event.apply(self.world_context)

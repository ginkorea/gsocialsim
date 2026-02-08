from dataclasses import dataclass, field
import random
from typing import Dict, Optional

from src.gsocialsim.kernel.sim_clock import SimClock
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.analytics.analytics import Analytics
from src.gsocialsim.social.global_social_reality import GlobalSocialReality
from src.gsocialsim.networks.network_layer import NetworkLayer
from src.gsocialsim.physical.physical_world import PhysicalWorld
from src.gsocialsim.evolution.evolutionary_system import EvolutionarySystem
from src.gsocialsim.kernel.stimulus_ingestion import StimulusIngestionEngine
from src.gsocialsim.kernel.event_scheduler import EventScheduler
from src.gsocialsim.kernel.events import DayBoundaryEvent, StimulusIngestionEvent, AgentActionEvent

@dataclass
class WorldContext:
    analytics: Analytics
    gsr: GlobalSocialReality
    network: NetworkLayer
    clock: SimClock
    physical_world: PhysicalWorld
    evolutionary_system: EvolutionarySystem
    stimulus_engine: StimulusIngestionEngine
    scheduler: EventScheduler
    agents: "AgentPopulation"

@dataclass
class AgentPopulation:
    agents: Dict[str, Agent] = field(default_factory=dict)
    def get(self, agent_id: str) -> Optional[Agent]: return self.agents.get(agent_id)
    def add_agent(self, agent: Agent): self.agents[agent.id] = agent
    def replace(self, exited_agent_id: str, newborn_agent: Agent):
        if exited_agent_id in self.agents: del self.agents[exited_agent_id]
        self.add_agent(newborn_agent)

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

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            analytics=self.analytics, gsr=self.gsr, network=self.network,
            clock=self.clock, physical_world=self.physical_world,
            evolutionary_system=self.evolutionary_system, stimulus_engine=self.stimulus_engine,
            scheduler=self.scheduler, agents=self.agents
        )

    def start(self):
        """Seeds the initial events to start the simulation."""
        # Schedule the first of each perpetual event
        self.scheduler.schedule(DayBoundaryEvent(timestamp=self.clock.ticks_per_day))
        self.scheduler.schedule(StimulusIngestionEvent(timestamp=0))
        for agent_id in self.agents.agents.keys():
            self.scheduler.schedule(AgentActionEvent(timestamp=0, agent_id=agent_id))

    def step(self, num_ticks: int = 1):
        """Processes events for a given number of ticks."""
        target_tick = self.clock.t + num_ticks

        # Loop until the event queue is empty or the target time is reached
        while self.clock.t < target_tick:
            next_event = self.scheduler.get_next_event()
            if not next_event:
                print("Event queue is empty. Halting simulation.")
                break

            # If the next event is in the future, we can simply advance the clock
            if next_event.timestamp >= target_tick:
                self.scheduler.schedule(next_event) # Put it back
                self.clock.t = target_tick # Move time to the end of the window
                break

            # Advance clock to the event's time
            self.clock.t = next_event.timestamp
            
            # Apply the event, which may schedule future events
            next_event.apply(self.world_context)

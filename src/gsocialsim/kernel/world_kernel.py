import random
from typing import Dict, Optional
from dataclasses import dataclass, field

from src.gsocialsim.kernel.sim_clock import SimClock
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.analytics.analytics import Analytics
from src.gsocialsim.social.global_social_reality import GlobalSocialReality
from src.gsocialsim.networks.network_layer import NetworkLayer


# Placeholder for EventScheduler (will be implemented in later phases)
class EventScheduler:
    def __init__(self):
        pass

# Placeholder for DeterministicReplay (will be implemented in later phases)
class DeterministicReplay:
    def __init__(self):
        pass

# Placeholder for WorldContext (will be expanded in later phases)
@dataclass
class WorldContext:
    # This will eventually hold references to agents, GSR, networks, etc.
    analytics: Analytics
    gsr: GlobalSocialReality
    network: NetworkLayer # For now, a single default network

@dataclass
class AgentPopulation:
    agents: Dict[str, Agent] = field(default_factory=dict)

    def get(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def add_agent(self, agent: Agent):
        self.agents[agent.id] = agent

    def replace(self, exited_agent_id: str, newborn_agent: Agent):
        if exited_agent_id in self.agents:
            del self.agents[exited_agent_id]
        self.add_agent(newborn_agent)


@dataclass
class WorldKernel:
    seed: int
    clock: SimClock = field(default_factory=SimClock)
    rng: random.Random = field(init=False)
    agents: AgentPopulation = field(default_factory=AgentPopulation)
    
    # Placeholders for other subsystems
    event_scheduler: EventScheduler = field(default_factory=EventScheduler)
    deterministic_replay: DeterministicReplay = field(default_factory=DeterministicReplay)
    analytics: Analytics = field(default_factory=Analytics)
    gsr: GlobalSocialReality = field(default_factory=GlobalSocialReality)
    network: NetworkLayer = field(default_factory=NetworkLayer)
    world_context: WorldContext = field(init=False)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            analytics=self.analytics,
            gsr=self.gsr,
            network=self.network
        )

    def step(self, num_ticks: int = 1):
        self.clock.advance(num_ticks)
        # In this phase, perception is triggered manually in tests.
        # In later phases, this step loop will trigger agent ticks automatically.


import random
from typing import Dict, Optional
from dataclasses import dataclass, field

from src.gsocialsim.kernel.sim_clock import SimClock
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.analytics.analytics import Analytics
from src.gsocialsim.social.global_social_reality import GlobalSocialReality
from src.gsocialsim.networks.network_layer import NetworkLayer
from src.gsocialsim.physical.physical_world import PhysicalWorld
from src.gsocialsim.evolution.evolutionary_system import EvolutionarySystem
from src.gsocialsim.stimuli.content_item import ContentItem


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
    clock: SimClock
    physical_world: PhysicalWorld
    evolutionary_system: EvolutionarySystem

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
    physical_world: PhysicalWorld = field(default_factory=PhysicalWorld)
    evolutionary_system: EvolutionarySystem = field(default_factory=EvolutionarySystem)
    world_context: WorldContext = field(init=False)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            analytics=self.analytics,
            gsr=self.gsr,
            network=self.network,
            clock=self.clock,
            physical_world=self.physical_world,
            evolutionary_system=self.evolutionary_system
        )

    def step(self, num_ticks: int = 1):
        for _ in range(num_ticks):
            current_tick = self.clock.t
            tick_of_day = self.clock.tick_of_day
            all_agents = list(self.agents.agents.values())
            
            # --- 1. Action Phase (Online) ---
            posts_this_tick = []
            for agent in all_agents:
                new_content = agent.act(tick=current_tick)
                if new_content:
                    posts_this_tick.append(new_content)
            
            # --- 2. Physical Interaction Phase ---
            co_located_groups = self.physical_world.get_co_located_agents(tick_of_day)
            for group in co_located_groups:
                for author_id in group:
                    author = self.agents.get(author_id)
                    if not author.beliefs.topics: continue
                    topic = author.rng.choice(list(author.beliefs.topics.keys()))
                    author_belief = author.beliefs.get(topic)
                    
                    physical_content = ContentItem(
                        id=f"phys_{author_id}_{current_tick}",
                        author_id=author_id, topic=topic, stance=author_belief.stance
                    )

                    for viewer_id in group:
                        if viewer_id != author_id:
                            viewer = self.agents.get(viewer_id)
                            viewer.perceive(physical_content, self.world_context, is_physical=True)

            # --- 3. Online Perception Phase ---
            if posts_this_tick:
                from src.gsocialsim.policy.bandit_learner import RewardVector
                for agent in all_agents:
                    following_list = self.world_context.network.graph.get_following(agent.id)
                    for post in posts_this_tick:
                        if post.author_id in following_list:
                            agent.perceive(post, self.world_context)
                            reward = RewardVector(affiliation=0.1)
                            author = self.agents.get(post.author_id)
                            if author:
                                author.learn(post.topic, reward)
            
            # --- 4. Day Boundary and Evolution ---
            day_before = self.clock.day
            self.clock.advance(1)
            day_after = self.clock.day

            if day_after > day_before:
                # First, all agents consolidate
                current_agents = list(self.agents.agents.values())
                for agent in current_agents:
                    agent.consolidate_daily(self.world_context)

                # Then, evolution happens
                agents_to_exit = [a for a in current_agents if self.evolutionary_system.should_exit(a)]
                
                if current_agents: # Ensure there's at least one agent to be a parent
                    fittest_parent = max(current_agents, key=lambda a: sum(a.policy.action_rewards.values()), default=None)

                    if fittest_parent:
                        for exited_agent in agents_to_exit:
                            new_id = f"gen2_{exited_agent.id}"
                            newborn = self.evolutionary_system.reproduce(fittest_parent, new_id, self.rng.randint(0, 10**9))
                            self.agents.replace(exited_agent.id, newborn)


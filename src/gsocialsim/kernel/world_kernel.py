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
from src.gsocialsim.kernel.stimulus_ingestion import StimulusIngestionEngine
from src.gsocialsim.types import TopicId

@dataclass
class WorldContext:
    analytics: Analytics
    gsr: GlobalSocialReality
    network: NetworkLayer
    clock: SimClock
    physical_world: PhysicalWorld
    evolutionary_system: EvolutionarySystem
    stimulus_engine: StimulusIngestionEngine

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
    world_context: WorldContext = field(init=False)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            analytics=self.analytics, gsr=self.gsr, network=self.network,
            clock=self.clock, physical_world=self.physical_world,
            evolutionary_system=self.evolutionary_system, stimulus_engine=self.stimulus_engine
        )

    def step(self, num_ticks: int = 1):
        for _ in range(num_ticks):
            current_tick = self.clock.t
            all_agents = list(self.agents.agents.values())

            # --- Phase 0: Stimulus Ingestion ---
            new_stimuli_this_tick = self.stimulus_engine.tick(current_tick)
            
            # --- Phase 1: Stimulus Perception ---
            if new_stimuli_this_tick:
                for agent in all_agents:
                    for stimulus in new_stimuli_this_tick:
                        temp_content = ContentItem(
                            id=stimulus.id, author_id=stimulus.source,
                            topic=TopicId(f"stim_{stimulus.id}"), stance=0.0
                        )
                        agent.perceive(temp_content, self.world_context, stimulus_id=stimulus.id)

            # --- Phase 2: Agent Action ---
            interactions_this_tick = []
            for agent in all_agents:
                new_interaction = agent.act(tick=current_tick)
                if new_interaction:
                    interactions_this_tick.append(new_interaction)
                    self.analytics.log_interaction(current_tick, new_interaction)
            
            # --- Phase 3: Interaction Perception ---
            if interactions_this_tick:
                from src.gsocialsim.policy.bandit_learner import RewardVector
                from src.gsocialsim.stimuli.interaction import InteractionVerb
                
                for viewer in all_agents:
                    following_list = self.world_context.network.graph.get_following(viewer.id)
                    for interaction in interactions_this_tick:
                        if interaction.agent_id == viewer.id or interaction.agent_id not in following_list:
                            continue
                        
                        author = self.agents.get(interaction.agent_id)
                        reward = RewardVector(affiliation=0.1)
                        
                        if interaction.verb == InteractionVerb.CREATE:
                            viewer.perceive(interaction.original_content, self.world_context)
                            author.learn(f"CREATE_{interaction.original_content.topic}", reward)
                        elif interaction.verb in [InteractionVerb.FORWARD, InteractionVerb.LIKE]:
                             author.learn(f"{interaction.verb.value}_{interaction.target_stimulus_id}", reward)
            
            # --- Phase 4: Day Boundary ---
            day_before = self.clock.day
            self.clock.advance(1)
            if self.clock.day > day_before:
                for agent in all_agents:
                    agent.consolidate_daily(self.world_context)
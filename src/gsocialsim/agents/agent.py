from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from collections import deque
import random

from gsocialsim.agents.identity_state import IdentityState
from gsocialsim.agents.belief_state import BeliefStore
from gsocialsim.agents.emotion_state import EmotionState
from gsocialsim.agents.budget_state import BudgetState, BudgetKind
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.agents.attention_system import AttentionSystem
from gsocialsim.agents.belief_update_engine import BeliefUpdateEngine
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.policy.bandit_learner import BanditLearner, RewardVector
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.agents.impression import Impression

if TYPE_CHECKING:
    from gsocialsim.kernel.world_kernel import WorldContext
    from gsocialsim.types import TopicId

class MemoryStore: pass

@dataclass
class Agent:
    id: str
    seed: int
    identity: IdentityState = field(default_factory=IdentityState)
    beliefs: BeliefStore = field(default_factory=BeliefStore)
    emotion: EmotionState = field(default_factory=EmotionState)
    budgets: BudgetState = field(default_factory=BudgetState)
    personality: RewardWeights = field(default_factory=RewardWeights)
    rng: random.Random = field(init=False)
    attention: AttentionSystem = field(default_factory=AttentionSystem)
    belief_update_engine: BeliefUpdateEngine = field(default_factory=BeliefUpdateEngine)
    memory: MemoryStore = field(default_factory=MemoryStore)
    policy: BanditLearner = field(default_factory=BanditLearner)
    # Store the most recent impressions, keyed by content_id
    recent_impressions: dict[str, Impression] = field(default_factory=dict)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.budgets._rng = self.rng

    def perceive(self, content: ContentItem, context: "WorldContext", is_physical: bool = False, stimulus_id: Optional[str] = None):
        impression = self.attention.evaluate(content, is_physical=is_physical)
        # Store the impression for potential deep focus/later action
        if impression.content_id:
            self.recent_impressions[impression.content_id] = impression

        context.analytics.log_exposure(
            viewer_id=self.id, source_id=content.author_id, topic=content.topic,
            is_physical=is_physical, timestamp=context.clock.t
        )
        
        old_stance = self.beliefs.get(content.topic).stance if self.beliefs.get(content.topic) else 0.0
        belief_delta = self.belief_update_engine.update(
            viewer=self,
            content_author_id=content.author_id,
            impression=impression,
            gsr=context.gsr
        )
        
        self.beliefs.apply_delta(belief_delta)
        new_stance = self.beliefs.get(content.topic).stance
        
        if context.analytics.crossing_detector.check(old_stance, new_stance):
            attribution = context.analytics.attribution_engine.assign_credit(
                agent_id=self.id, topic=content.topic, history=context.analytics.exposure_history
            )
            from gsocialsim.analytics.attribution import BeliefCrossingEvent
            crossing_event = BeliefCrossingEvent(
                timestamp=context.clock.t, agent_id=self.id, topic=content.topic,
                old_stance=old_stance, new_stance=new_stance, attribution=attribution
            )
            context.analytics.log_belief_crossing(crossing_event)
        
        context.analytics.log_belief_update(timestamp=context.clock.t, agent_id=self.id, delta=belief_delta)

    def learn(self, action_key: str, reward_vector: RewardVector):
        self.policy.learn(action_key, reward_vector)

    def act(self, tick: int) -> Optional[Interaction]:
        if self.budgets.action_budget < 1: return None
        interaction = self.policy.generate_interaction(self, tick)
        if interaction:
            self.budgets.spend(BudgetKind.ACTION, 1.0)
            reward = RewardVector()
            topic = None
            if interaction.verb == InteractionVerb.LIKE:
                reward.affiliation = 0.2
                topic = interaction.target_stimulus_id
            elif interaction.verb == InteractionVerb.FORWARD:
                reward.status = 0.3
                topic = interaction.target_stimulus_id
            if topic:
                action_key = f"{interaction.verb.value}_{topic}"
                self.learn(action_key, reward)
        return interaction

    def consolidate_daily(self, world_context):
        self.budgets.regen_daily()
        self.recent_impressions.clear() # Clear memory of impressions daily
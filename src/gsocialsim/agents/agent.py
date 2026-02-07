from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from collections import deque
import random

from src.gsocialsim.agents.identity_state import IdentityState
from src.gsocialsim.agents.belief_state import BeliefStore
from src.gsocialsim.agents.emotion_state import EmotionState
from src.gsocialsim.agents.budget_state import BudgetState, BudgetKind
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.agents.attention_system import AttentionSystem
from src.gsocialsim.agents.belief_update_engine import BeliefUpdateEngine
from src.gsocialsim.stimuli.content_item import ContentItem
from src.gsocialsim.policy.bandit_learner import BanditLearner, RewardVector
from src.gsocialsim.stimuli.interaction import Interaction

if TYPE_CHECKING:
    from src.gsocialsim.kernel.world_kernel import WorldContext
    from src.gsocialsim.types import TopicId

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
    recent_exposures: deque[str] = field(default_factory=lambda: deque(maxlen=20))

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.budgets._rng = self.rng

    def perceive(self, content: ContentItem, context: "WorldContext", is_physical: bool = False, stimulus_id: Optional[str] = None):
        impression = self.attention.evaluate(content, is_physical=is_physical)
        if stimulus_id and stimulus_id not in self.recent_exposures:
            self.recent_exposures.append(stimulus_id)

        context.analytics.log_exposure(
            viewer_id=self.id, source_id=content.author_id, topic=content.topic,
            is_physical=is_physical, timestamp=context.clock.t
        )
        old_stance = self.beliefs.get(content.topic).stance if self.beliefs.get(content.topic) else 0.0
        belief_delta = self.belief_update_engine.update(
            viewer_id=self.id, content_author_id=content.author_id, belief_store=self.beliefs,
            impression=impression, gsr=context.gsr
        )
        self.beliefs.apply_delta(belief_delta)
        new_stance = self.beliefs.get(content.topic).stance
        if context.analytics.crossing_detector.check(old_stance, new_stance):
            attribution = context.analytics.attribution_engine.assign_credit(
                agent_id=self.id, topic=content.topic, history=context.analytics.exposure_history
            )
            from src.gsocialsim.analytics.attribution import BeliefCrossingEvent
            crossing_event = BeliefCrossingEvent(
                timestamp=context.clock.t, agent_id=self.id, topic=content.topic,
                old_stance=old_stance, new_stance=new_stance, attribution=attribution
            )
            context.analytics.log_belief_crossing(crossing_event)

        context.analytics.log_belief_update(timestamp=context.clock.t, agent_id=self.id, delta=belief_delta)

    def learn(self, action_key: str, reward_vector: RewardVector):
        subjective_reward = reward_vector.weighted_sum(self.personality)
        self.policy.learn(action_key, subjective_reward)

    def act(self, tick: int) -> Optional[Interaction]:
        if self.budgets.action_budget < 1:
            return None
        interaction = self.policy.generate_interaction(self, tick)
        if interaction:
            self.budgets.spend(BudgetKind.ACTION, 1.0)
        return interaction

    def consolidate_daily(self, world_context):
        self.budgets.regen_daily()
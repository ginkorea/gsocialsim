import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.gsocialsim.agents.identity_state import IdentityState
from src.gsocialsim.agents.belief_state import BeliefStore
from src.gsocialsim.agents.emotion_state import EmotionState
from src.gsocialsim.agents.budget_state import BudgetState
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.agents.attention_system import AttentionSystem
from src.gsocialsim.agents.belief_update_engine import BeliefUpdateEngine
from src.gsocialsim.stimuli.content_item import ContentItem

if TYPE_CHECKING:
    from src.gsocialsim.kernel.world_kernel import WorldContext

# Placeholders for other agent components
class MemoryStore: pass
class ActionPolicy: pass
class BanditLearner: pass

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

    # Systems for cognition and behavior
    attention: AttentionSystem = field(default_factory=AttentionSystem)
    belief_update_engine: BeliefUpdateEngine = field(default_factory=BeliefUpdateEngine)
    memory: MemoryStore = field(default_factory=MemoryStore)
    policy: ActionPolicy = field(default_factory=ActionPolicy)
    learn: BanditLearner = field(default_factory=BanditLearner)


    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.budgets._rng = self.rng # Pass the agent's RNG to its budget state

    def perceive(self, content: ContentItem, context: "WorldContext"):
        """
        The core perception-to-belief-update loop for Phase 2.
        """
        # 1. Use AttentionSystem to generate an Impression from the content
        impression = self.attention.evaluate(content)

        # 2. Use BeliefUpdateEngine to calculate the change based on the impression
        belief_delta = self.belief_update_engine.update(
            viewer_id=self.id,
            content_author_id=content.author_id,
            belief_store=self.beliefs,
            impression=impression,
            gsr=context.gsr
        )

        # 3. Apply the change to the agent's own belief store
        self.beliefs.apply_delta(belief_delta)

        # 4. Log the event using the analytics system from the world context
        context.analytics.log_belief_update(
            timestamp=0, # Placeholder for clock time
            agent_id=self.id,
            delta=belief_delta
        )


    def tick(self, world_context):
        # Phase 2: Agent perception is driven externally by the test script
        pass

    def consolidate_daily(self, world_context):
        # Phase 2: No daily consolidation logic yet
        pass

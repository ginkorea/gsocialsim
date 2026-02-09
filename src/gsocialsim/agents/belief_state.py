from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from gsocialsim.agents.belief_update_engine import BeliefDelta

TopicId = str


@dataclass
class TopicBelief:
    topic: TopicId
    stance: float = 0.0       # [-1,+1]
    confidence: float = 0.0   # [0,1]
    salience: float = 0.0     # [0,1]
    knowledge: float = 0.0    # [0,1]


@dataclass
class BeliefStore:
    topics: Dict[TopicId, TopicBelief] = field(default_factory=dict)

    def get(self, topic_id: TopicId) -> Optional[TopicBelief]:
        return self.topics.get(topic_id)

    def update(self, topic_id: TopicId, stance: float, confidence: float, salience: float, knowledge: float):
        belief = self.topics.get(topic_id)
        if belief:
            belief.stance = stance
            belief.confidence = confidence
            belief.salience = salience
            belief.knowledge = knowledge
        else:
            self.topics[topic_id] = TopicBelief(
                topic=topic_id,
                stance=stance,
                confidence=confidence,
                salience=salience,
                knowledge=knowledge,
            )

    def apply_delta(self, delta: "BeliefDelta"):
        """Applies a belief delta to the current store."""
        belief = self.get(delta.topic_id)
        if belief is None:
            self.topics[delta.topic_id] = TopicBelief(
                topic=delta.topic_id,
                stance=delta.stance_delta,
                confidence=delta.confidence_delta,
            )
        else:
            belief.stance = max(-1.0, min(1.0, belief.stance + delta.stance_delta))
            belief.confidence = max(0.0, min(1.0, belief.confidence + delta.confidence_delta))

    # ---- New: safe consolidation helpers ----
    def nudge_salience(self, topic_id: TopicId, delta: float):
        belief = self.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief
        belief.salience = max(0.0, min(1.0, belief.salience + float(delta)))

    def nudge_knowledge(self, topic_id: TopicId, delta: float):
        belief = self.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief
        belief.knowledge = max(0.0, min(1.0, belief.knowledge + float(delta)))

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from gsocialsim.agents.belief_update_engine import BeliefDelta

TopicId = str


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(x)))


@dataclass
class TopicBelief:
    topic: TopicId
    stance: float = 0.0       # [-1,+1]
    confidence: float = 0.0   # [0,1]
    salience: float = 0.0     # [0,1]
    knowledge: float = 0.0    # [0,1]


@dataclass
class BeliefStore:
    """
    Canonical belief vector store.

    Contract note:
    - apply_delta() must be pure state mutation (no logging, no side effects).
    - WorldKernel CONSOLIDATE(t) is responsible for calling apply_delta() for queued deltas.
    """
    topics: Dict[TopicId, TopicBelief] = field(default_factory=dict)

    def get(self, topic_id: TopicId) -> Optional[TopicBelief]:
        return self.topics.get(topic_id)

    def update(self, topic_id: TopicId, stance: float, confidence: float, salience: float, knowledge: float) -> None:
        belief = self.topics.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief

        belief.stance = _clamp(stance, -1.0, 1.0)
        belief.confidence = _clamp(confidence, 0.0, 1.0)
        belief.salience = _clamp(salience, 0.0, 1.0)
        belief.knowledge = _clamp(knowledge, 0.0, 1.0)

    def apply_delta(self, delta: "BeliefDelta") -> None:
        """
        Applies a belief delta to the current store.

        Important:
        - Initializes all fields so later consolidation steps (salience/knowledge nudges) are safe.
        - Clamps stance/confidence.
        """
        topic_id = delta.topic_id
        belief = self.topics.get(topic_id)

        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief

        belief.stance = _clamp(belief.stance + float(delta.stance_delta), -1.0, 1.0)
        belief.confidence = _clamp(belief.confidence + float(delta.confidence_delta), 0.0, 1.0)

        # Leave salience/knowledge unchanged here (separate mechanisms control them)

    # ---- Consolidation helpers ----
    def nudge_salience(self, topic_id: TopicId, delta: float) -> None:
        belief = self.topics.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief
        belief.salience = _clamp(belief.salience + float(delta), 0.0, 1.0)

    def nudge_knowledge(self, topic_id: TopicId, delta: float) -> None:
        belief = self.topics.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief
        belief.knowledge = _clamp(belief.knowledge + float(delta), 0.0, 1.0)

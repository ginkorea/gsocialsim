from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
import random

from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


@dataclass
class TopicReality:
    """
    Global "outside-the-agent" state for a topic.

    truth: objective ground-truth strength in [0, 1]
    salience: visibility / availability in [0, 1]
    institutional_stance: optional stance in [-1, 1] (future use)
    volatility: how fast salience decays (higher = faster)
    """
    truth: float = 0.5
    salience: float = 0.0
    institutional_stance: float = 0.0
    volatility: float = 0.02


@dataclass
class GlobalSocialReality:
    """
    Global social reality includes:
      1) Latent dyadic relationship vectors between agent pairs (symmetric).
      2) Topic-level external reality (truth + salience), which agents observe imperfectly.
    """

    # --- (1) Relationships ---
    # Key is a sorted tuple of two AgentIds to ensure R(u,v) == R(v,u)
    _relations: Dict[Tuple[AgentId, AgentId], RelationshipVector] = field(default_factory=dict)

    # --- (2) Topic reality ---
    topics: Dict[TopicId, TopicReality] = field(default_factory=dict)
    default_truth: float = 0.5
    default_volatility: float = 0.02

    # ----------------------------
    # Relationships API (unchanged)
    # ----------------------------
    def _get_key(self, u: AgentId, v: AgentId) -> Tuple[AgentId, AgentId]:
        """Creates a canonical key for a pair of agents (self-relationships allowed)."""
        if u == v:
            return (u, v)
        return tuple(sorted((u, v)))

    def get_relationship(self, u: AgentId, v: AgentId) -> RelationshipVector:
        """
        Gets the relationship between two agents.
        If no relationship exists, it creates and returns a default one.
        Self-relationships are treated as maximally trusted by default.
        """
        key = self._get_key(u, v)
        if key not in self._relations:
            if u == v:
                self._relations[key] = RelationshipVector(
                    affinity=1.0,
                    trust=1.0,
                    intimacy=1.0,
                    conflict=0.0,
                    reciprocity=1.0,
                    status_delta=0.0,
                )
            else:
                self._relations[key] = RelationshipVector()
        return self._relations[key]

    def set_relationship(self, u: AgentId, v: AgentId, vector: RelationshipVector) -> None:
        """Sets a specific relationship vector for a pair of agents."""
        key = self._get_key(u, v)
        self._relations[key] = vector

    def update_trust(self, u: AgentId, v: AgentId, delta: float) -> float:
        """
        Adjust trust for a pair, clamped to [0,1]. Returns the new trust.
        """
        rel = self.get_relationship(u, v)
        try:
            rel.trust = _clamp01(float(rel.trust) + float(delta))
        except Exception:
            rel.trust = _clamp01(rel.trust)
        return rel.trust

    # ----------------------------
    # Topic reality API (new)
    # ----------------------------
    def ensure_topic(self, topic: TopicId) -> TopicReality:
        tr = self.topics.get(topic)
        if tr is None:
            tr = TopicReality(truth=self.default_truth, salience=0.0, volatility=self.default_volatility)
            self.topics[topic] = tr
        return tr

    def truth(self, topic: TopicId) -> float:
        return self.ensure_topic(topic).truth

    def set_truth(self, topic: TopicId, value: float) -> None:
        self.ensure_topic(topic).truth = _clamp01(value)

    def salience(self, topic: TopicId) -> float:
        return self.ensure_topic(topic).salience

    def set_salience(self, topic: TopicId, value: float) -> None:
        self.ensure_topic(topic).salience = _clamp01(value)

    def bump_salience(self, topic: TopicId, delta: float) -> None:
        tr = self.ensure_topic(topic)
        tr.salience = _clamp01(tr.salience + delta)

    def decay(self) -> None:
        """Decay salience over time (call on DayBoundaryEvent, etc.)."""
        for tr in self.topics.values():
            tr.salience = _clamp01(tr.salience * (1.0 - tr.volatility))

    def observe_truth(
        self,
        topic: TopicId,
        *,
        rng: Optional[random.Random] = None,
        noise_std: float = 0.08,
        attention_gain: float = 1.0,
    ) -> float:
        """
        Noisy observation of objective truth in [0, 1].
        Higher attention_gain => less noise.
        """
        r = rng or random
        tr = self.ensure_topic(topic)
        std = max(1e-6, noise_std / max(1e-6, attention_gain))
        return _clamp01(tr.truth + r.gauss(0.0, std))

    def observe_salience(
        self,
        topic: TopicId,
        *,
        rng: Optional[random.Random] = None,
        noise_std: float = 0.05,
    ) -> float:
        r = rng or random
        tr = self.ensure_topic(topic)
        return _clamp01(tr.salience + r.gauss(0.0, noise_std))

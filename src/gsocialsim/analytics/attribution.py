from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional
from collections import defaultdict, deque

from gsocialsim.types import AgentId, TopicId, ActorId


@dataclass
class ExposureEvent:
    timestamp: int
    source_actor_id: ActorId
    topic: TopicId
    is_physical: bool

    # --- new optional fields (backward compatible) ---
    content_id: Optional[str] = None
    channel: Optional[str] = None        # e.g., "broadcast", "dm", "physical"
    intake_mode: Optional[str] = None    # "scroll", "seek", "physical", "deep_focus"
    media_type: Optional[str] = None     # "news", "social_post", etc.
    consumed: bool = False               # True only when the agent actually consumes


class ExposureHistory:
    """Logs every piece of content an agent is exposed to (and optionally whether it was consumed)."""
    def __init__(self, max_history_per_agent: int = 2000):
        self._max = max(1, int(max_history_per_agent))
        self._history: Dict[AgentId, Deque[ExposureEvent]] = defaultdict(self._new_deque)

    def _new_deque(self) -> Deque[ExposureEvent]:
        return deque(maxlen=self._max)

    def log_exposure(self, viewer_id: AgentId, event: ExposureEvent):
        self._history[viewer_id].append(event)

    def get_history_for_agent(self, agent_id: AgentId) -> List[ExposureEvent]:
        hist = self._history.get(agent_id)
        if not hist:
            return []
        return list(hist)


@dataclass
class BeliefCrossingEvent:
    timestamp: int
    agent_id: AgentId
    topic: TopicId
    old_stance: float
    new_stance: float
    attribution: Dict[ActorId, float] = field(default_factory=dict)


class BeliefCrossingDetector:
    """Checks if a belief update crosses a meaningful threshold."""
    def check(self, old_stance: float, new_stance: float) -> bool:
        # Simple: sign-crossing
        return (old_stance <= 0 and new_stance > 0) or (old_stance >= 0 and new_stance < 0)


class AttributionEngine:
    """
    Assigns credit for a belief crossing event.

    Current model: recency-weighted accumulator over matching-topic exposure events.
    Boost factors:
      - physical exposures are stronger
      - consumed exposures are stronger than mere exposures
    """
    def assign_credit(
        self,
        agent_id: AgentId,
        topic: TopicId,
        history: ExposureHistory,
        window_days: int = 7,
    ) -> Dict[ActorId, float]:
        credits = defaultdict(float)
        total = 0.0
        agent_history = history.get_history_for_agent(agent_id)

        # TODO: incorporate real timestamp->day conversion. For now we treat history order as recency.
        # Weight decays with distance in the reversed list.
        decay = 0.97

        w = 1.0
        for event in reversed(agent_history):
            if event.topic != topic:
                w *= decay
                continue

            weight = w

            # Physical gets a boost (as your design intends)
            if event.is_physical:
                weight *= 5.0

            # Consumed gets a boost over mere exposure
            if getattr(event, "consumed", False):
                weight *= 1.75

            credits[event.source_actor_id] += weight
            total += weight

            w *= decay

        if total <= 0.0:
            return {}

        return {actor: val / total for actor, val in credits.items()}

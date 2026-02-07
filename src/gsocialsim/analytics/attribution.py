from dataclasses import dataclass, field
from typing import Dict, List
from collections import defaultdict
from src.gsocialsim.types import AgentId, TopicId, ActorId

@dataclass
class ExposureEvent:
    timestamp: int
    source_actor_id: ActorId
    topic: TopicId
    is_physical: bool

class ExposureHistory:
    """Logs every piece of content an agent is exposed to."""
    def __init__(self):
        self._history: Dict[AgentId, List[ExposureEvent]] = defaultdict(list)

    def log_exposure(self, viewer_id: AgentId, event: ExposureEvent):
        self._history[viewer_id].append(event)

    def get_history_for_agent(self, agent_id: AgentId) -> List[ExposureEvent]:
        return self._history.get(agent_id, [])

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
        # A simple crossing from non-positive to positive, or vice-versa
        return (old_stance <= 0 and new_stance > 0) or (old_stance >= 0 and new_stance < 0)

class AttributionEngine:
    """Assigns credit for a belief crossing event."""
    def assign_credit(self, agent_id: AgentId, topic: TopicId, history: ExposureHistory, window_days: int = 7) -> Dict[ActorId, float]:
        credits = defaultdict(float)
        total_credit = 0.0
        agent_history = history.get_history_for_agent(agent_id)
        
        # A simple recency-based model
        for event in reversed(agent_history):
            if event.topic == topic:
                # TODO: Use real timestamp difference
                weight = 1.0 # Simple weight for now
                if event.is_physical:
                    weight *= 5.0 # Physical gets more credit
                credits[event.source_actor_id] += weight
                total_credit += weight

        if total_credit == 0:
            return {}
            
        # Normalize credits
        return {actor: val / total_credit for actor, val in credits.items()}

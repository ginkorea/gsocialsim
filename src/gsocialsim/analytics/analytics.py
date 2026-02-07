from typing import Any
from src.gsocialsim.analytics.attribution import (
    ExposureHistory,
    BeliefCrossingDetector,
    AttributionEngine,
    BeliefCrossingEvent,
    ExposureEvent
)

class Analytics:
    """
    Phase 7: A logger that also manages exposure history and belief crossing attribution.
    """
    def __init__(self):
        self.exposure_history = ExposureHistory()
        self.crossing_detector = BeliefCrossingDetector()
        self.attribution_engine = AttributionEngine()
        self.crossings: list[BeliefCrossingEvent] = []

    def log_belief_update(self, timestamp: int, agent_id: str, delta: Any):
        # This can be commented out for cleaner output if desired
        # print(
        #     f"LOG:[T={timestamp}] Agent['{agent_id}'] BeliefUpdate: "
        #     f"Topic='{delta.topic_id}', StanceΔ={delta.stance_delta:.4f}, ConfΔ={delta.confidence_delta:.4f}"
        # )
        pass
    
    def log_exposure(self, viewer_id: str, source_id: str, topic: str, is_physical: bool, timestamp: int):
        event = ExposureEvent(
            timestamp=timestamp,
            source_actor_id=source_id,
            topic=topic,
            is_physical=is_physical
        )
        self.exposure_history.log_exposure(viewer_id, event)

    def log_belief_crossing(self, event: BeliefCrossingEvent):
        print(
            f"LOG:[T={event.timestamp}] Agent['{event.agent_id}'] BeliefCrossing: "
            f"Topic='{event.topic}', Stance={event.old_stance:.2f}->{event.new_stance:.2f}, "
            f"Attribution={event.attribution}"
        )
        self.crossings.append(event)

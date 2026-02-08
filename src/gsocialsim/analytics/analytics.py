from typing import Any
from gsocialsim.analytics.attribution import (
    ExposureHistory,
    BeliefCrossingDetector,
    AttributionEngine,
    BeliefCrossingEvent,
    ExposureEvent
)
from gsocialsim.stimuli.interaction import Interaction

class Analytics:
    """
    Manages all logging for the simulation, including verbose debugging
    and storing data for visualization.
    """
    def __init__(self):
        self.exposure_history = ExposureHistory()
        self.crossing_detector = BeliefCrossingDetector()
        self.attribution_engine = AttributionEngine()
        self.crossings: list[BeliefCrossingEvent] = []
        self.interactions: list[Interaction] = []

    def log_belief_update(self, timestamp: int, agent_id: str, delta: Any):
        print(
            f"DEBUG:[T={timestamp}] Agent['{agent_id}'] BeliefUpdate: "
            f"Topic='{delta.topic_id}', StanceΔ={delta.stance_delta:.4f}, ConfΔ={delta.confidence_delta:.4f}"
        )
    
    def log_exposure(self, viewer_id: str, source_id: str, topic: str, is_physical: bool, timestamp: int):
        print(
            f"DEBUG:[T={timestamp}] Agent['{viewer_id}'] Perceived: "
            f"Source='{source_id}', Topic='{topic}', Physical={is_physical}"
        )
        event = ExposureEvent(
            timestamp=timestamp,
            source_actor_id=source_id,
            topic=topic,
            is_physical=is_physical
        )
        self.exposure_history.log_exposure(viewer_id, event)

    def log_interaction(self, timestamp: int, interaction: Interaction):
        target = interaction.target_stimulus_id or (interaction.original_content.id if interaction.original_content else 'None')
        print(
            f"DEBUG:[T={timestamp}] Agent['{interaction.agent_id}'] Interacted: "
            f"Verb='{interaction.verb.value}', Target='{target}'"
        )
        self.interactions.append(interaction)

    def log_belief_crossing(self, event: BeliefCrossingEvent):
        print(
            f"LOG:[T={event.timestamp}] Agent['{event.agent_id}'] BeliefCrossing: "
            f"Topic='{event.topic}', Stance={event.old_stance:.2f}->{event.new_stance:.2f}, "
            f"Attribution={event.attribution}"
        )
        self.crossings.append(event)
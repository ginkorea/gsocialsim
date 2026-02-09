from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from collections import defaultdict

from gsocialsim.analytics.attribution import (
    ExposureHistory,
    BeliefCrossingDetector,
    AttributionEngine,
    BeliefCrossingEvent,
    ExposureEvent,
)
from gsocialsim.stimuli.interaction import Interaction


@dataclass
class DeliveryRecord:
    """
    Optional structured delivery logging for future phases.

    You don't have to use this yet; events can call Analytics.log_delivery()
    when ready (Broadcast feed, DM, etc.).
    """
    tick: int
    viewer_id: str
    layer_id: str
    intake_mode: str
    eligible: int = 0
    shown: int = 0
    seen: int = 0
    media_breakdown: Dict[str, int] = field(default_factory=dict)


class Analytics:
    """
    Manages all logging for the simulation, including verbose debugging
    and storing data for visualization.

    Upgrades:
      - Exposed vs Consumed split
      - Daily "dream" logging (consolidation summaries)
      - Optional DeliveryRecord logging for online layers
    """
    def __init__(self):
        self.exposure_history = ExposureHistory()
        self.crossing_detector = BeliefCrossingDetector()
        self.attribution_engine = AttributionEngine()
        self.crossings: list[BeliefCrossingEvent] = []
        self.interactions: list[Interaction] = []

        # --- new: light metrics ---
        self.exposure_counts = defaultdict(int)          # (agent_id) -> count
        self.consumed_counts = defaultdict(int)          # (agent_id) -> count
        self.consumed_by_media = defaultdict(int)        # (media_type) -> count
        self.dream_runs = []                             # list of dream summaries dicts
        self.delivery_records: list[DeliveryRecord] = [] # optional

    # -----------------
    # Existing methods
    # -----------------
    def log_belief_update(self, timestamp: int, agent_id: str, delta: Any):
        print(
            f"DEBUG:[T={timestamp}] Agent['{agent_id}'] BeliefUpdate: "
            f"Topic='{delta.topic_id}', StanceΔ={delta.stance_delta:.4f}, ConfΔ={delta.confidence_delta:.4f}"
        )

    def log_exposure(
        self,
        viewer_id: str,
        source_id: str,
        topic: str,
        is_physical: bool,
        timestamp: int,
        *,
        content_id: Optional[str] = None,
        channel: Optional[str] = None,
        intake_mode: Optional[str] = None,
        media_type: Optional[str] = None,
    ):
        # Backward compatible print
        print(
            f"DEBUG:[T={timestamp}] Agent['{viewer_id}'] Perceived: "
            f"Source='{source_id}', Topic='{topic}', Physical={is_physical}"
        )

        event = ExposureEvent(
            timestamp=timestamp,
            source_actor_id=source_id,
            topic=topic,
            is_physical=is_physical,
            content_id=content_id,
            channel=channel,
            intake_mode=intake_mode,
            media_type=media_type,
            consumed=False,
        )
        self.exposure_history.log_exposure(viewer_id, event)
        self.exposure_counts[viewer_id] += 1

    def log_interaction(self, timestamp: int, interaction: Interaction):
        target = interaction.target_stimulus_id or (interaction.original_content.id if interaction.original_content else "None")
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

    # -----------------
    # New methods
    # -----------------
    def log_consumption(
        self,
        viewer_id: str,
        content_id: str,
        topic: str,
        timestamp: int,
        *,
        media_type: Optional[str] = None,
        intake_mode: Optional[str] = None,
    ):
        """
        Mark the most recent matching exposure event as consumed.
        This supports exposed vs consumed split without changing ExposureHistory structure.
        """
        # Find latest matching exposure in history and mark consumed
        hist = self.exposure_history.get_history_for_agent(viewer_id)
        for event in reversed(hist):
            if event.content_id == content_id and event.topic == topic:
                event.consumed = True
                if media_type is not None:
                    event.media_type = media_type
                if intake_mode is not None:
                    event.intake_mode = intake_mode
                break

        self.consumed_counts[viewer_id] += 1
        if media_type:
            self.consumed_by_media[str(media_type)] += 1

        print(
            f"DEBUG:[T={timestamp}] Agent['{viewer_id}'] Consumed: "
            f"Content='{content_id}', Topic='{topic}', Media={media_type}, Intake={intake_mode}"
        )

    def log_dream(
        self,
        timestamp: int,
        agent_id: str,
        *,
        consolidated: int,
        topic_counts: Dict[str, int],
        actions: int = 0,
    ):
        """
        Record a daily consolidation run ("dreaming/reflection").
        Safe to call even if visualization is minimal right now.
        """
        summary = {
            "timestamp": timestamp,
            "agent_id": agent_id,
            "consolidated": consolidated,
            "topic_counts": dict(topic_counts),
            "actions": actions,
        }
        self.dream_runs.append(summary)

        # Keep print compact but informative
        top_topics = sorted(topic_counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
        top_str = ", ".join([f"{t}:{c}" for t, c in top_topics]) if top_topics else "none"
        print(
            f"LOG:[T={timestamp}] Agent['{agent_id}'] Dream: consolidated={consolidated}, actions={actions}, top_topics={top_str}"
        )

    def log_delivery(self, record: DeliveryRecord):
        """
        Optional future hook for eligible/shown/seen pipelines.
        """
        self.delivery_records.append(record)
        print(
            f"DEBUG:[T={record.tick}] Delivery viewer='{record.viewer_id}' layer='{record.layer_id}' "
            f"intake='{record.intake_mode}' eligible={record.eligible} shown={record.shown} seen={record.seen}"
        )

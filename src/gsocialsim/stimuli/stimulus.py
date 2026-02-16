from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class MediaType(str, Enum):
    """
    High-level media category for behavior weighting and feed semantics.

    Matches the design in project.md (news/social_post/video/meme/longform/forum_thread).
    """
    NEWS = "news"
    SOCIAL_POST = "social_post"
    VIDEO = "video"
    MEME = "meme"
    LONGFORM = "longform"
    FORUM_THREAD = "forum_thread"
    UNKNOWN = "unknown"

    @classmethod
    def from_any(cls, value: Any) -> "MediaType":
        if value is None:
            return cls.UNKNOWN
        if isinstance(value, MediaType):
            return value
        if isinstance(value, str):
            v = value.strip().lower()
            for mt in cls:
                if mt.value == v:
                    return mt
        return cls.UNKNOWN


@dataclass
class Stimulus:
    """
    A generic container for a piece of external data injected into the world.

    Backward compatible with the original fields:
      - id, source, tick, content_text, metadata

    New capability:
      - media_type: used for consumption vs interaction weighting
      - creator_id / outlet_id / community_id: supports subscription targeting
      - topic_hint: optional explicit topic string (still mirrors metadata["topic"])
    """

    # --- legacy / required ---
    id: str
    source: str  # e.g., "NewsOutletX", "SocialMediaFeedY", or creator/outlet identifier
    tick: int
    content_text: str

    # --- new / optional (safe defaults) ---
    media_type: MediaType = MediaType.UNKNOWN
    creator_id: Optional[str] = None
    outlet_id: Optional[str] = None
    community_id: Optional[str] = None
    topic_hint: Optional[str] = None
    stance_hint: Optional[float] = None

    # freeform extensibility
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Allow media_type to come from metadata or be passed as a string.
        if self.media_type is None or not isinstance(self.media_type, MediaType):
            self.media_type = MediaType.from_any(
                self.media_type if self.media_type is not None else self.metadata.get("media_type")
            )

        # If topic_hint wasn't provided, mirror from metadata (or vice versa).
        if self.topic_hint is None:
            t = self.metadata.get("topic")
            if isinstance(t, str):
                t = t.strip() or None
            self.topic_hint = t
        else:
            # normalize and keep metadata in sync
            if isinstance(self.topic_hint, str):
                self.topic_hint = self.topic_hint.strip() or None
            self.metadata.setdefault("topic", self.topic_hint)

        # If stance_hint wasn't provided, mirror from metadata
        if self.stance_hint is None:
            s = self.metadata.get("stance")
            try:
                self.stance_hint = float(s) if s is not None else None
            except Exception:
                self.stance_hint = None
        else:
            try:
                self.stance_hint = float(self.stance_hint)
            except Exception:
                self.stance_hint = None
        if self.stance_hint is not None:
            self.metadata.setdefault("stance", self.stance_hint)

        # Subscription-related IDs can live in metadata too (keeps CSV simple).
        if self.creator_id is None:
            v = self.metadata.get("creator_id")
            self.creator_id = v.strip() if isinstance(v, str) and v.strip() else None

        if self.outlet_id is None:
            v = self.metadata.get("outlet_id")
            self.outlet_id = v.strip() if isinstance(v, str) and v.strip() else None

        if self.community_id is None:
            v = self.metadata.get("community_id")
            self.community_id = v.strip() if isinstance(v, str) and v.strip() else None

        # If the source looks like a publisher and we have no explicit creator/outlet,
        # treat source as a generic "actor id" but don't override explicit fields.
        self.metadata.setdefault("source", self.source)

    @property
    def topic(self) -> Optional[str]:
        """Canonical topic accessor (preferred over direct metadata lookups)."""
        return self.topic_hint

    def to_debug_dict(self) -> Dict[str, Any]:
        """Helpful for logging/analytics without dumping huge metadata."""
        return {
            "id": self.id,
            "tick": self.tick,
            "source": self.source,
            "media_type": self.media_type.value if isinstance(self.media_type, MediaType) else str(self.media_type),
            "creator_id": self.creator_id,
            "outlet_id": self.outlet_id,
            "community_id": self.community_id,
            "topic": self.topic,
        }

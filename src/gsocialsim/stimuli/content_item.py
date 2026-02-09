from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from gsocialsim.types import ContentId, ActorId, TopicId
from gsocialsim.stimuli.stimulus import MediaType


@dataclass
class ContentItem:
    """
    A representation of a piece of content an agent can perceive.

    Backward compatible with the original minimal fields:
      - id, author_id, topic, stance, is_identity_threatening

    New capability:
      - media_type: used for consume vs interact weighting
      - outlet_id/community_id: supports subscription targeting in future layers
      - provenance: optional metadata chain (stimulus id, transform chain, etc.)
    """
    id: ContentId
    author_id: ActorId
    topic: TopicId
    stance: float  # [-1.0, +1.0]
    is_identity_threatening: bool = False

    # --- new / optional (safe defaults) ---
    media_type: MediaType = MediaType.UNKNOWN
    outlet_id: Optional[str] = None
    community_id: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)

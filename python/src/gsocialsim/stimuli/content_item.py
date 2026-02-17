from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

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
      - content_text: optional raw text (for identity threat checks)
      - identity_threat: optional precomputed threat signal [0,1]
      - primal_triggers: optional neuromarketing-style triggers
      - primal_intensity: optional intensity [0,1]
    """
    id: ContentId
    author_id: ActorId
    topic: TopicId
    stance: float  # [-1.0, +1.0]
    is_identity_threatening: bool = False

    # --- new / optional (safe defaults) ---
    content_text: Optional[str] = None
    identity_threat: Optional[float] = None
    primal_triggers: List[str] = field(default_factory=list)
    primal_intensity: Optional[float] = None
    media_type: MediaType = MediaType.UNKNOWN
    outlet_id: Optional[str] = None
    community_id: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)

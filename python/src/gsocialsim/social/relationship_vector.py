from dataclasses import dataclass, field
from typing import Dict
from gsocialsim.types import TopicId

@dataclass
class RelationshipVector:
    """
    Represents the latent social relationship between two agents.
    For Phase 3, we only focus on 'trust'. Other fields are placeholders.
    """
    affinity: float = 0.5
    trust: float = 0.5  # [0,1] - The most important factor for Phase 3
    intimacy: float = 0.5
    conflict: float = 0.0
    reciprocity: float = 0.5
    status_delta: float = 0.0
    topic_alignment: Dict[TopicId, float] = field(default_factory=dict)

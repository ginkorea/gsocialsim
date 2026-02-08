from enum import Enum
from dataclasses import dataclass
from typing import Optional

from gsocialsim.types import ContentId, TopicId

class IntakeMode(Enum):
    """ How an agent perceived a piece of content. """
    SCROLL = "scroll" # Passive, feed-driven
    SEEK = "seek"     # Active, goal-directed
    PHYSICAL = "physical" # Offline interaction
    DEEP_FOCUS = "deep_focus" # Focused, expensive processing

@dataclass
class Impression:
    """
    A richer representation of an agent's internal reaction to a ContentItem/Stimulus.
    """
    intake_mode: IntakeMode
    content_id: ContentId
    topic: TopicId
    stance_signal: float
    emotional_valence: float = 0.0 # Perceived emotional tone [-1, 1]
    arousal: float = 0.0         # Perceived intensity [0, 1]
    credibility_signal: float = 0.5 # Perceived credibility [0, 1]
    identity_threat: float = 0.0 # Perceived threat to identity [0, 1]
    social_proof: float = 0.0    # Perceived social proof (e.g., likes/forwards from others) [0, 1]
    relationship_strength_source: float = 0.0 # Relationship strength of the source [0, 1]
from dataclasses import dataclass
from enum import Enum
from src.gsocialsim.types import ContentId, TopicId

class IntakeMode(Enum):
    """ How an agent perceived a piece of content. """
    SCROLL = "scroll" # Passive, feed-driven
    SEEK = "seek"     # Active, goal-directed
    PHYSICAL = "physical" # Offline interaction

@dataclass
class Impression:
    """
    A minimal representation of an agent's internal reaction to a ContentItem.
    For Phase 2, this is very simple. It will be expanded later.
    """
    intake_mode: IntakeMode
    content_id: ContentId
    topic: TopicId
    stance_signal: float # The perceived stance from the content

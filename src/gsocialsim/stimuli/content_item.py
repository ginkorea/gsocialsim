from dataclasses import dataclass
from typing import Optional

from gsocialsim.types import ContentId, ActorId, TopicId

@dataclass
class ContentItem:
    """
    A minimal representation of a piece of content an agent can perceive.
    """
    id: ContentId
    author_id: ActorId
    topic: TopicId
    stance: float # A value from -1.0 to 1.0 representing the content's position
    is_identity_threatening: bool = False

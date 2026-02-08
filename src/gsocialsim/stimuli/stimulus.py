from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Stimulus:
    """ A generic container for a piece of external data injected into the world. """
    id: str
    source: str  # e.g., "NewsOutletX", "SocialMediaFeedY"
    tick: int
    content_text: str
    metadata: Dict = field(default_factory=dict)

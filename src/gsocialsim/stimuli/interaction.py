from enum import Enum
from dataclasses import dataclass
from typing import Optional

@dataclass
class Interaction:
    """ Represents an agent's action, either creating original content or acting on a stimulus. """
    agent_id: str
    verb: "InteractionVerb"
    target_stimulus_id: Optional[str] = None
    original_content: Optional["ContentItem"] = None # Used for CREATE verb

class InteractionVerb(Enum):
    CREATE = "create"   # Original post
    LIKE = "like"
    FORWARD = "forward"
    COMMENT = "comment"
    REPLY = "reply"

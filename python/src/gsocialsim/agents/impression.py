from enum import Enum
from dataclasses import dataclass
from typing import Optional

from gsocialsim.types import ContentId, TopicId
from gsocialsim.stimuli.stimulus import MediaType


class IntakeMode(Enum):
    """How an agent perceived a piece of content."""
    SCROLL = "scroll"         # Passive, feed-driven
    SEEK = "seek"             # Active, goal-directed
    PHYSICAL = "physical"     # Offline interaction
    DEEP_FOCUS = "deep_focus" # Focused, expensive processing


@dataclass
class Impression:
    """
    A richer representation of an agent's internal reaction to a ContentItem/Stimulus.

    Backward compatible: existing constructors that pass only the original fields still work.
    New fields (safe defaults):
      - media_type
      - consumed_prob / interact_prob (separate knobs)
    """
    intake_mode: IntakeMode
    content_id: ContentId
    topic: TopicId
    stance_signal: float

    # Existing fields
    emotional_valence: float = 0.0          # Perceived emotional tone [-1, 1]
    arousal: float = 0.0                    # Perceived intensity [0, 1]
    credibility_signal: float = 0.5         # Perceived credibility [0, 1]
    identity_threat: float = 0.0            # Perceived threat to identity [0, 1]
    social_proof: float = 0.0               # Social proof (likes/forwards) [0, 1]
    relationship_strength_source: float = 0.0  # Relationship strength to source [0, 1]

    # New fields for subscriptions/media weighting phase
    media_type: MediaType = MediaType.UNKNOWN
    consumed_prob: float = 1.0              # Probability agent actually consumes (reads/watches)
    interact_prob: float = 0.0              # Probability agent interacts (like/comment/reshare/reply)
    primal_activation: float = 0.0          # Neuromarketing-style activation [0,1]

    def clamp(self) -> None:
        """Keep probabilities and bounded signals sane."""
        self.arousal = max(0.0, min(1.0, self.arousal))
        self.credibility_signal = max(0.0, min(1.0, self.credibility_signal))
        self.identity_threat = max(0.0, min(1.0, self.identity_threat))
        self.social_proof = max(0.0, min(1.0, self.social_proof))
        self.relationship_strength_source = max(0.0, min(1.0, self.relationship_strength_source))
        self.consumed_prob = max(0.0, min(1.0, self.consumed_prob))
        self.interact_prob = max(0.0, min(1.0, self.interact_prob))
        self.primal_activation = max(0.0, min(1.0, self.primal_activation))

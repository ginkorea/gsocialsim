from dataclasses import dataclass

@dataclass
class EmotionState:
    valence: float = 0.0
    arousal: float = 0.0
    anger: float = 0.0  # Optional, but included for completeness
    anxiety: float = 0.0 # Optional, but included for completeness

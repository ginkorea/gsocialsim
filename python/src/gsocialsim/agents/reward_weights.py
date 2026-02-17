from dataclasses import dataclass

@dataclass
class RewardWeights:
    status: float = 1.0
    affiliation: float = 1.0
    dominance: float = 1.0
    coherence: float = 1.0
    novelty: float = 1.0
    safety: float = 1.0
    effort_cost: float = -1.0  # Negative weight

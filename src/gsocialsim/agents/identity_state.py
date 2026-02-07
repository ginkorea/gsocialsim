from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class IdentityState:
    identity_vector: List[float] = field(default_factory=lambda: [0.0] * 8) # 8-16 dimensions
    identity_rigidity: float = 0.5  # [0,1]
    ingroup_labels: Set[str] = field(default_factory=set)
    taboo_boundaries: Set[str] = field(default_factory=set)

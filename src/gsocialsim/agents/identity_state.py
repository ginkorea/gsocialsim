from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class IdentityState:
    identity_vector: List[float] = field(default_factory=lambda: [0.0] * 8)
    identity_rigidity: float = 0.5
    ingroup_labels: Set[str] = field(default_factory=set)
    taboo_boundaries: Set[str] = field(default_factory=set)

    def is_threatening(self, content_text: str) -> bool:
        """ A simple check to see if content text contains taboo keywords. """
        if not content_text:
            return False
        # A more complex model could use an LLM for this check.
        # For now, we use a simple keyword search.
        for taboo in self.taboo_boundaries:
            if taboo in content_text.lower():
                return True
        return False

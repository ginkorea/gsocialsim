from dataclasses import dataclass
from enum import Enum
import random

class BudgetKind(Enum):
    ATTENTION = "attention_minutes"
    ACTION = "action_budget"
    DEEP_FOCUS = "deep_focus_budget"
    RISK = "risk_budget"

@dataclass
class BudgetState:
    attention_minutes: float = 0.0
    action_budget: float = 0.0
    deep_focus_budget: float = 0.0
    risk_budget: float = 0.0
    _rng: random.Random = None

    def regen_daily(self):
        if self._rng is None: raise ValueError("RNG not set for BudgetState.")
        self.attention_minutes = max(0, self._rng.gauss(60, 30))
        self.action_budget = max(0, self._rng.gauss(10, 5))
        self.deep_focus_budget = max(0, self._rng.betavariate(2, 5) * 5) # Skewed towards lower deep focus
        self.risk_budget = max(0, self._rng.uniform(0, 1))

    def spend(self, kind: BudgetKind, amount: float) -> bool:
        if kind == BudgetKind.ATTENTION:
            if self.attention_minutes >= amount:
                self.attention_minutes -= amount
                return True
        elif kind == BudgetKind.ACTION:
            if self.action_budget >= amount:
                self.action_budget -= amount
                return True
        elif kind == BudgetKind.DEEP_FOCUS:
            if self.deep_focus_budget >= amount:
                self.deep_focus_budget -= amount
                return True
        elif kind == BudgetKind.RISK:
            # Risk budget might be more complex, e.g., a threshold
            # For now, just a simple spend check
            if self.risk_budget >= amount:
                self.risk_budget -= amount
                return True
        return False

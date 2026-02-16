from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random


class BudgetKind(Enum):
    ATTENTION = "attention_minutes"
    ACTION = "action_budget"
    DEEP_FOCUS = "deep_focus_budget"
    RISK = "risk_budget"


@dataclass
class BudgetState:
    """
    Contract-aligned budget model.

    Key idea:
      - regen_daily() seeds "banks" (daily totals)
      - reset_for_tick() allocates per-tick allowances from the banks
      - spend() spends from the per-tick allowance and from the bank

    Compatibility:
      - Existing code reads:
          attention_minutes, action_budget, deep_focus_budget, risk_budget
      - Existing code calls:
          spend(kind, amount) and regen_daily()
      - Kernel calls:
          reset_for_tick() / reset_tick() / reset()
    """

    # Per-tick allowances (what agents can spend within the current tick)
    attention_minutes: float = 0.0
    action_budget: float = 0.0
    deep_focus_budget: float = 0.0
    risk_budget: float = 0.0

    # Daily banks (total budget remaining for the day)
    attention_bank_minutes: float = 0.0
    action_bank: float = 0.0
    deep_focus_bank: float = 0.0
    risk_bank: float = 0.0

    # Tick parameters
    minutes_per_tick: float = 15.0
    max_actions_per_tick: float = 1.0
    max_deep_focus_per_tick: float = 1.0

    _rng: random.Random = field(default=None, repr=False)

    def regen_daily(self):
        """
        Seed daily banks.
        These distributions are intentionally simple and deterministic given RNG.
        """
        if self._rng is None:
            raise ValueError("RNG not set for BudgetState.")

        # Daily attention minutes (mean 60, stdev 30), clamp at 0
        self.attention_bank_minutes = max(0.0, float(self._rng.gauss(60, 30)))

        # Daily actions (mean 10, stdev 5), clamp at 0
        self.action_bank = max(0.0, float(self._rng.gauss(10, 5)))

        # Daily deep focus tokens: skew low (0..5)
        self.deep_focus_bank = max(0.0, float(self._rng.betavariate(2, 5) * 5))

        # Daily risk budget (0..1)
        self.risk_bank = max(0.0, float(self._rng.uniform(0, 1)))

        # After daily regen, immediately allocate for the next tick
        self.reset_for_tick()

    # Kernel compatibility: it probes reset_for_tick/reset_tick/reset
    def reset_for_tick(self):
        """
        Allocate per-tick allowances from the daily banks.

        Contract: one tick is 15 minutes.
        """
        # Attention: cannot exceed both remaining bank and minutes_per_tick
        self.attention_minutes = min(self.attention_bank_minutes, float(self.minutes_per_tick))

        # Actions: cap actions per tick (default 1), also cannot exceed bank
        self.action_budget = min(self.action_bank, float(self.max_actions_per_tick))

        # Deep focus: cap per tick (default 1), cannot exceed bank
        self.deep_focus_budget = min(self.deep_focus_bank, float(self.max_deep_focus_per_tick))

        # Risk: keep simple for now; allow spending any remaining risk this tick
        self.risk_budget = float(self.risk_bank)

    def reset_tick(self):
        self.reset_for_tick()

    def reset(self):
        self.reset_for_tick()

    def spend(self, kind: BudgetKind, amount: float) -> bool:
        """
        Spend from both per-tick allowance and daily bank.
        Returns True if successful.
        """
        amt = float(amount)

        if kind == BudgetKind.ATTENTION:
            if self.attention_minutes >= amt and self.attention_bank_minutes >= amt:
                self.attention_minutes -= amt
                self.attention_bank_minutes -= amt
                return True

        elif kind == BudgetKind.ACTION:
            if self.action_budget >= amt and self.action_bank >= amt:
                self.action_budget -= amt
                self.action_bank -= amt
                return True

        elif kind == BudgetKind.DEEP_FOCUS:
            if self.deep_focus_budget >= amt and self.deep_focus_bank >= amt:
                self.deep_focus_budget -= amt
                self.deep_focus_bank -= amt
                return True

        elif kind == BudgetKind.RISK:
            if self.risk_budget >= amt and self.risk_bank >= amt:
                self.risk_budget -= amt
                self.risk_bank -= amt
                return True

        return False

"""
models/trap.py
--------------
Trap entity. Stepping on an un-triggered trap applies a score penalty
and (per the Bayesian model) has a probability of activating rather
than being guaranteed, to introduce genuine uncertainty into planning.
"""

from __future__ import annotations
from dataclasses import dataclass
import random

from config import TRAP_PENALTY


@dataclass
class Trap:
    blocks_movement: bool = False
    activation_probability: float = 0.75
    triggered: bool = False

    def trigger(self, rng: random.Random = None) -> int:
        """Returns the score penalty applied (0 if the trap fails to
        activate — traps are probabilistic, not deterministic)."""
        rng = rng or random
        if rng.random() <= self.activation_probability:
            self.triggered = True
            return TRAP_PENALTY
        return 0

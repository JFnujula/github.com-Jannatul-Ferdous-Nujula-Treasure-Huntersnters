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
        rng = rng or random
        if rng.random() <= self.activation_probability:
            self.triggered = True
            return TRAP_PENALTY
        return 0

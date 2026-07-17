"""
models/powerup.py
------------------
Power-up entity. Grants a random beneficial effect when collected.
Kept intentionally simple (an enum-like `kind` + apply hook) so
students can add new effects without touching Player logic elsewhere.
"""

from __future__ import annotations
from dataclasses import dataclass
import random

from config import POWERUP_BONUS

POWERUP_KINDS = ("speed_boost", "shield", "score_bonus", "reveal_map")


@dataclass
class PowerUp:
    blocks_movement: bool = False
    kind: str = None

    def __post_init__(self):
        if self.kind is None:
            self.kind = random.choice(POWERUP_KINDS)

    def collect_bonus(self) -> int:
        """Base score bonus simply for picking one up; the specific
        effect (speed_boost, shield, etc.) is applied by Player.apply_powerup."""
        return POWERUP_BONUS

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
        return POWERUP_BONUS

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Treasure:
    value: int = 50
    blocks_movement: bool = False  # treasures sit on open ground
    collected: bool = False

    def collect(self) -> int:
        self.collected = True
        return self.value

"""
models/door.py
--------------
Locked door. Blocks movement until a player spends an "open door"
action on it. Doors are a clean example of state that changes the
walkability of a tile mid-game, which search algorithms must account
for by re-planning rather than caching paths forever.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Door:
    locked: bool = True

    @property
    def blocks_movement(self) -> bool:
        return self.locked

    def open(self) -> bool:
        """Attempt to open the door. Returns True if it changed state."""
        if self.locked:
            self.locked = False
            return True
        return False

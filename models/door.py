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

"""
models/tile.py
--------------
A single cell on the game board.

Each Tile stores its terrain (which determines movement cost and
walkability) plus an optional "occupant" — a Treasure, Trap, Door or
PowerUp object living on that cell. Keeping terrain and occupant
separate (composition) lets a tile be, for example, "mud with a trap
on it" without needing a combinatorial explosion of tile subclasses.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any

from config import TerrainType, TERRAIN_COST, TERRAIN_WALKABLE


@dataclass
class Tile:
    row: int
    col: int
    terrain: TerrainType = TerrainType.GRASS

    # A Treasure / Trap / Door / PowerUp instance, or None if empty.
    occupant: Optional[Any] = None

    # Temporary obstacles placed by the human player expire after N turns.
    temp_obstacle_turns_left: int = 0

    @property
    def cost(self) -> float:
        """Movement cost to enter this tile (used by UCS / A*)."""
        return TERRAIN_COST[self.terrain]

    @property
    def is_walkable(self) -> bool:
        if self.temp_obstacle_turns_left > 0:
            return False
        if not TERRAIN_WALKABLE[self.terrain]:
            return False
        # A closed, locked door blocks the tile until opened.
        occ = self.occupant
        if occ is not None and getattr(occ, "blocks_movement", False):
            return False
        return True

    def place_temp_obstacle(self, turns: int = 3) -> None:
        """Human-player action: temporarily block this tile."""
        self.temp_obstacle_turns_left = max(self.temp_obstacle_turns_left, turns)

    def tick(self) -> None:
        """Called once per turn to decay temporary effects."""
        if self.temp_obstacle_turns_left > 0:
            self.temp_obstacle_turns_left -= 1

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        occ = type(self.occupant).__name__ if self.occupant else "empty"
        return f"Tile({self.row},{self.col},{self.terrain.value},{occ})"

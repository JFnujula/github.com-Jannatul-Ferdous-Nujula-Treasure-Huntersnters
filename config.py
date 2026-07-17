"""
config.py
---------
Central configuration for AI Treasure Hunters.

Keeping every tunable constant in one place makes the game easy for
students to modify (e.g. change grid size, tile costs, colors) without
hunting through gameplay code.
"""

from pathlib import Path
from enum import Enum, auto


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"
SAVES_DIR = PROJECT_ROOT / "saves"
SAVES_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Difficulty -> grid size
# ---------------------------------------------------------------------------
class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


GRID_SIZES = {
    Difficulty.EASY: (10, 10),
    Difficulty.MEDIUM: (15, 15),
    Difficulty.HARD: (20, 20),
}

# Number of AI search "plies" (moves ahead) Minimax/DLS look by difficulty.
SEARCH_DEPTH = {
    Difficulty.EASY: 2,
    Difficulty.MEDIUM: 4,
    Difficulty.HARD: 6,
}


# ---------------------------------------------------------------------------
# Terrain costs (used by UCS / A* / Q-learning reward shaping)
# ---------------------------------------------------------------------------
class TerrainType(Enum):
    GRASS = "grass"
    MUD = "mud"
    WATER = "water"
    WALL = "wall"  # not walkable


TERRAIN_COST = {
    TerrainType.GRASS: 1,
    TerrainType.MUD: 3,
    TerrainType.WATER: 4,
    TerrainType.WALL: float("inf"),
}

TERRAIN_WALKABLE = {
    TerrainType.GRASS: True,
    TerrainType.MUD: True,
    TerrainType.WATER: True,
    TerrainType.WALL: False,
}


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
TREASURE_BASE_VALUE = 50
TRAP_PENALTY = -20
POWERUP_BONUS = 10
STRATEGIC_BONUS = 15  # e.g. blocking opponent from a treasure

# ---------------------------------------------------------------------------
# Turn / game limits
# ---------------------------------------------------------------------------
MAX_TURNS = 200

# ---------------------------------------------------------------------------
# Rendering (Pygame)
# ---------------------------------------------------------------------------
TILE_PIXELS = 40
FPS = 60

COLOR_BG = (18, 18, 24)
COLOR_GRID_LINE = (50, 50, 60)

COLOR_TERRAIN = {
    TerrainType.GRASS: (58, 92, 58),
    TerrainType.MUD: (92, 70, 42),
    TerrainType.WATER: (40, 70, 110),
    TerrainType.WALL: (30, 30, 34),
}

COLOR_TREASURE = (255, 205, 60)
COLOR_TRAP = (200, 50, 50)
COLOR_DOOR = (140, 100, 200)
COLOR_POWERUP = (60, 200, 180)

COLOR_HUMAN = (70, 140, 255)
COLOR_AI = (255, 90, 90)

COLOR_TEXT = (230, 230, 235)

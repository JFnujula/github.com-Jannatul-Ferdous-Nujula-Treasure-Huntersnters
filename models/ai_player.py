from __future__ import annotations
from typing import Optional, Tuple, List

from models.player import Player, ActionResult
from models.board import Board
from ai.astar import AStar
from ai.bfs import BFS

Coord = Tuple[int, int]


class AIPlayer(Player):
    def __init__(self, name: str, start: Coord, color=(255, 90, 90), heuristic: str = "manhattan"):
        super().__init__(name, start, color)
        self.pathfinder = AStar(heuristic=heuristic)
        self.fallback = BFS()
        self.current_path: List[Coord] = []
        self.last_search_result = None  # exposed for the AI visualizer panel

    def choose_target(self, board: Board) -> Optional[Coord]:
        """Pick the nearest treasure by search cost. Returns None if no
        treasures remain or none are reachable."""
        treasures = board.treasures()
        if not treasures:
            return None

        best_target, best_result = None, None
        for t in treasures:
            result = self.pathfinder.search(board, self.position, t)
            if result.found and (best_result is None or result.cost < best_result.cost):
                best_target, best_result = t, result

        self.last_search_result = best_result
        return best_target

    def take_turn(self, board: Board) -> ActionResult:
        """Decide and execute one action for this turn. Returns the
        ActionResult so Game can log/score it uniformly with the human
        player's actions."""
        target = self.choose_target(board)
        if target is None:
            return ActionResult(False, f"{self.name} has no reachable treasures.")

        result = self.pathfinder.search(board, self.position, target)
        self.last_search_result = result
        if not result.found or len(result.path) < 2:
            return ActionResult(False, f"{self.name} could not find a path to {target}.")

        next_step = result.path[1]  # path[0] is current position
        return self.move(board, next_step)

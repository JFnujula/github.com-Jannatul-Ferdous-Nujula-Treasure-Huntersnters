"""
main.py
-------
Phase 1 entry point: a playable Pygame rendering of the core game
loop (board, human movement via arrow keys, AI turn via A*/BFS
chasing the nearest treasure). This is intentionally the *minimal*
runnable slice — the PySide6 menu/dashboard shell, Minimax/Alpha-Beta,
Bayesian reasoning, Q-learning, and ANN modules layer on top of this
same Game/Board/Player core in later phases without needing to change
it.

Controls
--------
Arrow keys : move the human player
D          : place a temporary obstacle one tile in front (down)
SPACE      : let the AI take its turn immediately (auto-plays otherwise)
R          : restart with a new random board
ESC / close window : quit

Run:
    pip install -r requirements.txt
    python main.py
"""

from __future__ import annotations
import sys

import pygame

from config import (
    Difficulty, TILE_PIXELS, FPS, COLOR_BG, COLOR_GRID_LINE, COLOR_TERRAIN,
    COLOR_TREASURE, COLOR_TRAP, COLOR_DOOR, COLOR_POWERUP, COLOR_TEXT,
)
from models.game import Game
from models.treasure import Treasure
from models.trap import Trap
from models.door import Door
from models.powerup import PowerUp

SIDEBAR_WIDTH = 260


class GameApp:
    def __init__(self, difficulty: Difficulty = Difficulty.EASY):
        pygame.init()
        pygame.display.set_caption("AI Treasure Hunters")

        self.difficulty = difficulty
        self.game = Game(difficulty=difficulty)

        board_w = self.game.board.cols * TILE_PIXELS
        board_h = self.game.board.rows * TILE_PIXELS
        self.screen = pygame.display.set_mode((board_w + SIDEBAR_WIDTH, board_h))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)
        self.big_font = pygame.font.SysFont("consolas", 22, bold=True)

        self.ai_move_delay_ms = 350
        self._ai_timer = 0

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if not self.game.current_player_is_human or self.game.game_over:
            if event.key == pygame.K_r:
                self.game = Game(difficulty=self.difficulty)
            return

        r, c = self.game.human.position
        target = None
        if event.key in (pygame.K_UP, pygame.K_w):
            target = (r - 1, c)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            target = (r + 1, c)
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            target = (r, c - 1)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            target = (r, c + 1)
        elif event.key == pygame.K_r:
            self.game = Game(difficulty=self.difficulty)
            return

        if target is not None:
            self.game.human_action("move", target=target)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt_ms: int) -> None:
        if self.game.game_over:
            return
        if not self.game.current_player_is_human:
            self._ai_timer += dt_ms
            if self._ai_timer >= self.ai_move_delay_ms:
                self._ai_timer = 0
                self.game.ai_take_turn()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw_board(self) -> None:
        board = self.game.board
        for r in range(board.rows):
            for c in range(board.cols):
                tile = board.get_tile(r, c)
                x, y = c * TILE_PIXELS, r * TILE_PIXELS
                color = COLOR_TERRAIN[tile.terrain]
                if tile.temp_obstacle_turns_left > 0:
                    color = (90, 30, 30)
                pygame.draw.rect(self.screen, color, (x, y, TILE_PIXELS, TILE_PIXELS))
                pygame.draw.rect(self.screen, COLOR_GRID_LINE, (x, y, TILE_PIXELS, TILE_PIXELS), 1)

                occ = tile.occupant
                cx, cy = x + TILE_PIXELS // 2, y + TILE_PIXELS // 2
                if isinstance(occ, Treasure) and not occ.collected:
                    pygame.draw.circle(self.screen, COLOR_TREASURE, (cx, cy), TILE_PIXELS // 3)
                elif isinstance(occ, Trap):
                    pygame.draw.polygon(
                        self.screen, COLOR_TRAP,
                        [(cx, y + 6), (x + 6, y + TILE_PIXELS - 6), (x + TILE_PIXELS - 6, y + TILE_PIXELS - 6)],
                    )
                elif isinstance(occ, Door):
                    color = COLOR_DOOR if occ.locked else (100, 200, 100)
                    pygame.draw.rect(self.screen, color, (x + 8, y + 4, TILE_PIXELS - 16, TILE_PIXELS - 8))
                elif isinstance(occ, PowerUp):
                    pygame.draw.circle(self.screen, COLOR_POWERUP, (cx, cy), TILE_PIXELS // 4, 3)

    def draw_players(self) -> None:
        for player, is_ai in ((self.game.human, False), (self.game.ai, True)):
            r, c = player.position
            cx = c * TILE_PIXELS + TILE_PIXELS // 2
            cy = r * TILE_PIXELS + TILE_PIXELS // 2
            radius = TILE_PIXELS // 2 - 4
            pygame.draw.circle(self.screen, player.color, (cx, cy), radius)
            label = "AI" if is_ai else "H"
            text = self.font.render(label, True, (10, 10, 10))
            self.screen.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))

    def draw_sidebar(self) -> None:
        board_w = self.game.board.cols * TILE_PIXELS
        x0 = board_w + 12
        pygame.draw.rect(self.screen, (24, 24, 30), (board_w, 0, SIDEBAR_WIDTH, self.screen.get_height()))

        lines = [
            "AI TREASURE HUNTERS",
            "",
            f"Turn: {self.game.turn_count}",
            f"Active: {'HUMAN' if self.game.current_player_is_human else 'AI'}",
            "",
            f"Human score: {self.game.human.score}",
            f"AI score:    {self.game.ai.score}",
            "",
            "Controls:",
            "Arrows: move",
            "R: restart",
            "",
        ]
        y = 16
        for i, line in enumerate(lines):
            font = self.big_font if i == 0 else self.font
            text = font.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (x0, y))
            y += text.get_height() + 6

        if self.game.ai.last_search_result:
            res = self.game.ai.last_search_result
            info_lines = [
                "AI Search Info:",
                f"Algo: {res.algorithm_name}",
                f"Expanded: {len(res.expanded_nodes)}",
                f"Path cost: {res.cost:.1f}",
                f"Time: {res.time_seconds * 1000:.2f} ms",
            ]
            for line in info_lines:
                text = self.font.render(line, True, (170, 200, 255))
                self.screen.blit(text, (x0, y))
                y += text.get_height() + 4

        if self.game.game_over:
            y += 10
            text = self.big_font.render(f"WINNER: {self.game.winner}", True, (255, 220, 90))
            self.screen.blit(text, (x0, y))
            y += text.get_height() + 6
            hint = self.font.render("Press R to play again", True, COLOR_TEXT)
            self.screen.blit(hint, (x0, y))

    def render(self) -> None:
        self.screen.fill(COLOR_BG)
        self.draw_board()
        self.draw_players()
        self.draw_sidebar()
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    self.handle_input(event)

            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    GameApp(difficulty=Difficulty.EASY).run()

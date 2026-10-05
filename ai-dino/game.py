# =============================================================
#  game.py  —  Main Game class: loop, update, draw
# =============================================================

import sys
import random
import pygame

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    BG_DAY, BG_NIGHT, FG_DAY, FG_NIGHT,
    GROUND_Y, INIT_SPEED, SPEED_INC, MAX_SPEED,
    SCORE_RATE, NIGHT_CYCLE, S,
)
from sprites import SpriteBank, GROUND_DOTS, GROUND_TEX_W, STARS
from dino import Dinosaur
from obstacle import spawn_obstacle
from cloud import Cloud


# ─────────────────────────────────────────────────────────────
#  Score font helpers
# ─────────────────────────────────────────────────────────────

def _load_font(size):
    """Load monospace font (fallback to system default)."""
    for name in ("Courier New", "Courier", "monospace", None):
        try:
            return pygame.font.SysFont(name, size, bold=True)
        except Exception:
            pass
    return pygame.font.Font(None, size)


# ─────────────────────────────────────────────────────────────
#  Game
# ─────────────────────────────────────────────────────────────

class Game:
    # ── Obstacle spawning ─────────────────────────────────────
    #   Gap is measured in "scrolled pixels" between spawns.
    #   At higher speeds it shrinks (harder), but has a minimum.
    BASE_MIN_GAP    = 500    # pixels at INIT_SPEED
    BASE_MAX_GAP    = 1100
    MIN_POSSIBLE_GAP = 260   # hard minimum (give player reaction time)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🦕  Chrome Dino")

        self.clock     = pygame.time.Clock()
        self.font_big  = _load_font(44)
        self.font_med  = _load_font(28)
        self.font_sml  = _load_font(22)

        self.sprites   = SpriteBank()
        self.dino      = Dinosaur(self.sprites)

        self.hi_score  = 0
        self._reset()

    # ── State reset ───────────────────────────────────────────

    def _reset(self):
        self.speed          = INIT_SPEED
        self.score          = 0.0
        self.night          = False
        self._night_cycle   = 0           # how many toggles so far
        self._scrolled      = 0.0         # total pixels scrolled (for gap)
        self._gap_target    = self._random_gap()

        self.obstacles      = []
        self.clouds         = [Cloud(self.sprites, offscreen=False) for _ in range(3)]

        self._ground_off    = 0.0         # ground texture scroll offset
        self._score_flash   = 0           # frames remaining for score flash
        self._prev_hundred  = 0

        self.running     = False   # True once player presses Start
        self.game_over   = False

        self.dino.reset()
        self._refresh_colors()

    def _random_gap(self):
        """Pixel gap for next obstacle, shrinks with speed."""
        ratio = INIT_SPEED / max(self.speed, INIT_SPEED)
        lo = max(int(self.BASE_MIN_GAP * ratio), self.MIN_POSSIBLE_GAP)
        hi = max(int(self.BASE_MAX_GAP * ratio), lo + 100)
        return random.randint(lo, hi)

    def _refresh_colors(self):
        fg = FG_NIGHT if self.night else FG_DAY
        bg = BG_NIGHT if self.night else BG_DAY
        self.sprites.set_colors(fg, bg)
        self._fg = fg
        self._bg = bg

    # ─────────────────────────────────────────────────────────
    #  Main loop
    # ─────────────────────────────────────────────────────────

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

    # ── Event handling ────────────────────────────────────────

    def _handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_SPACE, pygame.K_UP):
                    if self.game_over:
                        self._reset()
                    elif not self.running:
                        self.running = True
                    else:
                        self.dino.jump()

                elif ev.key == pygame.K_DOWN:
                    if self.running and not self.game_over:
                        self.dino.start_duck()

            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_DOWN:
                    self.dino.stop_duck()

    # ── Update ────────────────────────────────────────────────

    def _update(self):
        if not self.running or self.game_over:
            return

        # ── Speed ──────────────────────────────────────────────
        self.speed = min(self.speed + SPEED_INC, MAX_SPEED)

        # ── Score ──────────────────────────────────────────────
        prev_score = self.score
        self.score += self.speed * SCORE_RATE
        cur_hundred = int(self.score) // 100
        if cur_hundred > self._prev_hundred:
            self._prev_hundred = cur_hundred
            self._score_flash  = 36    # 36 frames ≈ 0.6 s of flashing

        if self._score_flash > 0:
            self._score_flash -= 1

        # ── Night / Day ────────────────────────────────────────
        new_cycle = int(self.score) // NIGHT_CYCLE
        if new_cycle > self._night_cycle:
            self._night_cycle = new_cycle
            self.night = not self.night
            self._refresh_colors()

        # ── Ground scroll ──────────────────────────────────────
        self._ground_off  = (self._ground_off + self.speed) % GROUND_TEX_W
        self._scrolled   += self.speed

        # ── Dino ───────────────────────────────────────────────
        self.dino.update()

        # ── Spawn obstacles ────────────────────────────────────
        if self._scrolled >= self._gap_target:
            self.obstacles.append(spawn_obstacle(self.sprites, self.score))
            self._scrolled   = 0.0
            self._gap_target = self._random_gap()

        # ── Update obstacles ───────────────────────────────────
        for obs in self.obstacles:
            obs.update(self.speed)
        self.obstacles = [o for o in self.obstacles if not o.dead]

        # ── Collision ──────────────────────────────────────────
        dr = self.dino.get_rect()
        for obs in self.obstacles:
            if dr.colliderect(obs.get_rect()):
                self.dino.die()
                self.game_over = True
                if self.score > self.hi_score:
                    self.hi_score = self.score
                return

        # ── Clouds ─────────────────────────────────────────────
        for c in self.clouds:
            c.update()
        self.clouds = [c for c in self.clouds if not c.dead]
        while len(self.clouds) < 4:
            self.clouds.append(Cloud(self.sprites, offscreen=True))

    # ─────────────────────────────────────────────────────────
    #  Draw
    # ─────────────────────────────────────────────────────────

    def _draw(self):
        fg, bg = self._fg, self._bg

        # ── Background ─────────────────────────────────────────
        self.screen.fill(bg)

        # ── Night extras: stars + moon ──────────────────────────
        if self.night:
            self._draw_night_sky(fg)

        # ── Clouds ─────────────────────────────────────────────
        for c in self.clouds:
            c.draw(self.screen)

        # ── Ground ─────────────────────────────────────────────
        self._draw_ground(fg)

        # ── Obstacles ──────────────────────────────────────────
        for obs in self.obstacles:
            obs.draw(self.screen)

        # ── Dino ───────────────────────────────────────────────
        self.dino.draw(self.screen)

        # ── HUD (score) ────────────────────────────────────────
        self._draw_hud(fg)

        # ── Overlays ───────────────────────────────────────────
        if not self.running and not self.game_over:
            self._draw_start(fg)
        elif self.game_over:
            self._draw_game_over(fg)

        pygame.display.flip()

    # ── Ground ────────────────────────────────────────────────

    def _draw_ground(self, fg):
        # Solid line
        pygame.draw.rect(self.screen, fg,
                         (0, GROUND_Y, SCREEN_WIDTH, S * 2))

        # Scrolling dot texture
        off = int(self._ground_off)
        for (tx, ty, tw, th) in GROUND_DOTS:
            sx = (tx - off) % GROUND_TEX_W
            if sx < SCREEN_WIDTH:
                pygame.draw.rect(self.screen, fg,
                                 (sx, GROUND_Y + ty, tw * S, th * S))
            # Wrap-around: same dot appearing again from the left
            sx2 = sx - GROUND_TEX_W
            if 0 <= sx2 + tw * S:
                pygame.draw.rect(self.screen, fg,
                                 (sx2, GROUND_Y + ty, tw * S, th * S))

    # ── Night sky ─────────────────────────────────────────────

    def _draw_night_sky(self, fg):
        # Stars
        for (sx, sy) in STARS:
            pygame.draw.rect(self.screen, fg, (sx, sy, S * 2, S * 2))

        # Crescent moon  (full circle minus offset circle)
        moon_x, moon_y, moon_r = 980, 60, 22
        pygame.draw.circle(self.screen, fg, (moon_x, moon_y), moon_r)
        # Bite out of the moon with background colour
        pygame.draw.circle(self.screen, self._bg,
                           (moon_x + 10, moon_y - 6), moon_r - 6)

    # ── HUD ───────────────────────────────────────────────────

    def _draw_hud(self, fg):
        score_int = int(self.score)
        hi_int    = int(self.hi_score)

        # Flash: hide score every other 6-frame window during flash
        if self._score_flash > 0 and (self._score_flash // 6) % 2 == 1:
            return

        hi_surf  = self.font_med.render(f"HI {hi_int:05d}", True, fg)
        cur_surf = self.font_med.render(f"{score_int:05d}", True, fg)

        gap = 16
        total_w = hi_surf.get_width() + gap + cur_surf.get_width()
        base_x  = SCREEN_WIDTH - total_w - 20

        self.screen.blit(hi_surf,  (base_x, 18))
        self.screen.blit(cur_surf, (base_x + hi_surf.get_width() + gap, 18))

    # ── Start screen ──────────────────────────────────────────

    def _draw_start(self, fg):
        self._draw_centered_text(
            self.font_sml,
            "Press  SPACE  or  ↑  to  start",
            SCREEN_HEIGHT // 2 - 10,
            fg,
        )

    # ── Game over screen ──────────────────────────────────────

    def _draw_game_over(self, fg):
        mid_y = SCREEN_HEIGHT // 2

        self._draw_centered_text(self.font_big, "G A M E  O V E R",
                                 mid_y - 52, fg)
        # Thin separator line
        line_w = 200
        pygame.draw.rect(self.screen, fg,
                         (SCREEN_WIDTH // 2 - line_w // 2,
                          mid_y - 12, line_w, S))

        self._draw_centered_text(self.font_sml,
                                 "Press  SPACE  or  ↑  to  restart",
                                 mid_y + 16, fg)

    # ── Utility ───────────────────────────────────────────────

    def _draw_centered_text(self, font, text, y, color):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))

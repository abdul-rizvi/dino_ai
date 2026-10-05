# =============================================================
#  obstacle.py  —  Cacti and Pterodactyl (Bird) obstacles
# =============================================================

import pygame
import random
from constants import SCREEN_WIDTH, GROUND_Y, S
from sprites import (
    SMALL_W, SMALL_H,
    LARGE_W, LARGE_H,
    BIRD_W,  BIRD_H,
)


# ─────────────────────────────────────────────────────────────
#  Bird flight heights  (y of top of sprite, at S=2 scale)
#
#  Calculations for reference (S=2, DINO_H=52, DUCK_H=38, BIRD_H=36):
#    Running dino top  = GROUND_Y − 104  = 211
#    Ducking dino top  = GROUND_Y − 76   = 239
#    Bird pixel height = 72
#
#  LOW  (248) → bottom 320: hits running AND ducking → must JUMP
#  MID  (155) → bottom 227: hits running (211<227✓), safe to duck (239>227✓)
#  HIGH ( 80) → bottom 152: clears running (211>152✓) → can RUN UNDER
# ─────────────────────────────────────────────────────────────

_BIRD_H_PX = BIRD_H * S                 # 72 px at S=2

BIRD_Y_LOW  = GROUND_Y - _BIRD_H_PX           # = 243  must jump
BIRD_Y_MID  = GROUND_Y - _BIRD_H_PX - 90      # = 153  must duck
BIRD_Y_HIGH = GROUND_Y - _BIRD_H_PX - 165     # =  78  run under

BIRD_HEIGHTS = [BIRD_Y_LOW, BIRD_Y_MID, BIRD_Y_HIGH]

# Weight probabilities: low/mid are "hard", high is "easy"
BIRD_HEIGHT_WEIGHTS = [3, 3, 1]

# Wing animation
WING_ANIM_SPEED = 8    # frames per wing-flap


# ─────────────────────────────────────────────────────────────
#  Base obstacle
# ─────────────────────────────────────────────────────────────

class Obstacle:
    def __init__(self, sprites):
        self.sprites = sprites
        self.x       = float(SCREEN_WIDTH + 60)
        self.dead    = False
        # Subclasses must set: self.image, self.width, self.height, self.y

    # ── update ───────────────────────────────────────────────

    def update(self, speed):
        self.x -= speed
        if self.x + self.width < -20:
            self.dead = True

    # ── draw ─────────────────────────────────────────────────

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

    # ── hitbox (slightly inset) ───────────────────────────────

    def get_rect(self):
        pad = 2 * S
        return pygame.Rect(
            int(self.x) + pad,
            int(self.y) + pad,
            self.width  - pad * 2,
            self.height - pad * 2,
        )


# ─────────────────────────────────────────────────────────────
#  Cactus  (5 varieties)
# ─────────────────────────────────────────────────────────────

_CACTUS_VARIANTS = [
    'small_1', 'small_1', 'small_1',   # bias toward single small
    'small_2', 'small_2',
    'small_3',
    'large_1', 'large_1',
    'large_2',
]


class Cactus(Obstacle):
    def __init__(self, sprites):
        super().__init__(sprites)
        kind = random.choice(_CACTUS_VARIANTS)
        self.image  = getattr(sprites, f'cactus_{kind}')
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
        self.y      = float(GROUND_Y - self.height)


# ─────────────────────────────────────────────────────────────
#  Bird (Pterodactyl)
# ─────────────────────────────────────────────────────────────

class Bird(Obstacle):
    def __init__(self, sprites):
        super().__init__(sprites)
        self.y       = float(random.choices(BIRD_HEIGHTS,
                                            weights=BIRD_HEIGHT_WEIGHTS)[0])
        self.width   = BIRD_W * S
        self.height  = BIRD_H * S
        self._frame  = 0
        self._frame_t = 0

    def update(self, speed):
        super().update(speed)
        self._frame_t += 1
        if self._frame_t >= WING_ANIM_SPEED:
            self._frame_t = 0
            self._frame   = 1 - self._frame

    def draw(self, screen):
        img = (self.sprites.bird_up
               if self._frame == 0
               else self.sprites.bird_down)
        screen.blit(img, (int(self.x), int(self.y)))

    # Bird.image not used (draw() overridden), but define for safety
    @property
    def image(self):
        return self.sprites.bird_up


# ─────────────────────────────────────────────────────────────
#  Factory
# ─────────────────────────────────────────────────────────────

def spawn_obstacle(sprites, score):
    """
    Return a new Cactus or Bird.
    Birds are rarer at the start; probability ramps up with score.
    """
    bird_prob = min(0.15 + score / 8000.0, 0.40)
    if random.random() < bird_prob:
        return Bird(sprites)
    return Cactus(sprites)

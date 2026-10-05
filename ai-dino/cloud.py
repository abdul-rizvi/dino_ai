# =============================================================
#  cloud.py  —  Background cloud with parallax scroll
# =============================================================

import random
from constants import SCREEN_WIDTH, S
from sprites import CLOUD_W, CLOUD_H


class Cloud:
    """
    Clouds scroll slower than the ground (parallax effect).
    Speed is independent of game speed to give visual depth.
    """

    MIN_SPEED = 1.5
    MAX_SPEED = 3.0
    MIN_Y     = 40
    MAX_Y     = 150

    def __init__(self, sprites, offscreen=True):
        self.sprites = sprites
        self.speed   = random.uniform(self.MIN_SPEED, self.MAX_SPEED)
        self.y       = random.randint(self.MIN_Y, self.MAX_Y)
        self.dead    = False

        # Spread initial clouds across the screen; new ones start off-screen
        if offscreen:
            self.x = float(SCREEN_WIDTH + random.randint(50, 400))
        else:
            self.x = float(random.randint(0, SCREEN_WIDTH))

    def update(self):
        self.x -= self.speed
        if self.x + CLOUD_W * S < 0:
            self.dead = True

    def draw(self, screen):
        screen.blit(self.sprites.cloud, (int(self.x), self.y))

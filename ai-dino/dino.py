# =============================================================
#  dino.py  —  Dinosaur player character
# =============================================================

import pygame
from constants import (
    GROUND_Y, DINO_X, GRAVITY, JUMP_VEL, DUCK_BOOST, S
)
from sprites import DINO_W, DINO_H, DUCK_W, DUCK_H


class Dinosaur:
    """
    The T-Rex player.

    State machine:
        running → jump()  → jumping → (lands) → running
        running → duck()  → ducking → unduck() → running
        any     → die()   → dead

    Inputs fed to the AI neural network come from properties
    exposed by this class (y, vel_y, is_jumping, is_ducking).
    """

    ANIM_SPEED = 5     # frames between leg-animation ticks

    def __init__(self, sprites):
        self.sprites  = sprites
        self.x        = DINO_X
        self.y        = float(GROUND_Y - DINO_H * S)
        self.vel_y    = 0.0
        self.jumping  = False
        self.ducking  = False
        self.dead     = False
        self._frame   = 0     # 0 or 1  (which leg frame)
        self._frame_t = 0     # timer counter

    # ── public geometry ──────────────────────────────────────

    @property
    def ground_y(self):
        """Top-of-dino y when standing on the ground."""
        h = DUCK_H if self.ducking else DINO_H
        return float(GROUND_Y - h * S)

    @property
    def width(self):
        return (DUCK_W if self.ducking else DINO_W) * S

    @property
    def height(self):
        return (DUCK_H if self.ducking else DINO_H) * S

    # ── actions ──────────────────────────────────────────────

    def jump(self):
        """Called when SPACE / UP is pressed."""
        if not self.jumping and not self.dead:
            self.vel_y   = JUMP_VEL
            self.jumping = True
            self.ducking = False

    def start_duck(self):
        """Called while DOWN is held."""
        if not self.dead:
            if self.jumping:
                # Fast-fall when ducking mid-air
                self.vel_y += DUCK_BOOST * 8
            self.ducking = True

    def stop_duck(self):
        if not self.dead:
            self.ducking = False

    def die(self):
        self.dead = True

    def reset(self):
        self.y        = float(GROUND_Y - DINO_H * S)
        self.vel_y    = 0.0
        self.jumping  = False
        self.ducking  = False
        self.dead     = False
        self._frame   = 0
        self._frame_t = 0

    # ── update ───────────────────────────────────────────────

    def update(self):
        if self.dead:
            return

        # ── Physics ──────────────────────────────────────────
        self.vel_y += GRAVITY
        if self.ducking and self.jumping:
            self.vel_y += DUCK_BOOST       # extra fall when ducking in air
        self.y += self.vel_y

        # ── Land ─────────────────────────────────────────────
        ground = self.ground_y
        if self.y >= ground:
            self.y       = ground
            self.vel_y   = 0.0
            self.jumping = False

        # ── Animate legs ─────────────────────────────────────
        self._frame_t += 1
        if self._frame_t >= self.ANIM_SPEED:
            self._frame_t = 0
            self._frame   = 1 - self._frame

    # ── draw ─────────────────────────────────────────────────

    def draw(self, screen):
        sp = self.sprites
        if self.dead:
            img = sp.dino_dead
        elif self.ducking:
            img = sp.duck0 if self._frame == 0 else sp.duck1
        elif self.jumping:
            img = sp.dino_jump
        else:
            img = sp.dino_run0 if self._frame == 0 else sp.dino_run1

        screen.blit(img, (self.x, int(self.y)))

    # ── collision rect (slightly inset for fairness) ─────────

    def get_rect(self):
        pad_x = 8 * S // 2
        pad_y = 6 * S // 2
        return pygame.Rect(
            self.x + pad_x,
            int(self.y) + pad_y,
            self.width  - pad_x * 2,
            self.height - pad_y * 2,
        )

    # ── AI-readable sensor values (normalised 0-1) ────────────

    @property
    def sensor_y(self):
        """Vertical position: 0 = on ground, 1 = max jump height."""
        max_height = (JUMP_VEL ** 2) / (2 * GRAVITY)
        dist_from_ground = self.ground_y - self.y
        return min(dist_from_ground / max_height, 1.0)

    @property
    def sensor_vel_y(self):
        """Normalised vertical velocity: -1 = rising, +1 = falling."""
        return self.vel_y / abs(JUMP_VEL)

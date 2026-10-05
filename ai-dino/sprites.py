# =============================================================
#  sprites.py  —  Build every pre-rendered pygame.Surface
# =============================================================
#
#  All pixel-art shapes are defined at 1× scale (matching the
#  original Chrome Dino pixel grid).  Multiply by S at render
#  time so the game looks sharp at any scale factor.
#
#  Colour convention inside rect lists:
#    (x, y, w, h)           → filled with the foreground colour
#    (x, y, w, h, 'bg')     → filled with the background colour
#                              (used for eye whites, etc.)
# =============================================================

import pygame
import random
from constants import S, BG_DAY, FG_DAY, BG_NIGHT, FG_NIGHT


# ─────────────────────────────────────────────────────────────
#  Internal helpers
# ─────────────────────────────────────────────────────────────

def _blank(w1x, h1x):
    """Return a transparent surface at S× size."""
    surf = pygame.Surface((w1x * S, h1x * S), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    return surf


def _paint(surf, rects, fg, bg):
    """
    Draw a list of rects onto *surf*.
    Each element is (x, y, w, h) or (x, y, w, h, 'bg').
    Coordinates are at 1× and scaled by S internally.
    """
    for r in rects:
        x, y, w, h = r[0] * S, r[1] * S, r[2] * S, r[3] * S
        color = bg if (len(r) > 4 and r[4] == 'bg') else fg
        surf.fill(color, (x, y, w, h))


# ─────────────────────────────────────────────────────────────
#  DINO  (48 × 52 px at 1×  →  96 × 104 at S=2)
# ─────────────────────────────────────────────────────────────

DINO_W, DINO_H = 48, 52   # running / jumping bounding box (1×)
DUCK_W, DUCK_H = 64, 38   # ducking bounding box (1×)

# ── shared body parts ────────────────────────────────────────
_DINO_BODY = [
    # torso
    (2,  22, 40, 16),
    # head block
    (12,  0, 24, 22),
    # beak extension (right side of head)
    (34,  8, 10,  6),
    # tail
    (0,  14, 12, 10),
    # tiny arm nub
    (26, 24,  8,  6),
    # eye white  ← background colour
    (18,  4, 10, 10, 'bg'),
    # eye pupil
    (20,  6,  6,  6),
]

# ── running legs – frame 0 (left leg back / right leg forward) ──
_RUN0 = [
    (8,  36,  8, 12),   # back leg (down)
    (22, 38,  8,  6),   # front leg (up)
    (20, 42, 14,  4),   # front foot
]

# ── running legs – frame 1 ────────────────────────────────────
_RUN1 = [
    (8,  38,  8,  6),   # back leg (up)
    (6,  42, 14,  4),   # back foot
    (22, 36,  8, 12),   # front leg (down)
]

# ── jumping legs (both hanging) ───────────────────────────────
_JUMP_LEGS = [
    (8,  36,  8, 14),
    (22, 36,  8, 14),
]

# ── dead eye overlay (X eyes) ─────────────────────────────────
_DEAD_EYE = [
    (18,  4, 10, 10, 'bg'),   # clear normal eye area
    # \ stroke
    (18,  4,  4,  4),
    (22,  8,  4,  4),
    # / stroke
    (22,  4,  4,  4),
    (18,  8,  4,  4),
]

# ─────────────────────────────────────────────────────────────
#  DUCK dino  (64 × 38 px at 1×  →  128 × 76 at S=2)
# ─────────────────────────────────────────────────────────────

_DUCK_BODY = [
    # wide flat torso
    (0,  12, 54, 14),
    # head thrust forward (right side)
    (36,  0, 22, 16),
    # beak
    (56,  6, 10,  6),
    # tail
    (0,   4, 12, 10),
    # tiny arm nub
    (40, 18,  8,  6),
    # eye white
    (44,  4, 10, 10, 'bg'),
    # eye pupil
    (46,  6,  6,  6),
]

_DUCK0 = [
    (14, 24,  8, 12),   # back leg (down)
    (28, 26,  8,  6),   # front leg (up)
    (26, 30, 14,  4),   # front foot
]

_DUCK1 = [
    (14, 26,  8,  6),   # back leg (up)
    (12, 30, 14,  4),   # back foot
    (28, 24,  8, 12),   # front leg (down)
]


# ─────────────────────────────────────────────────────────────
#  SMALL CACTUS  (17 × 35 px at 1×  →  34 × 70 at S=2)
# ─────────────────────────────────────────────────────────────

SMALL_W, SMALL_H = 17, 35

_SMALL = [
    (6,  8,  5, 27),   # trunk
    (3,  0, 11, 10),   # top cap
    (0, 10,  7,  5),   # left arm (horizontal)
    (0, 13,  4, 10),   # left arm (vertical)
    (10, 16,  7,  5),  # right arm (horizontal)
    (13, 19,  4,  8),  # right arm (vertical)
]


# ─────────────────────────────────────────────────────────────
#  LARGE CACTUS  (24 × 50 px at 1×  →  48 × 100 at S=2)
# ─────────────────────────────────────────────────────────────

LARGE_W, LARGE_H = 24, 50

_LARGE = [
    (8,   6,  8, 44),   # trunk
    (3,   0, 18, 10),   # top cap
    (0,  12,  9,  6),   # left arm (horizontal)
    (0,  15,  5, 14),   # left arm (vertical)
    (14, 20,  9,  6),   # right arm (horizontal)
    (18, 24,  5, 12),   # right arm (vertical)
]


# ─────────────────────────────────────────────────────────────
#  BIRD (pterodactyl)  (46 × 36 px at 1×  →  92 × 72 at S=2)
# ─────────────────────────────────────────────────────────────

BIRD_W, BIRD_H = 46, 36

_BIRD_BODY = [
    # main body
    (10, 12, 28, 14),
    # head + beak
    (36,  8, 10, 10),
    # tail
    (0,  14,  8, 10),
    # feet
    (16, 24,  4,  6),
    (22, 24,  4,  6),
]

_WING_UP   = [(0,  0, 40, 12)]   # wing raised above body
_WING_DOWN = [(0, 24, 40, 12)]   # wing dropped below body


# ─────────────────────────────────────────────────────────────
#  CLOUD  (46 × 14 px at 1×  →  92 × 28 at S=2)
# ─────────────────────────────────────────────────────────────

CLOUD_W, CLOUD_H = 46, 14

_CLOUD = [
    (0,   8, 46, 6),
    (6,   4, 20, 8),
    (18,  0, 16, 14),
    (30,  4, 12, 8),
]


# ─────────────────────────────────────────────────────────────
#  Ground texture  (pre-generated static dot pattern)
# ─────────────────────────────────────────────────────────────

GROUND_TEX_W = 2400   # tile width; larger = longer repeat

_rng = random.Random(12345)   # fixed seed → same pattern every run
GROUND_DOTS = []
for _ in range(120):
    GROUND_DOTS.append((
        _rng.randint(0, GROUND_TEX_W - 1),   # x in tile
        _rng.randint(4, 14),                  # y below ground line
        _rng.choice([1, 1, 2]),               # width (1× coords)
        1,                                    # height
    ))


# ─────────────────────────────────────────────────────────────
#  Night sky (stars + moon)  – static positions
# ─────────────────────────────────────────────────────────────

_srng = random.Random(99)
STARS = [(_srng.randint(0, SCREEN_WIDTH := 1200),
          _srng.randint(10,  180))
         for _ in range(24)]


# ─────────────────────────────────────────────────────────────
#  SpriteBank  —  public API
# ─────────────────────────────────────────────────────────────

class SpriteBank:
    """
    Holds every pre-rendered pygame.Surface.
    Call set_colors(fg, bg) when the day/night mode changes;
    all surfaces are rebuilt automatically.
    """

    def __init__(self):
        self.fg = FG_DAY
        self.bg = BG_DAY
        self._build()

    def set_colors(self, fg, bg):
        if fg != self.fg or bg != self.bg:
            self.fg, self.bg = fg, bg
            self._build()

    # ── builder ───────────────────────────────────────────────

    def _build(self):
        fg, bg = self.fg, self.bg

        def dino_surf(legs, dead=False):
            s = _blank(DINO_W, DINO_H)
            _paint(s, _DINO_BODY, fg, bg)
            _paint(s, legs,       fg, bg)
            if dead:
                _paint(s, _DEAD_EYE, fg, bg)
            return s

        def duck_surf(legs):
            s = _blank(DUCK_W, DUCK_H)
            _paint(s, _DUCK_BODY, fg, bg)
            _paint(s, legs,       fg, bg)
            return s

        def cactus_multi(unit_rects, uw, uh, count, gap=2):
            """Build a surface with *count* cacti side-by-side."""
            total_w = uw * count + gap * (count - 1)
            surf = _blank(total_w, uh)
            for i in range(count):
                offset_x = i * (uw + gap)
                shifted = [(r[0] + offset_x,) + r[1:] for r in unit_rects]
                _paint(surf, shifted, fg, bg)
            return surf

        def bird_surf(wing):
            s = _blank(BIRD_W, BIRD_H)
            _paint(s, _BIRD_BODY, fg, bg)
            _paint(s, wing,       fg, bg)
            return s

        # ── dino ──────────────────────────────────────────────
        self.dino_run0 = dino_surf(_RUN0)
        self.dino_run1 = dino_surf(_RUN1)
        self.dino_jump = dino_surf(_JUMP_LEGS)
        self.dino_dead = dino_surf(_RUN0, dead=True)
        self.duck0     = duck_surf(_DUCK0)
        self.duck1     = duck_surf(_DUCK1)

        # ── cacti ─────────────────────────────────────────────
        self.cactus_small_1 = cactus_multi(_SMALL, SMALL_W, SMALL_H, 1)
        self.cactus_small_2 = cactus_multi(_SMALL, SMALL_W, SMALL_H, 2)
        self.cactus_small_3 = cactus_multi(_SMALL, SMALL_W, SMALL_H, 3)
        self.cactus_large_1 = cactus_multi(_LARGE, LARGE_W, LARGE_H, 1)
        self.cactus_large_2 = cactus_multi(_LARGE, LARGE_W, LARGE_H, 2)

        # ── bird ──────────────────────────────────────────────
        self.bird_up   = bird_surf(_WING_UP)
        self.bird_down = bird_surf(_WING_DOWN)

        # ── cloud ─────────────────────────────────────────────
        cloud = _blank(CLOUD_W, CLOUD_H)
        _paint(cloud, _CLOUD, fg, bg)
        self.cloud = cloud

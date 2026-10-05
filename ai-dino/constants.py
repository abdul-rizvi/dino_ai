# =============================================================
#  constants.py  —  All game-wide constants
# =============================================================

# ── Window ────────────────────────────────────────────────────
SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 400
FPS           = 60

# ── Palette (Chrome Dino grayscale scheme) ────────────────────
WHITE    = (255, 255, 255)
BG_DAY   = (247, 247, 247)
FG_DAY   = (83,  83,  83 )
BG_NIGHT = (35,  35,  35 )
FG_NIGHT = (163, 163, 163)

# ── Ground ────────────────────────────────────────────────────
GROUND_Y = 315          # y-coordinate of top of ground line

# ── Dino start position ───────────────────────────────────────
DINO_X = 80

# ── Physics ───────────────────────────────────────────────────
GRAVITY    = 0.85        # px / frame² (downward)
JUMP_VEL   = -17.0       # initial upward velocity on jump
DUCK_BOOST = 0.55        # extra gravity while ducking mid-air

# ── Game speed ────────────────────────────────────────────────
INIT_SPEED  = 8.0        # starting scroll speed (px/frame)
SPEED_INC   = 0.005      # speed added each frame
MAX_SPEED   = 26.0       # hard cap

# ── Score ─────────────────────────────────────────────────────
SCORE_RATE  = 0.08       # score points per pixel scrolled

# ── Day / Night cycle ─────────────────────────────────────────
NIGHT_CYCLE = 700        # toggle every N score points

# ── Sprite scale ─────────────────────────────────────────────
#  All pixel-art coordinates are defined at 1× and multiplied
#  by S at render time (S=2 → each original px becomes 2×2).
S = 2

# =============================================================
#  visualizer.py  —  YouTube Visual HUD & Neural Network Brain
# =============================================================

import math
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, S

# Color schemes
HUD_BG_DAY     = (240, 240, 240, 220)
HUD_BG_NIGHT   = (30, 30, 30, 220)
HUD_BORDER_DAY = (180, 180, 180)
HUD_BORDER_NIGHT = (70, 70, 70)

TEXT_DAY       = (40, 40, 40)
TEXT_NIGHT     = (230, 230, 230)
ACCENT_GREEN   = (46, 204, 113)
ACCENT_RED     = (231, 76, 60)
ACCENT_YELLOW  = (241, 196, 15)
ACCENT_CYAN    = (52, 152, 219)
ACCENT_PURPLE  = (155, 89, 182)

INPUT_LABELS = [
    "Dist X",
    "Width",
    "Height",
    "Obs Y",
    "Next Dist",
    "Dino Y",
    "Vel Y",
    "Speed"
]

OUTPUT_LABELS = [
    "JUMP",
    "DUCK"
]


class HUDVisualizer:
    def __init__(self):
        # Fonts
        self.font_large = pygame.font.SysFont("Consolas", 22, bold=True)
        self.font_main  = pygame.font.SysFont("Consolas", 15, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 11, bold=True)
        self.font_tiny  = pygame.font.SysFont("Consolas", 9, bold=False)

        # Toggles
        self.show_rays = True
        self.show_network = True
        self.show_help = True

    # ── 1. Top-Left HUD Info Box ──────────────────────────────
    def draw_stats(self, screen, gen, alive, pop_size, score, hi_score, speed, fps_mode, is_night):
        bg_col = (20, 20, 25, 210) if is_night else (255, 255, 255, 210)
        border_col = (80, 80, 95) if is_night else (200, 200, 210)
        txt_col = TEXT_NIGHT if is_night else TEXT_DAY

        box_w, box_h = 240, 130
        panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        panel.fill(bg_col)
        pygame.draw.rect(panel, border_col, (0, 0, box_w, box_h), width=2, border_radius=6)

        # Generation title
        gen_surf = self.font_large.render(f"GENERATION {gen}", True, ACCENT_YELLOW)
        panel.blit(gen_surf, (12, 10))

        # Alive badge
        alive_color = ACCENT_GREEN if alive > 10 else (ACCENT_YELLOW if alive > 3 else ACCENT_RED)
        alive_surf = self.font_main.render(f"ALIVE:  {alive:02d} / {pop_size}", True, alive_color)
        panel.blit(alive_surf, (12, 38))

        # Score & High Score
        sc_surf = self.font_main.render(f"SCORE:  {int(score):05d}", True, txt_col)
        panel.blit(sc_surf, (12, 58))

        hi_surf = self.font_main.render(f"BEST:   {int(hi_score):05d}", True, ACCENT_CYAN)
        panel.blit(hi_surf, (12, 78))

        # Speed and FPS Mode
        spd_surf = self.font_small.render(f"SPEED: {speed:.1f} px/f  |  {fps_mode}", True, (140, 140, 150))
        panel.blit(spd_surf, (12, 102))

        screen.blit(panel, (15, 15))

    # ── 2. Laser Raycast Vision Lines ─────────────────────────
    def draw_vision_rays(self, screen, dino, upcoming_obs, is_night):
        if not self.show_rays or dino is None or upcoming_obs is None:
            return

        # Dino eye position
        eye_x = int(dino.x + dino.width * 0.75)
        eye_y = int(dino.y + dino.height * 0.25)

        # Obstacle center / target point
        target_x = int(upcoming_obs.x + upcoming_obs.width * 0.3)
        target_y = int(upcoming_obs.y + upcoming_obs.height * 0.5)

        # Draw laser sight line
        laser_color = (0, 255, 180, 160) if not is_night else (80, 240, 255, 180)
        ray_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(ray_surface, laser_color, (eye_x, eye_y), (target_x, target_y), 2)

        # Target lock circle
        pygame.draw.circle(ray_surface, (255, 80, 80, 200), (target_x, target_y), 5, 2)

        # Obstacle bounding detection box
        obs_rect = upcoming_obs.get_rect()
        pygame.draw.rect(ray_surface, (255, 60, 60, 160), obs_rect, 2, border_radius=3)

        # Distance tag text
        dist_px = int(upcoming_obs.x - (dino.x + dino.width))
        tag_surf = self.font_tiny.render(f"{dist_px}px", True, (255, 80, 80))
        ray_surface.blit(tag_surf, (target_x - 10, target_y - 20))

        screen.blit(ray_surface, (0, 0))

    # ── 3. Live Neural Network Brain Overlay ──────────────────
    def draw_neural_net(self, screen, genome, config, last_inputs, last_outputs, is_night):
        if not self.show_network or genome is None:
            return

        box_w, box_h = 320, 165
        box_x = SCREEN_WIDTH - box_w - 15
        box_y = 15

        panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg_col = (15, 15, 22, 220) if is_night else (255, 255, 255, 220)
        border_col = (70, 70, 90) if is_night else (200, 200, 215)
        panel.fill(bg_col)
        pygame.draw.rect(panel, border_col, (0, 0, box_w, box_h), width=2, border_radius=6)

        # Header title
        title_col = TEXT_NIGHT if is_night else TEXT_DAY
        title = self.font_small.render("AI BRAIN  (NEAT NEURAL NET)", True, title_col)
        panel.blit(title, (10, 8))

        # Node coordinates mapping
        in_x = 75
        out_x = box_w - 45
        mid_x = (in_x + out_x) // 2

        num_inputs = len(INPUT_LABELS)
        in_ys = [28 + i * 16 for i in range(num_inputs)]
        out_ys = [50, 110]

        node_positions = {}
        for idx in range(num_inputs):
            node_positions[-(idx + 1)] = (in_x, in_ys[idx])

        node_positions[0] = (out_x, out_ys[0]) # Jump
        node_positions[1] = (out_x, out_ys[1]) # Duck

        # Hidden nodes positioning
        hidden_nodes = [n for n in genome.nodes.keys() if n not in (0, 1) and n > 0]
        if hidden_nodes:
            step_y = max(100 // (len(hidden_nodes) + 1), 16)
            for i, h_id in enumerate(hidden_nodes):
                node_positions[h_id] = (mid_x, 35 + (i + 1) * step_y)

        # Draw connections
        for conn_key, conn in genome.connections.items():
            if not conn.enabled:
                continue
            in_node, out_node = conn_key
            if in_node in node_positions and out_node in node_positions:
                pt1 = node_positions[in_node]
                pt2 = node_positions[out_node]

                weight = conn.weight
                alpha = min(255, int(abs(weight) * 60) + 70)
                width = max(1, min(int(abs(weight) * 1.5), 3))

                if weight >= 0:
                    col = (50, 180, 255, alpha)   # Excitatory (Cyan)
                else:
                    col = (255, 75, 75, alpha)    # Inhibitory (Red)

                pygame.draw.line(panel, col, pt1, pt2, width)

        # Draw input nodes + labels
        for idx, label in enumerate(INPUT_LABELS):
            pt = node_positions[-(idx + 1)]
            val = last_inputs[idx] if (last_inputs and idx < len(last_inputs)) else 0.0

            # Glowing circle if input is active
            active_intensity = min(255, max(50, int(abs(val) * 200)))
            fill_col = (0, active_intensity, 120)
            pygame.draw.circle(panel, fill_col, pt, 4)
            pygame.draw.circle(panel, (180, 180, 190), pt, 4, 1)

            lbl_surf = self.font_tiny.render(label, True, (130, 130, 140))
            panel.blit(lbl_surf, (8, pt[1] - 5))

        # Draw output nodes + labels
        for idx, label in enumerate(OUTPUT_LABELS):
            pt = node_positions[idx]
            out_val = last_outputs[idx] if (last_outputs and idx < len(last_outputs)) else 0.0
            is_firing = out_val > 0.5

            if is_firing:
                pygame.draw.circle(panel, ACCENT_GREEN, pt, 7)
                pygame.draw.circle(panel, (255, 255, 255), pt, 7, 2)
                lbl_surf = self.font_small.render(label, True, ACCENT_GREEN)
            else:
                pygame.draw.circle(panel, (70, 70, 80), pt, 5)
                pygame.draw.circle(panel, (140, 140, 150), pt, 5, 1)
                lbl_surf = self.font_small.render(label, True, (140, 140, 150))

            panel.blit(lbl_surf, (pt[0] - 38, pt[1] - 6))

        screen.blit(panel, (box_x, box_y))

    # ── 4. Bottom Controls Helper ─────────────────────────────
    def draw_controls(self, screen, is_night):
        if not self.show_help:
            return
        txt = "[1] 1x Speed  [2] 2x Speed  [3] 5x Speed  [F] Ultra Warp  [SPACE] Pause  [V] Raycast  [N] Brain  [ESC] Save & Quit"
        col = (110, 110, 120) if is_night else (130, 130, 140)
        surf = self.font_tiny.render(txt, True, col)
        screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, SCREEN_HEIGHT - 18))

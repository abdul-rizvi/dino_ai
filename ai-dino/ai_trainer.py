# =============================================================
#  ai_trainer.py  —  NEAT Multi-Dino AI Training Simulation
# =============================================================

import os
import sys
import time
import pickle
import random
import pygame
import neat

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    BG_DAY, BG_NIGHT, FG_DAY, FG_NIGHT,
    GROUND_Y, INIT_SPEED, SPEED_INC, MAX_SPEED,
    SCORE_RATE, NIGHT_CYCLE, S, DINO_X,
)
from sprites import SpriteBank, GROUND_TEX_W
from dino import Dinosaur
from obstacle import spawn_obstacle
from cloud import Cloud
from visualizer import HUDVisualizer

# Global tracking
GLOBAL_GEN = 0
GLOBAL_HI_SCORE = 0.0
BEST_OVERALL_GENOME = None
BEST_OVERALL_FITNESS = -1e9


def _draw_dino(screen, dino, is_leader=True):
    """Draw dino with solid colors for the leader, translucent ghost for the pack."""
    sp = dino.sprites
    if dino.ducking:
        img = sp.duck0 if dino._frame == 0 else sp.duck1
    elif dino.jumping:
        img = sp.dino_jump
    else:
        img = sp.dino_run0 if dino._frame == 0 else sp.dino_run1

    if is_leader:
        screen.blit(img, (dino.x, int(dino.y)))
    else:
        ghost = img.copy()
        ghost.set_alpha(85)
        screen.blit(ghost, (dino.x, int(dino.y)))


class AITrainingSimulation:
    BASE_MIN_GAP     = 520
    BASE_MAX_GAP     = 1150
    MIN_POSSIBLE_GAP = 280

    def __init__(self, config_path):
        self.config_path = config_path

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🦕 AI Dino Evolution — NEAT Reinforcement Learning")

        self.clock      = pygame.time.Clock()
        self.sprites    = SpriteBank()
        self.hud        = HUDVisualizer()

        # Speed multipliers: 1x (60 FPS), 2x (120 FPS), 5x (300 FPS), Warp (uncapped)
        self.fps_target = 60
        self.fps_mode   = "1x (60 FPS)"
        self.paused     = False

        # Ensure output directories exist
        os.makedirs("checkpoints", exist_ok=True)
        os.makedirs("stats", exist_ok=True)

        # CSV log header if not present
        log_file = os.path.join("stats", "training_log.csv")
        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("generation,best_score,best_fitness,avg_fitness\n")

    def _random_gap(self, speed):
        ratio = INIT_SPEED / max(speed, INIT_SPEED)
        lo = max(int(self.BASE_MIN_GAP * ratio), self.MIN_POSSIBLE_GAP)
        hi = max(int(self.BASE_MAX_GAP * ratio), lo + 100)
        return random.randint(lo, hi)

    def eval_genomes(self, genomes, config):
        """Runs one generation of the 50-dino population."""
        global GLOBAL_GEN, GLOBAL_HI_SCORE, BEST_OVERALL_GENOME, BEST_OVERALL_FITNESS
        GLOBAL_GEN += 1

        dinos = []
        nets  = []
        ge    = []

        # Initialize agents
        for genome_id, genome in genomes:
            genome.fitness = 0.0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            dinos.append(Dinosaur(self.sprites))
            ge.append(genome)

        # Game environment state
        speed         = INIT_SPEED
        score         = 0.0
        night         = False
        night_cycle   = 0
        ground_off    = 0.0
        scrolled      = 0.0
        gap_target    = self._random_gap(speed)

        obstacles     = []
        clouds        = [Cloud(self.sprites, offscreen=False) for _ in range(3)]
        passed_obs    = set()

        last_inputs   = None
        last_outputs  = None
        generation_running = True

        fg = FG_DAY
        bg = BG_DAY
        self.sprites.set_colors(fg, bg)

        while generation_running and len(dinos) > 0:
            # Handle Pygame user input & speed toggles
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("\n[AI Trainer] Exiting training. Saving best genome...")
                        if BEST_OVERALL_GENOME:
                            with open(os.path.join("checkpoints", "latest_best.pkl"), "wb") as f:
                                pickle.dump(BEST_OVERALL_GENOME, f)
                        pygame.quit()
                        sys.exit()

                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused

                    elif event.key == pygame.K_1:
                        self.fps_target = 60
                        self.fps_mode   = "1x (60 FPS)"
                    elif event.key == pygame.K_2:
                        self.fps_target = 120
                        self.fps_mode   = "2x (120 FPS)"
                    elif event.key == pygame.K_3:
                        self.fps_target = 300
                        self.fps_mode   = "5x (300 FPS)"
                    elif event.key in (pygame.K_f, pygame.K_w):
                        self.fps_target = 0
                        self.fps_mode   = "WARP (Uncapped)"

                    elif event.key == pygame.K_v:
                        self.hud.show_rays = not self.hud.show_rays
                    elif event.key == pygame.K_n:
                        self.hud.show_network = not self.hud.show_network
                    elif event.key == pygame.K_h:
                        self.hud.show_help = not self.hud.show_help

            if self.paused:
                self.clock.tick(30)
                continue

            # ── 1. Update Game Physics & Environment ──────────
            speed = min(speed + SPEED_INC, MAX_SPEED)
            score += speed * SCORE_RATE
            if score > GLOBAL_HI_SCORE:
                GLOBAL_HI_SCORE = score

            # Day / Night Toggle
            cur_night = int(score) // NIGHT_CYCLE
            if cur_night > night_cycle:
                night_cycle = cur_night
                night = not night
                fg = FG_NIGHT if night else FG_DAY
                bg = BG_NIGHT if night else BG_DAY
                self.sprites.set_colors(fg, bg)

            # Ground & Cloud Scrolling
            ground_off = (ground_off + speed) % GROUND_TEX_W
            scrolled += speed

            for c in clouds:
                c.update()
            clouds = [c for c in clouds if not c.dead]
            while len(clouds) < 4:
                clouds.append(Cloud(self.sprites, offscreen=True))

            # ── 2. Spawn & Move Obstacles ─────────────────────
            if scrolled >= gap_target:
                obstacles.append(spawn_obstacle(self.sprites, score))
                scrolled   = 0.0
                gap_target = self._random_gap(speed)

            for obs in obstacles:
                obs.update(speed)
            obstacles = [o for o in obstacles if not o.dead]

            # ── 3. Find Upcoming Obstacles for AI Sensors ─────
            # Find obstacles currently in front of the dinos (DINO_X)
            upcoming_obs = None
            second_obs   = None
            for obs in obstacles:
                if obs.x + obs.width > DINO_X:
                    if upcoming_obs is None:
                        upcoming_obs = obs
                    elif second_obs is None:
                        second_obs = obs
                        break

            # Calculate normalized sensory inputs
            if upcoming_obs:
                dist_x = (upcoming_obs.x - (DINO_X + 96)) / SCREEN_WIDTH
                obs_w  = upcoming_obs.width / 150.0
                obs_h  = upcoming_obs.height / 150.0
                obs_y  = (GROUND_Y - upcoming_obs.y) / 250.0
            else:
                dist_x = 1.0
                obs_w  = 0.0
                obs_h  = 0.0
                obs_y  = 0.0

            dist_next = ((second_obs.x - DINO_X) / SCREEN_WIDTH) if second_obs else 1.0
            norm_speed = (speed - INIT_SPEED) / (MAX_SPEED - INIT_SPEED)

            # ── 4. AI Decisions & Dino Updates ────────────────
            alive_indices_to_remove = set()

            for i in range(len(dinos)):
                dino = dinos[i]
                dino_y = dino.sensor_y
                dino_vel = dino.sensor_vel_y

                # 8 Sensor Inputs
                inputs = [
                    dist_x,
                    obs_w,
                    obs_h,
                    obs_y,
                    dist_next,
                    dino_y,
                    dino_vel,
                    norm_speed
                ]

                # Feedforward pass
                output = nets[i].activate(inputs)
                jump_val = output[0]
                duck_val = output[1]

                # Save leader's inputs/outputs for the visual HUD
                if i == 0:
                    last_inputs = inputs
                    last_outputs = output

                # Action mapping
                if jump_val > 0.5 and jump_val > duck_val:
                    dino.jump()
                elif duck_val > 0.5 and duck_val > jump_val:
                    dino.start_duck()
                else:
                    dino.stop_duck()

                dino.update()

                # Reward for surviving another frame (higher at high speeds)
                ge[i].fitness += 0.1 * (speed / INIT_SPEED)

                # Obstacle cleared bonus
                if upcoming_obs and id(upcoming_obs) not in passed_obs:
                    if upcoming_obs.x + upcoming_obs.width < dino.x:
                        ge[i].fitness += 15.0

                # Collision detection
                dino_rect = dino.get_rect()
                for obs in obstacles:
                    if dino_rect.colliderect(obs.get_rect()):
                        ge[i].fitness -= 2.0  # slight penalty on death
                        alive_indices_to_remove.add(i)
                        break

            # Mark passed obstacles
            if upcoming_obs and upcoming_obs.x + upcoming_obs.width < DINO_X:
                passed_obs.add(id(upcoming_obs))

            # Remove dead dinos from current generation
            if alive_indices_to_remove:
                dinos = [d for idx, d in enumerate(dinos) if idx not in alive_indices_to_remove]
                nets  = [n for idx, n in enumerate(nets) if idx not in alive_indices_to_remove]
                ge    = [g for idx, g in enumerate(ge) if idx not in alive_indices_to_remove]

            # ── 5. Render Everything ──────────────────────────
            self.screen.fill(bg)

            # Draw clouds
            for c in clouds:
                c.draw(self.screen)

            # Draw ground texture
            ground_y = GROUND_Y
            pygame.draw.line(self.screen, fg, (0, ground_y), (SCREEN_WIDTH, ground_y), 2)
            # Dotted ground texture
            gx = -ground_off
            while gx < SCREEN_WIDTH:
                pygame.draw.line(self.screen, fg, (int(gx), ground_y + 4), (int(gx + 12), ground_y + 4), 1)
                gx += 24

            # Draw obstacles
            for obs in obstacles:
                obs.draw(self.screen)

            # Draw Dinosaurs: pack first (ghosts), leader last (solid)
            if len(dinos) > 1:
                for d in dinos[1:]:
                    _draw_dino(self.screen, d, is_leader=False)
            if len(dinos) > 0:
                _draw_dino(self.screen, dinos[0], is_leader=True)

            # Draw YouTube HUD overlays
            # 1. Laser raycast from leader
            if len(dinos) > 0:
                self.hud.draw_vision_rays(self.screen, dinos[0], upcoming_obs, night)

            # 2. Stats box (Gen, Alive, Score, Speed)
            self.hud.draw_stats(
                self.screen,
                gen=GLOBAL_GEN,
                alive=len(dinos),
                pop_size=len(genomes),
                score=score,
                hi_score=GLOBAL_HI_SCORE,
                speed=speed,
                fps_mode=self.fps_mode,
                is_night=night
            )

            # 3. Live Neural Network brain
            if len(ge) > 0:
                self.hud.draw_neural_net(
                    self.screen,
                    genome=ge[0],
                    config=config,
                    last_inputs=last_inputs,
                    last_outputs=last_outputs,
                    is_night=night
                )

            # 4. Controls guide
            self.hud.draw_controls(self.screen, night)

            pygame.display.flip()

            # FPS Tick
            if self.fps_target > 0:
                self.clock.tick(self.fps_target)

        # ── 6. Generation Complete: Logging & Checkpoints ─────
        best_fit = max(g.fitness for _, g in genomes)
        avg_fit  = sum(g.fitness for _, g in genomes) / len(genomes)
        best_genome = max((g for _, g in genomes), key=lambda g: g.fitness)

        print(f"[GEN {GLOBAL_GEN:03d}]  Score: {int(score):05d}  |  Best Fit: {best_fit:7.1f}  |  Avg Fit: {avg_fit:7.1f}")

        # Update all-time best
        if best_fit > BEST_OVERALL_FITNESS:
            BEST_OVERALL_FITNESS = best_fit
            BEST_OVERALL_GENOME = best_genome

        # Save milestone checkpoints
        if GLOBAL_GEN in (1, 5, 10, 25, 50, 75, 100, 150, 200) or GLOBAL_GEN % 50 == 0:
            ckpt_path = os.path.join("checkpoints", f"best_gen_{GLOBAL_GEN}.pkl")
            with open(ckpt_path, "wb") as f:
                pickle.dump(best_genome, f)
            print(f"  [CHECKPOINT] Saved milestone: {ckpt_path}")

        # Always update latest_best.pkl
        with open(os.path.join("checkpoints", "latest_best.pkl"), "wb") as f:
            pickle.dump(best_genome, f)

        # Append to CSV log
        log_file = os.path.join("stats", "training_log.csv")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{GLOBAL_GEN},{int(score)},{best_fit:.2f},{avg_fit:.2f}\n")


def run_training(config_file="neat_config.txt", generations=300):
    """Entry point to launch NEAT evolution."""
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    sim = AITrainingSimulation(config_file)
    pop = neat.Population(config)

    # Standard console output
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    print("\n" + "=" * 60)
    print("  [AI Dino] NEAT AI DINO TRAINING STARTED")
    print("  Press '1', '2', '3' or 'F' to adjust simulation speed.")
    print("  Press 'SPACE' to pause. Press 'ESC' to quit & save.")
    print("=" * 60 + "\n")

    winner = pop.run(sim.eval_genomes, generations)

    # Save final winning genome
    with open(os.path.join("checkpoints", "winner.pkl"), "wb") as f:
        pickle.dump(winner, f)
    print("\n[AI Trainer] Evolution Complete! Winner saved to checkpoints/winner.pkl")


if __name__ == "__main__":
    run_training()

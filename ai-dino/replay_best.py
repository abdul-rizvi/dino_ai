# =============================================================
#  replay_best.py  —  Replay any Saved AI Dino Brain
# =============================================================

import os
import sys
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


def replay(checkpoint_file="checkpoints/latest_best.pkl", config_file="neat_config.txt"):
    if not os.path.exists(checkpoint_file):
        print(f"Checkpoint file '{checkpoint_file}' not found.")
        print("Run training first via 'python ai_trainer.py' to generate checkpoints!")
        return

    # Load NEAT config
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    # Load genome
    with open(checkpoint_file, "rb") as f:
        genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Init Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"AI Dino Replay : {os.path.basename(checkpoint_file)}")

    clock = pygame.time.Clock()
    sprites = SpriteBank()
    hud = HUDVisualizer()

    dino = Dinosaur(sprites)
    speed = INIT_SPEED
    score = 0.0
    night = False
    night_cycle = 0
    ground_off = 0.0
    scrolled = 0.0
    gap_target = 600

    obstacles = []
    clouds = [Cloud(sprites, offscreen=False) for _ in range(3)]
    fps_target = 60
    fps_mode = "1x (60 FPS)"
    paused = False

    last_inputs = None
    last_outputs = None

    fg = FG_DAY
    bg = BG_DAY
    sprites.set_colors(fg, bg)

    print(f"\n Playing AI Champion from {checkpoint_file}")
    print("  Controls: [1] 1x Speed  [2] 2x Speed  [3] 5x Speed  [SPACE] Pause  [ESC] Quit\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_1:
                    fps_target = 60
                    fps_mode = "1x (60 FPS)"
                elif event.key == pygame.K_2:
                    fps_target = 120
                    fps_mode = "2x (120 FPS)"
                elif event.key == pygame.K_3:
                    fps_target = 300
                    fps_mode = "5x (300 FPS)"
                elif event.key == pygame.K_v:
                    hud.show_rays = not hud.show_rays
                elif event.key == pygame.K_n:
                    hud.show_network = not hud.show_network

        if paused:
            clock.tick(30)
            continue

        if dino.dead:
            # Show dead for 1.5 seconds then reset
            pygame.time.delay(1200)
            dino.reset()
            speed = INIT_SPEED
            score = 0.0
            obstacles.clear()
            scrolled = 0.0

        # Update Game
        speed = min(speed + SPEED_INC, MAX_SPEED)
        score += speed * SCORE_RATE

        cur_night = int(score) // NIGHT_CYCLE
        if cur_night > night_cycle:
            night_cycle = cur_night
            night = not night
            fg = FG_NIGHT if night else FG_DAY
            bg = BG_NIGHT if night else BG_DAY
            sprites.set_colors(fg, bg)

        ground_off = (ground_off + speed) % GROUND_TEX_W
        scrolled += speed

        for c in clouds:
            c.update()
        clouds = [c for c in clouds if not c.dead]
        while len(clouds) < 4:
            clouds.append(Cloud(sprites, offscreen=True))

        # Spawn obstacles
        if scrolled >= gap_target:
            obstacles.append(spawn_obstacle(sprites, score))
            scrolled = 0.0
            gap_target = random.randint(300, 900)

        for obs in obstacles:
            obs.update(speed)
        obstacles = [o for o in obstacles if not o.dead]

        # Sensory Inputs
        upcoming_obs = None
        second_obs   = None
        for obs in obstacles:
            if obs.x + obs.width > DINO_X:
                if upcoming_obs is None:
                    upcoming_obs = obs
                elif second_obs is None:
                    second_obs = obs
                    break

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

        inputs = [
            dist_x,
            obs_w,
            obs_h,
            obs_y,
            dist_next,
            dino.sensor_y,
            dino.sensor_vel_y,
            norm_speed
        ]

        # AI Decision
        output = net.activate(inputs)
        last_inputs = inputs
        last_outputs = output

        if output[0] > 0.5 and output[0] > output[1]:
            dino.jump()
        elif output[1] > 0.5 and output[1] > output[0]:
            dino.start_duck()
        else:
            dino.stop_duck()

        dino.update()

        # Check collision
        dino_rect = dino.get_rect()
        for obs in obstacles:
            if dino_rect.colliderect(obs.get_rect()):
                dino.die()
                break

        # Render
        screen.fill(bg)

        for c in clouds:
            c.draw(screen)

        pygame.draw.line(screen, fg, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        gx = -ground_off
        while gx < SCREEN_WIDTH:
            pygame.draw.line(screen, fg, (int(gx), GROUND_Y + 4), (int(gx + 12), GROUND_Y + 4), 1)
            gx += 24

        for obs in obstacles:
            obs.draw(screen)

        dino.draw(screen)

        # Draw HUD & Visualizer
        hud.draw_vision_rays(screen, dino, upcoming_obs, night)
        hud.draw_stats(
            screen,
            gen=1,
            alive=0 if dino.dead else 1,
            pop_size=1,
            score=score,
            hi_score=score,
            speed=speed,
            fps_mode=fps_mode,
            is_night=night
        )
        hud.draw_neural_net(
            screen,
            genome=genome,
            config=config,
            last_inputs=last_inputs,
            last_outputs=last_outputs,
            is_night=night
        )
        hud.draw_controls(screen, night)

        pygame.display.flip()
        clock.tick(fps_target)

    pygame.quit()


if __name__ == "__main__":
    ckpt = sys.argv[1] if len(sys.argv) > 1 else "checkpoints/latest_best.pkl"
    replay(checkpoint_file=ckpt)

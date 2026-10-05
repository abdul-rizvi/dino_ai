# 🦕 AI Learns to Play Dino — From Zero to Hero
### A Complete Reinforcement Learning Project for YouTube Content

> **"Watch an AI go from running into the first cactus... to surviving forever."**

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [What the AI Knows (Inputs)](#-what-the-ai-knows-inputs)
3. [What the AI Can Do (Actions)](#-what-the-ai-can-do-actions)
4. [What the AI Is Scored On (Reward)](#-what-the-ai-is-scored-on-reward)
5. [Technology Stack](#-technology-stack)
6. [Full Project Roadmap](#-full-project-roadmap)
7. [Folder Structure](#-folder-structure)
8. [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
9. [The Algorithm — NEAT Explained Simply](#-the-algorithm--neat-explained-simply)
10. [Training Loop Explained](#-training-loop-explained)
11. [Score & Stats Logging](#-score--stats-logging)
12. [Visualization & Recording for YouTube](#-visualization--recording-for-youtube)
13. [YouTube Content Strategy](#-youtube-content-strategy)
14. [Milestones to Film](#-milestones-to-film)
15. [Common Pitfalls & How to Fix Them](#-common-pitfalls--how-to-fix-them)
16. [FAQ](#-faq)

---

## 🦕 Project Overview

This project trains an **AI agent** to play the **Chrome Dinosaur Game** (also called T-Rex Runner) using **Reinforcement Learning** — specifically the **NEAT** (NeuroEvolution of Augmenting Topologies) algorithm.

The entire point is to:

- Start with an AI that **knows absolutely nothing** — it will die on the very first cactus every time.
- Feed it only **raw inputs** from the game (no cheat codes, no hand-crafted rules).
- Let it **evolve and learn** purely by trial and error.
- After **hundreds of generations**, watch it **dodge every obstacle perfectly**.

This makes for **incredible YouTube content** because the audience can literally watch the AI get smarter in real time — the score goes from `50` → `200` → `1,000` → `10,000+`.

---

## 🧠 What the AI Knows (Inputs)

The AI is NOT told "jump over the cactus." It only sees **numbers** — raw sensor data about the game world:

| # | Input | Description | Example Value |
|---|-------|-------------|---------------|
| 1 | `distance_to_next_obstacle` | How far (in pixels) the next cactus/pterodactyl is | `320.5` |
| 2 | `obstacle_width` | How wide the obstacle is | `25.0` |
| 3 | `obstacle_height` | How tall the obstacle is | `60.0` |
| 4 | `obstacle_type` | Is it a cactus (0) or bird (1)? | `0` or `1` |
| 5 | `dino_y_position` | Is the dino on the ground or in the air? | `150.0` |
| 6 | `dino_velocity_y` | How fast is the dino moving up/down? | `-5.2` |
| 7 | `game_speed` | Current scrolling speed of the game | `8.5` |
| 8 | `distance_to_second_obstacle` | Distance to the NEXT next obstacle (for clusters) | `520.0` |

> **Why this matters for YouTube:** You can visualize all these inputs live on screen as colored bars or numbers. The audience sees exactly what the AI "sees." It feels like peeking inside the brain of a robot.

---

## 🕹️ What the AI Can Do (Actions)

The AI has only **3 possible actions** at any moment:

| Action | Key | Description |
|--------|-----|-------------|
| `NOTHING` | — | Keep running, do nothing |
| `JUMP` | `Space / ↑` | Jump over an obstacle |
| `DUCK` | `↓` | Duck under a flying pterodactyl |

> **That's it.** The AI must figure out WHEN to use these actions entirely on its own.

---

## 🏆 What the AI Is Scored On (Reward)

The AI receives **reward signals** that tell it if it did well or badly:

| Event | Reward | Reason |
|-------|--------|--------|
| Survived 1 frame | `+0.1` | Small reward for staying alive |
| Every 100 points scored | `+10.0` | Reward for lasting longer |
| Died (hit obstacle) | `-100.0` | Big penalty for dying |
| Jumped unnecessarily | `-1.0` | Penalize pointless jumps |

The AI's only goal is to **maximize its total reward** — and the only way to do that is to **stop dying**.

---

## 🛠️ Technology Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Game Environment** | `pygame` | Renders the Dino game we can control with code |
| **AI Algorithm** | `neat-python` | Implements the NEAT neuroevolution algorithm |
| **Neural Network** | Built into NEAT | The "brain" of the dinosaur |
| **Screen Recording** | `opencv-python` | Records training sessions to video |
| **Stats & Logging** | `matplotlib` + `csv` | Graphs score over time |
| **Visualization** | `pygame` overlay | Shows AI inputs, network, generation count live |
| **Language** | Python 3.10+ | Everything is in Python |

---

## 🗺️ Full Project Roadmap

This is your **complete step-by-step journey** from zero to a finished YouTube video.

```
PHASE 0: Research & Setup          (~1 day)
  └── Understand NEAT algorithm
  └── Set up Python environment
  └── Install all dependencies

PHASE 1: Build the Game            (~2-3 days)
  └── Create Dino game in pygame
  └── Add cactus & pterodactyl obstacles
  └── Make game speed increase over time
  └── Expose game state as Python variables

PHASE 2: Connect the AI            (~1-2 days)
  └── Write NEAT config file
  └── Connect game inputs → neural network
  └── Connect neural network output → game actions
  └── Test that AI can control the dino (badly at first)

PHASE 3: Training Loop             (~1 day)
  └── Run multiple dinos simultaneously (population)
  └── Kill dinos when they die, keep best genes
  └── Log scores per generation
  └── Save best genome to disk

PHASE 4: Visualization             (~1-2 days)
  └── Show generation number on screen
  └── Show each dino's score
  └── Visualize neural network live
  └── Add input sensor visualization

PHASE 5: Recording & Content       (~1 day)
  └── Record training session with OBS or OpenCV
  └── Record key milestone moments
  └── Create score graph video
  └── Edit YouTube video

PHASE 6: Polish & Upload           (~1 day)
  └── Final testing, clean up code
  └── Write GitHub README (this file!)
  └── Upload to GitHub
  └── Upload to YouTube
```

**Total estimated time: 7–12 days** (depending on experience level)

---

## 📁 Folder Structure

```
ai-dino/
│
├── 📄 README.md                  ← You are here
├── 📄 requirements.txt           ← All Python dependencies
├── 📄 neat_config.txt            ← NEAT algorithm configuration
│
├── 🐍 main.py                    ← Entry point, starts training
├── 🐍 game.py                    ← The Dino game (pygame)
├── 🐍 dino.py                    ← Dino character class
├── 🐍 obstacle.py                ← Cactus & Bird obstacle classes
├── 🐍 ai_player.py               ← Connects NEAT genome to game
├── 🐍 visualizer.py              ← Live neural network visualizer
├── 🐍 recorder.py                ← Records screen to video
├── 🐍 stats.py                   ← Logs and plots score history
│
├── 📁 assets/
│   ├── 🖼️ dino_run1.png
│   ├── 🖼️ dino_run2.png
│   ├── 🖼️ dino_dead.png
│   ├── 🖼️ dino_duck.png
│   ├── 🖼️ cactus_small.png
│   ├── 🖼️ cactus_large.png
│   ├── 🖼️ bird.png
│   └── 🖼️ ground.png
│
├── 📁 checkpoints/               ← Saved best genomes per generation
│   ├── gen_001_best.pkl
│   ├── gen_050_best.pkl
│   └── gen_200_best.pkl
│
├── 📁 recordings/                ← Saved training videos
│   ├── gen_001_100.mp4
│   └── highlights.mp4
│
└── 📁 stats/
    ├── scores.csv                ← Raw score data
    └── score_graph.png           ← Graph of scores over time
```

---

## ⚙️ Step-by-Step Setup Guide

### Step 1 — Install Python

Make sure you have Python **3.10 or newer**. Download from [python.org](https://python.org).

```bash
python --version
# Should show: Python 3.10.x or higher
```

### Step 2 — Create a Virtual Environment

```bash
# Navigate to your project folder
cd ai-dino

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### Step 3 — Install Dependencies

Create a `requirements.txt` file:

```txt
pygame==2.5.2
neat-python==0.92
opencv-python==4.9.0.80
matplotlib==3.8.0
numpy==1.26.0
```

Install them all:

```bash
pip install -r requirements.txt
```

### Step 4 — Create the NEAT Config File

Create `neat_config.txt` — this is the **brain blueprint** for the AI:

```ini
[NEAT]
fitness_criterion     = max
fitness_threshold     = 100000
pop_size              = 50
reset_on_extinction   = False

[DefaultGenome]
# Node activation options
activation_default      = tanh
activation_mutate_rate  = 0.0
activation_options      = tanh

# Aggregation options  
aggregation_default     = sum
aggregation_mutate_rate = 0.0
aggregation_options     = sum

# Bias options
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_max_value          = 30.0
bias_min_value          = -30.0
bias_mutate_power       = 0.5
bias_mutate_rate        = 0.7
bias_replace_rate       = 0.1

# Genome compatibility options
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# Connection add/remove rates
conn_add_prob           = 0.5
conn_delete_prob        = 0.3

# Connection enable options
enabled_default         = True
enabled_mutate_rate     = 0.01

feed_forward            = True
initial_connection      = full

# Node add/remove rates
node_add_prob           = 0.2
node_delete_prob        = 0.2

# Network parameters
num_hidden              = 0
num_inputs              = 8
num_outputs             = 3

# Node response options
response_init_mean      = 1.0
response_init_stdev     = 0.0
response_max_value      = 30.0
response_min_value      = -30.0
response_mutate_power   = 0.0
response_mutate_rate    = 0.0
response_replace_rate   = 0.0

# Connection weight options
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 30
weight_min_value        = -30
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 20
species_elitism      = 2

[DefaultReproduction]
elitism            = 2
survival_threshold = 0.2
```

---

## 🧬 The Algorithm — NEAT Explained Simply

> **For non-technical viewers of your YouTube video, you can use this exact explanation.**

### What is NEAT?

NEAT stands for **NeuroEvolution of Augmenting Topologies**. It's an algorithm that:

1. Creates a **population** of AI brains (e.g., 50 dinosaurs at once)
2. Each brain is a **neural network** — connections between inputs and outputs
3. All brains start **completely random** — they have no idea what to do
4. They all play the game at the same time until they die
5. The ones that **survived the longest** get to "reproduce" — passing their best traits to the next generation
6. The new generation **mutates slightly** — some connections change, new ones appear
7. Repeat for **hundreds of generations**

### The Evolution Process (Visual)

```
Generation 1:  50 dinos, all die immediately        → Best score: 47
Generation 5:  Some learn to jump                   → Best score: 230
Generation 20: Most learn to jump small cacti        → Best score: 890
Generation 50: Learning to handle speed increases    → Best score: 3,400
Generation 100: Handling clusters, birds             → Best score: 9,200
Generation 200: Near-perfect play                   → Best score: 50,000+
```

### The Neural Network Brain

```
INPUTS (8 numbers)          HIDDEN LAYER            OUTPUTS (3 decisions)
─────────────────           ────────────            ──────────────────────
distance_to_obstacle ──────►                ┌──────► NOTHING (keep running)
obstacle_width       ──────► [neurons that  │
obstacle_height      ──────►  learn to      ├──────► JUMP
obstacle_type        ──────►  combine       │
dino_y_position      ──────►  these         └──────► DUCK
dino_velocity_y      ──────►  signals]
game_speed           ──────►
distance_2nd_obs     ──────►

The output with the HIGHEST activation value wins → that's the action taken
```

---

## 🔄 Training Loop Explained

Here's exactly what happens every single frame of the game:

```
EVERY FRAME:
│
├─ 1. GET GAME STATE
│     └── Read: obstacle distance, speed, dino position, etc.
│
├─ 2. FEED INTO NEURAL NETWORK
│     └── Each of the 50 dinos passes its inputs through its own brain
│     └── Brain outputs 3 numbers (one per action)
│
├─ 3. PICK ACTION
│     └── Whichever output number is highest = that's the action
│     └── (NOTHING / JUMP / DUCK)
│
├─ 4. APPLY ACTION TO GAME
│     └── Press the jump or duck key, or do nothing
│
├─ 5. CHECK FOR DEATH
│     └── Did the dino hit an obstacle?
│          YES → Remove this dino from the population, record its score
│          NO  → Add +0.1 to its fitness score (survived another frame)
│
└─ 6. WHEN ALL DINOS ARE DEAD
      └── NEAT evaluates all fitness scores
      └── Best genomes survive → produce next generation
      └── Weak genomes are deleted
      └── Repeat from step 1 with new generation
```

---

## 📊 Score & Stats Logging

Every generation, log these stats to `stats/scores.csv`:

```csv
generation, best_score, avg_score, worst_score, num_species, elapsed_time
1,          47,         12,         3,           3,           00:00:08
2,          89,         31,         8,           4,           00:00:16
3,          145,        67,         21,          5,           00:00:24
...
200,        52340,      31200,      8900,         8,          03:24:15
```

### What to Show on YouTube

You can generate a **live graph** during training that looks like this:

```
Score Over Generations
│
50000 ┤                                              ╭──────
40000 ┤                                         ╭───╯
30000 ┤                                    ╭────╯
20000 ┤                              ╭─────╯
10000 ┤                    ╭─────────╯
 5000 ┤          ╭─────────╯
 1000 ┤   ╭──────╯
    0 ┼───╯────────────────────────────────────────────────
      0   20   40   60   80   100  120  140  160  180  200
                        Generation
```

The moment this graph goes **exponential** (shoots up suddenly) is **the best moment in your YouTube video** — the AI has a breakthrough.

---

## 🎬 Visualization & Recording for YouTube

### Live On-Screen Overlay (What Viewers See)

During training, display this information on screen in real time:

```
┌─────────────────────────────────────────┐
│  🧬 Generation: 47          👾 Alive: 23/50  │
│  🏆 Best Score: 3,420       ⏱️ Time: 02:14   │
│  📈 Best Ever: 8,900                         │
├─────────────────────────────────────────┤
│  NEURAL NETWORK VISUALIZATION                │
│  [live animated brain diagram here]          │
├─────────────────────────────────────────┤
│  SENSOR DATA (current best dino)             │
│  🔴 Obstacle Distance: ████░░░░ 320px        │
│  🟡 Obstacle Height:   ███░░░░░ 60px         │
│  🟢 Game Speed:        ██████░░ 8.5          │
│  🔵 Dino Y Position:   ████████ 150px        │
└─────────────────────────────────────────┘
```

### Recording Setup

**Option A — OBS Studio (Recommended for YouTube)**
- Free, professional
- Download: [obsproject.com](https://obsproject.com)
- Set output: 1080p, 60fps, MP4
- Scene: Capture the pygame window

**Option B — OpenCV (In-Code Recording)**
```python
# recorder.py
import cv2
import pygame
import numpy as np

class ScreenRecorder:
    def __init__(self, filename, fps=60, size=(1280, 720)):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(filename, fourcc, fps, size)
    
    def capture_frame(self, surface):
        # Convert pygame surface to OpenCV frame
        frame = pygame.surfarray.array3d(surface)
        frame = frame.transpose([1, 0, 2])  # Swap axes
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.writer.write(frame)
    
    def stop(self):
        self.writer.release()
```

### What to Record for YouTube

| Clip | When to Record | Duration | Purpose |
|------|---------------|----------|---------|
| **Gen 1 Fail** | Very first run | 30 sec | Show AI is clueless |
| **First Jump** | When AI first jumps | 30 sec | Exciting "aha" moment |
| **First 100 points** | Gen ~5–10 | 1 min | First milestone |
| **First 1,000 points** | Gen ~20–30 | 2 min | Big improvement |
| **First 10,000 points** | Gen ~60–80 | 2 min | Getting scary good |
| **Handling Birds** | When it ducks first time | 1 min | New behavior learned |
| **First 50,000+** | Gen ~150–200 | 3 min | Near-perfect play |
| **Score Graph Timelapse** | End of training | 2 min | Satisfying reveal |
| **AI vs Human** | After training | 3 min | Epic comparison |

---

## 📹 YouTube Content Strategy

### Video Structure (Recommended)

```
[0:00 - 0:30]  HOOK
  "Watch this AI go from dying instantly to being
   literally unkillable — in 200 generations."
  (Show the BEST clip first, then cut back to Gen 1)

[0:30 - 2:00]  EXPLAIN THE SETUP
  "Here's what the AI knows... here's what it can do...
   that's IT. No rules. No tutorials. Just numbers."
  (Show the input visualization, keep it simple)

[2:00 - 5:00]  GEN 1–10: THE STRUGGLE
  "Watch how dumb it is right now."
  Show all the fail compilations. Funny moments.
  AI jumping AWAY from cacti, not OVER them.

[5:00 - 9:00]  GEN 10–50: SOMETHING IS LEARNING
  "Wait... did it just... jump on purpose?!"
  Show the first intentional jump. Score climbing.
  Show the score graph starting to rise.

[9:00 - 14:00]  GEN 50–150: GETTING DANGEROUS
  "It's getting scary now."
  Show it handling speed increases, clusters, birds.
  Show the neural network visualization lighting up.

[14:00 - 17:00]  GEN 150–200: BASICALLY PERFECT
  Show it running for minutes without dying.
  Score counter going insane.

[17:00 - 18:00]  AI vs HUMAN CHALLENGE
  Human player (you) tries to beat the AI.
  Spoiler: you lose.

[18:00 - 19:00]  SCORE GRAPH REVEAL
  Show the beautiful exponential graph.
  "From 47 to 52,000 in 200 generations."

[19:00 - 20:00]  OUTRO
  "The AI learned this in 3 hours.
   It took you and me years to get good at video games."
```

### Thumbnail Ideas

- **Split image**: Left = dino hitting cactus (red X), Right = dino dodging everything (green checkmark)
- **Text**: "AI Learned to Play Dino in 200 Tries"
- **Score counter**: Show `52,340` in big numbers

### Title Ideas

- "I Trained an AI to Play the Dino Game (It Got Scary Good)"
- "Dumb AI → Unkillable AI in 200 Generations"
- "Teaching an AI to Play Chrome Dino From Scratch"
- "AI Learns to Play Dino Game | Reinforcement Learning"

---

## 🎯 Milestones to Film

These are the **emotional peaks** of your video — record them specifically:

### Milestone 1: The First Jump (Gen 3–8)
> The AI accidentally jumps over a cactus for the first time.
> The audience reaction: **"Oh wait, it's learning!"**

### Milestone 2: The First 500 Points (Gen 10–20)
> A dino stays alive long enough to reach 500 points.
> The scoreboard starts feeling real.

### Milestone 3: The Speed Increase Survival (Gen 30–50)
> The Chrome Dino game speeds up over time. Surviving a speed jump is hard.
> When the AI handles its first speed increase, it's a breakthrough.

### Milestone 4: Ducking Under a Bird (Gen 50–80)
> Birds fly at head height — the only way to avoid them is to DUCK.
> When the AI ducks for the first time, the neural network has discovered a **new strategy**.
> This is cinematic gold for your video.

### Milestone 5: Surviving 5 Minutes (Gen 100–150)
> The game has been running for **5 minutes** with one dino alive.
> Show the clock. Let it breathe. Let the audience feel the tension.

### Milestone 6: The Perfect Run (Gen 150–200)
> The game keeps accelerating. Eventually the AI plays "perfectly."
> Record the full run.

---

## 🐛 Common Pitfalls & How to Fix Them

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| AI never learns to jump | Reward for survival is too small | Increase survival reward or add a "near-miss" bonus |
| AI jumps constantly (spam jumping) | Jump penalty is too small | Increase the penalty for unnecessary jumps |
| Training is too slow | Population size too large | Reduce `pop_size` from 50 to 30 |
| AI gets stuck at a score | Too few hidden neurons | Add hidden nodes in config |
| All dinos die generation 1 | Game starts too fast | Start game speed lower, increase gradually |
| Training never improves after gen 20 | Species going extinct | Increase `max_stagnation` in config |
| Video looks choppy | Frame rate too low | Set pygame clock to 60fps minimum |
| AI learns to jump over birds | Bird height detection wrong | Ensure `obstacle_type` input is correct |

---

## ❓ FAQ

**Q: Why NEAT instead of Deep Q-Network (DQN)?**
> NEAT is much easier to visualize — you can literally draw the neural network on screen. DQN uses a massive deep neural network that's impossible to visualize intuitively. For YouTube content, NEAT is far superior for teaching.

**Q: How long does training take?**
> On a modern laptop: roughly **2–4 hours** for 200 generations with 50 dinos in the population. You don't need a GPU.

**Q: Can I use the actual Chrome Dino game (from the browser)?**
> Technically yes — using `pyautogui` + `mss` (screen capture) to read the browser and send keystrokes. But it's 10x more complicated and unreliable. **Rebuilding the game in pygame** gives you full control, perfect performance, and looks identical on camera.

**Q: What if the AI never gets past 1,000 points?**
> Tweak the NEAT config: increase `pop_size` to 100, lower `compatibility_threshold` to 2.0, and increase `conn_add_prob` to 0.7. Also check that your fitness function is correctly rewarding survival time.

**Q: Can I run multiple training sessions at once?**
> Yes! You can run training without the pygame window (headless mode) for maximum speed, then only render the final/best genome visually for the video.

**Q: How do I make the "score graph" video effect?**
> Use `matplotlib.animation.FuncAnimation` to create an animated line graph where the score is drawn generation by generation. Export as `.gif` or `.mp4`.

**Q: Do I need to know machine learning to build this?**
> No deep math required. NEAT handles all the hard parts. You just need to:
> 1. Define what the AI can see (inputs)
> 2. Define what the AI can do (outputs)  
> 3. Define how to score it (fitness function)
> The library does everything else.

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Clone / create project
mkdir ai-dino && cd ai-dino

# 2. Set up environment
python -m venv venv
venv\Scripts\activate      # Windows
pip install pygame neat-python opencv-python matplotlib numpy

# 3. Run training
python main.py

# 4. Watch the magic happen
# Generation 1: AI dies immediately
# Generation 50: AI is getting good
# Generation 200: AI is basically unbeatable
```

---

## 📚 Learning Resources

| Resource | Link | Why It Helps |
|----------|------|-------------|
| NEAT-Python Docs | [neat-python.readthedocs.io](https://neat-python.readthedocs.io) | Official library docs |
| NEAT Paper (Original) | Stanley & Miikkulainen, 2002 | The science behind the algorithm |
| Pygame Tutorial | [pygame.org/docs](https://www.pygame.org/docs) | How to build the game |
| Code Bullet (YouTube) | @CodeBullet | Inspiration — best AI game videos |
| TechWithTim NEAT Tutorial | YouTube | Hands-on NEAT tutorial in Python |

---

## 📜 License

MIT License — use this freely, credit appreciated.

---

*Built with 🦕 + 🧠 + a lot of patience watching AI dinosaurs die*

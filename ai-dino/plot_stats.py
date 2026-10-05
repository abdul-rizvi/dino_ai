# =============================================================
#  plot_stats.py  —  YouTube Chart Generator for AI Progress
# =============================================================

import os
import csv
import matplotlib.pyplot as plt

def generate_training_chart(csv_path="stats/training_log.csv", output_png="stats/training_progress.png"):
    if not os.path.exists(csv_path):
        print(f"File {csv_path} not found. Run training first!")
        return

    gens = []
    scores = []
    best_fits = []
    avg_fits = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gens.append(int(row["generation"]))
            scores.append(float(row["best_score"]))
            best_fits.append(float(row["best_fitness"]))
            avg_fits.append(float(row["avg_fitness"]))

    if not gens:
        print("No training data logged yet.")
        return

    # Modern dark YouTube-friendly style
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.patch.set_facecolor("#18181c")
    ax1.set_facecolor("#202026")
    ax2.set_facecolor("#202026")

    # 1. Scores plot
    ax1.plot(gens, scores, color="#00ffcc", linewidth=2.5, label="High Score")
    ax1.set_title("AI Dino Learning Curve — Score by Generation", fontsize=14, color="#ffffff", pad=12, fontweight="bold")
    ax1.set_ylabel("Score", fontsize=11, color="#cccccc")
    ax1.grid(True, linestyle="--", alpha=0.3, color="#555566")
    ax1.legend(loc="upper left")

    # 2. Fitness plot
    ax2.plot(gens, best_fits, color="#ffcc00", linewidth=2.2, label="Best Fitness")
    ax2.plot(gens, avg_fits, color="#ff4466", linewidth=1.5, linestyle="--", label="Average Fitness")
    ax2.set_title("Genetic Fitness Progression", fontsize=12, color="#ffffff", pad=10)
    ax2.set_xlabel("Generation", fontsize=11, color="#cccccc")
    ax2.set_ylabel("Fitness Points", fontsize=11, color="#cccccc")
    ax2.grid(True, linestyle="--", alpha=0.3, color="#555566")
    ax2.legend(loc="upper left")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()

    print(f"[Chart Generated] Saved high-resolution graph to: {output_png}")

if __name__ == "__main__":
    generate_training_chart()

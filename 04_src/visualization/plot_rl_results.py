"""
Plot RL results for the Adaptive AI Tutor Research Lab.

Goal:
Create visualizations for Q-learning and policy comparison results.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


Q_LEARNING_PATH = Path("06_results/tables/q_learning_results.csv")
POLICY_COMPARISON_PATH = Path("06_results/tables/rl_policy_comparison.csv")

OUTPUT_DIR = Path("06_results/figures/rl")
Q_LEARNING_REWARD_PLOT = OUTPUT_DIR / "q_learning_reward_curve.png"
POLICY_COMPARISON_PLOT = OUTPUT_DIR / "rl_policy_comparison.png"


def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file."""

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    return pd.read_csv(path)


def plot_q_learning_reward_curve(q_learning_df: pd.DataFrame) -> None:
    """Plot total reward per episode for Q-learning."""

    episode_summary = (
        q_learning_df.groupby("episode")
        .agg(total_reward=("reward", "sum"))
        .reset_index()
    )

    episode_summary["rolling_reward"] = (
        episode_summary["total_reward"]
        .rolling(window=10, min_periods=1)
        .mean()
    )

    plt.figure(figsize=(9, 5))
    plt.plot(
        episode_summary["episode"],
        episode_summary["total_reward"],
        label="Episode reward",
        alpha=0.5,
    )
    plt.plot(
        episode_summary["episode"],
        episode_summary["rolling_reward"],
        label="Rolling average reward",
        linewidth=2,
    )

    plt.title("Q-Learning Reward Curve")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.legend()
    plt.tight_layout()
    plt.savefig(Q_LEARNING_REWARD_PLOT, dpi=200)
    plt.close()


def plot_policy_comparison(policy_df: pd.DataFrame) -> None:
    """Plot average reward by policy."""

    plt.figure(figsize=(7, 5))
    plt.bar(policy_df["policy"], policy_df["average_reward"])

    plt.title("Average Reward by Policy")
    plt.xlabel("Policy")
    plt.ylabel("Average Reward")
    plt.tight_layout()
    plt.savefig(POLICY_COMPARISON_PLOT, dpi=200)
    plt.close()


def main() -> None:
    """Create RL result plots."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    q_learning_df = load_csv(Q_LEARNING_PATH)
    policy_df = load_csv(POLICY_COMPARISON_PATH)

    plot_q_learning_reward_curve(q_learning_df)
    plot_policy_comparison(policy_df)

    print("RL plots created successfully.")
    print(f"Q-learning reward curve saved to: {Q_LEARNING_REWARD_PLOT}")
    print(f"Policy comparison plot saved to: {POLICY_COMPARISON_PLOT}")


if __name__ == "__main__":
    main()


# NOTES
# This file creates plots for the RL part of the project.
#
# q_learning_reward_curve.png:
# Shows whether reward improves across training episodes.
#
# rl_policy_comparison.png:
# Compares random policy and Q-learning by average reward.
#
# Why this matters:
# Research projects need visual results, not only code.
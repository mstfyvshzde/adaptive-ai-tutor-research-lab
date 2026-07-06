"""
Compare RL policies for the Adaptive AI Tutor Research Lab.

Goal:
Compare random policy results with Q-learning results.
"""

from pathlib import Path

import pandas as pd


RANDOM_POLICY_PATH = Path("06_results/tables/rl_random_policy_results.csv")
Q_LEARNING_PATH = Path("06_results/tables/q_learning_results.csv")

OUTPUT_DIR = Path("06_results/tables")
OUTPUT_PATH = OUTPUT_DIR / "rl_policy_comparison.csv"


def load_results(path: Path, policy_name: str) -> pd.DataFrame:
    """Load policy result file."""

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    dataframe = pd.read_csv(path)
    dataframe["policy"] = policy_name

    return dataframe


def summarize_policy(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create summary metrics for one policy."""

    summary = (
        dataframe.groupby("policy")
        .agg(
            average_reward=("reward", "mean"),
            average_correctness=("is_correct", "mean"),
            average_probability_correct=("probability_correct", "mean"),
            total_steps=("reward", "count"),
        )
        .round(3)
        .reset_index()
    )

    return summary


def main() -> None:
    """Compare random policy and Q-learning policy."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    random_df = load_results(RANDOM_POLICY_PATH, "random_policy")
    q_learning_df = load_results(Q_LEARNING_PATH, "q_learning")

    combined_df = pd.concat([random_df, q_learning_df], ignore_index=True)

    comparison_df = summarize_policy(combined_df)
    comparison_df.to_csv(OUTPUT_PATH, index=False)

    print("RL policy comparison completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nPolicy comparison:")
    print(comparison_df)


if __name__ == "__main__":
    main()


# NOTES
# This file compares two RL policies:
# 1. random_policy:
#    Chooses easy, medium, or hard randomly.
#
# 2. q_learning:
#    Learns which action gives better reward.
#
# Why this matters:
# We need to show whether learning-based decision making performs better
# than a random tutoring strategy.
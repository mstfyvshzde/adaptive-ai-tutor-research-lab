"""
Evaluate reinforcement learning policy results.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path("06_results/tables/rl_policy_comparison.csv")
OUTPUT_PATH = Path("06_results/tables/rl_evaluation_summary.csv")


def main() -> None:
    """Create RL evaluation summary."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing file: {INPUT_PATH}. Run compare_rl_policies.py first."
        )

    comparison_df = pd.read_csv(INPUT_PATH)

    summary_df = comparison_df.sort_values(
        "average_reward",
        ascending=False,
    ).reset_index(drop=True)

    summary_df.to_csv(OUTPUT_PATH, index=False)

    print("RL evaluation completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(summary_df)


if __name__ == "__main__":
    main()
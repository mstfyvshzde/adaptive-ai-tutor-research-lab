"""
Evaluate supervised knowledge tracing results.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path("06_results/tables/supervised_baseline_metrics.csv")
OUTPUT_PATH = Path("06_results/tables/supervised_evaluation_summary.csv")


def main() -> None:
    """Create a clean supervised model summary."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing file: {INPUT_PATH}. Run supervised_baselines.py first."
        )

    results_df = pd.read_csv(INPUT_PATH)

    summary_df = (
        results_df.sort_values("roc_auc", ascending=False)
        .reset_index(drop=True)
    )

    summary_df.to_csv(OUTPUT_PATH, index=False)

    print("Supervised evaluation completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(summary_df)


if __name__ == "__main__":
    main()
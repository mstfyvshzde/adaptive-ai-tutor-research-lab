"""
Evaluate recommendation baseline outputs.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path("06_results/tables/recommendation_examples.csv")
OUTPUT_PATH = Path("06_results/tables/recommender_evaluation_summary.csv")


def main() -> None:
    """Summarize recommendation methods."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing file: {INPUT_PATH}. Run recommender.py first."
        )

    recommendations_df = pd.read_csv(INPUT_PATH)

    summary_df = (
        recommendations_df.groupby("method")
        .agg(
            recommendation_count=("recommended_question_id", "count"),
            unique_topics=("recommended_topic", "nunique"),
            unique_difficulties=("recommended_difficulty", "nunique"),
        )
        .reset_index()
    )

    summary_df.to_csv(OUTPUT_PATH, index=False)

    print("Recommender evaluation completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(summary_df)


if __name__ == "__main__":
    main()
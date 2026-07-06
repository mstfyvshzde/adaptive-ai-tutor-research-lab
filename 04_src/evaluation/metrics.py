"""
Shared evaluation metrics for the Adaptive AI Tutor Research Lab.
"""

import pandas as pd


def summarize_binary_classification(results_df: pd.DataFrame) -> pd.DataFrame:
    """Return supervised model metrics sorted by ROC-AUC."""

    metric_columns = [
        "model",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "log_loss",
    ]

    available_columns = [col for col in metric_columns if col in results_df.columns]

    return (
        results_df[available_columns]
        .sort_values("roc_auc", ascending=False)
        .reset_index(drop=True)
    )


def summarize_policy_results(results_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize RL policy results."""

    return (
        results_df.groupby("policy")
        .agg(
            average_reward=("reward", "mean"),
            average_correctness=("is_correct", "mean"),
            total_steps=("reward", "count"),
        )
        .round(3)
        .reset_index()
    )
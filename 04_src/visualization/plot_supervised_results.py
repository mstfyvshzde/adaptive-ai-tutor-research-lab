"""
Plot supervised baseline results.

Goal:
Visualize model comparison for knowledge tracing.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("06_results/tables/supervised_baseline_metrics.csv")
OUTPUT_DIR = Path("06_results/figures/supervised")
ROC_AUC_PLOT = OUTPUT_DIR / "supervised_roc_auc_comparison.png"
LOG_LOSS_PLOT = OUTPUT_DIR / "supervised_log_loss_comparison.png"


def load_results(path: Path) -> pd.DataFrame:
    """Load supervised baseline metrics."""

    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}. Run supervised_baselines.py first."
        )

    return pd.read_csv(path)


def plot_roc_auc(results_df: pd.DataFrame) -> None:
    """Plot ROC-AUC comparison."""

    plt.figure(figsize=(8, 5))
    plt.bar(results_df["model"], results_df["roc_auc"])
    plt.title("Supervised Model Comparison — ROC-AUC")
    plt.xlabel("Model")
    plt.ylabel("ROC-AUC")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(ROC_AUC_PLOT, dpi=200)
    plt.close()


def plot_log_loss(results_df: pd.DataFrame) -> None:
    """Plot Log Loss comparison."""

    plt.figure(figsize=(8, 5))
    plt.bar(results_df["model"], results_df["log_loss"])
    plt.title("Supervised Model Comparison — Log Loss")
    plt.xlabel("Model")
    plt.ylabel("Log Loss")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(LOG_LOSS_PLOT, dpi=200)
    plt.close()


def main() -> None:
    """Create supervised result plots."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results_df = load_results(INPUT_PATH)

    plot_roc_auc(results_df)
    plot_log_loss(results_df)

    print("Supervised result plots created successfully.")
    print(f"ROC-AUC plot saved to: {ROC_AUC_PLOT}")
    print(f"Log Loss plot saved to: {LOG_LOSS_PLOT}")


if __name__ == "__main__":
    main()


# NOTES
# This file creates plots for supervised model results.
#
# ROC-AUC:
# Shows how well the model separates correct and incorrect answers.
#
# Log Loss:
# Shows how reliable the probability predictions are.
#
# Lower Log Loss is better.
# Higher ROC-AUC is better.
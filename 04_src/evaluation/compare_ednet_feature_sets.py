from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

BASELINE_METRICS_PATH = (
    ROOT
    / "06_results/tables/ednet/scale_experiments/ednet_500k_max/ednet_supervised_metrics.csv"
)

ENHANCED_METRICS_PATH = (
    ROOT
    / "06_results/tables/ednet/ednet_enhanced_supervised_metrics.csv"
)

OUTPUT_PATH = ROOT / "06_results/tables/ednet/ednet_feature_ablation_500k.csv"


REQUIRED_COLUMNS = ["accuracy", "f1", "roc_auc", "log_loss"]


def normalize_model_column(df):
    possible_model_columns = ["model", "model_name", "classifier"]

    for col in possible_model_columns:
        if col in df.columns:
            return df.rename(columns={col: "best_model"})

    raise ValueError(
        f"Could not find model column. Expected one of: {possible_model_columns}"
    )


def load_best_row(path, feature_set_name):
    if not path.exists():
        raise FileNotFoundError(f"Metrics file not found: {path}")

    df = pd.read_csv(path)
    df = normalize_model_column(df)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in {path}: {missing_columns}")

    best = df.sort_values("roc_auc", ascending=False).iloc[0]

    return {
        "feature_set": feature_set_name,
        "best_model": best["best_model"],
        "accuracy": best["accuracy"],
        "f1": best["f1"],
        "roc_auc": best["roc_auc"],
        "log_loss": best["log_loss"],
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        load_best_row(BASELINE_METRICS_PATH, "baseline_features"),
        load_best_row(ENHANCED_METRICS_PATH, "enhanced_features"),
    ]

    comparison = pd.DataFrame(rows)

    comparison.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved ablation table: {OUTPUT_PATH}")
    print()
    print(comparison.to_string(index=False))

    baseline_auc = comparison.loc[
        comparison["feature_set"] == "baseline_features", "roc_auc"
    ].iloc[0]

    enhanced_auc = comparison.loc[
        comparison["feature_set"] == "enhanced_features", "roc_auc"
    ].iloc[0]

    delta = enhanced_auc - baseline_auc

    print()
    print(f"ROC-AUC delta enhanced - baseline: {delta:.6f}")


if __name__ == "__main__":
    main()
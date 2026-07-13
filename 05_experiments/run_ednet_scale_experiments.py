"""
Run EdNet V2 scale experiments.

This script runs the EdNet pipeline at multiple dataset sizes and stores
separate result snapshots for comparison.

Scales:
- 5k pilot
- 50k small
- 200k medium
- 500k max planned V2
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "05_experiments" / "configs" / "ednet_config.yaml"

SCALE_RESULTS_DIR = PROJECT_ROOT / "06_results" / "tables" / "ednet" / "scale_experiments"

PIPELINE_STEPS = [
    PROJECT_ROOT / "04_src" / "data" / "prepare_ednet_subset.py",
    PROJECT_ROOT / "04_src" / "data" / "validate_ednet_dataset.py",
    PROJECT_ROOT / "04_src" / "features" / "build_ednet_features.py",
    PROJECT_ROOT / "04_src" / "models" / "ednet_supervised_baselines.py",
]


SCALES = [
    {
        "scale_name": "ednet_5k_pilot",
        "target_students": 100,
        "target_interactions": 5000,
        "max_interactions_per_student": 100,
    },
    {
        "scale_name": "ednet_50k_small",
        "target_students": 1000,
        "target_interactions": 50000,
        "max_interactions_per_student": 100,
    },
    {
        "scale_name": "ednet_200k_medium",
        "target_students": 4000,
        "target_interactions": 200000,
        "max_interactions_per_student": 120,
    },
    {
        "scale_name": "ednet_500k_max",
        "target_students": 10000,
        "target_interactions": 500000,
        "max_interactions_per_student": 150,
    },
]


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_config(config: dict) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        yaml.safe_dump(config, file, sort_keys=False)


def update_config_for_scale(config: dict, scale: dict) -> dict:
    config = config.copy()
    config["dataset"] = config["dataset"].copy()

    config["dataset"]["target_students"] = scale["target_students"]
    config["dataset"]["target_interactions"] = scale["target_interactions"]
    config["dataset"]["max_interactions_per_student"] = scale[
        "max_interactions_per_student"
    ]

    return config


def run_script(script_path: Path) -> None:
    print("=" * 80)
    print(f"Running: {script_path.relative_to(PROJECT_ROOT)}")

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )


def snapshot_results(scale_name: str) -> dict:
    SCALE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    validation_path = PROJECT_ROOT / "06_results" / "tables" / "ednet" / "ednet_validation_summary.csv"
    feature_path = PROJECT_ROOT / "06_results" / "tables" / "ednet" / "ednet_feature_summary.csv"
    metrics_path = PROJECT_ROOT / "06_results" / "tables" / "ednet" / "ednet_supervised_metrics.csv"

    scale_dir = SCALE_RESULTS_DIR / scale_name
    scale_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy(validation_path, scale_dir / "ednet_validation_summary.csv")
    shutil.copy(feature_path, scale_dir / "ednet_feature_summary.csv")
    shutil.copy(metrics_path, scale_dir / "ednet_supervised_metrics.csv")

    validation = pd.read_csv(validation_path).iloc[0].to_dict()
    metrics = pd.read_csv(metrics_path)

    best_model_row = metrics.sort_values("roc_auc", ascending=False).iloc[0]

    return {
        "scale_name": scale_name,
        "students": int(validation["students"]),
        "questions": int(validation["questions"]),
        "interactions": int(validation["interactions"]),
        "average_correctness": round(float(validation["average_correctness"]), 4),
        "best_model": best_model_row["model"],
        "best_accuracy": round(float(best_model_row["accuracy"]), 4),
        "best_f1": round(float(best_model_row["f1"]), 4),
        "best_roc_auc": round(float(best_model_row["roc_auc"]), 4),
        "best_log_loss": round(float(best_model_row["log_loss"]), 4),
    }


def save_scale_summary(rows: list[dict]) -> None:
    output_path = SCALE_RESULTS_DIR / "ednet_scale_experiment_summary.csv"
    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(output_path, index=False)

    print("\nScale experiment summary saved:")
    print(output_path)
    print(summary_df.to_string(index=False))


def main() -> None:
    original_config = load_config()
    summary_rows = []

    for scale in SCALES:
        scale_name = scale["scale_name"]

        print("\n" + "#" * 80)
        print(f"Starting scale experiment: {scale_name}")
        print("#" * 80)

        scale_config = update_config_for_scale(original_config, scale)
        save_config(scale_config)

        for script_path in PIPELINE_STEPS:
            run_script(script_path)

        summary = snapshot_results(scale_name)
        summary_rows.append(summary)

    save_scale_summary(summary_rows)

    final_config = update_config_for_scale(original_config, SCALES[-1])
    save_config(final_config)

    print("\nAll EdNet scale experiments completed.")


if __name__ == "__main__":
    main()

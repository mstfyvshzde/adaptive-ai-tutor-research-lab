"""
Build learning-history features for the EdNet V2 dataset.

Input:
- 02_data/processed/ednet/ednet_interactions_mapped.csv

Output:
- 02_data/processed/ednet/ednet_features.csv
- 06_results/tables/ednet/ednet_feature_summary.csv

The features are designed to avoid target leakage.
Only previous student/question/topic history is used.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "05_experiments" / "configs" / "ednet_config.yaml"


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_mapped_interactions(config: dict) -> pd.DataFrame:
    input_path = PROJECT_ROOT / config["outputs"]["mapped_interactions"]

    if not input_path.exists():
        raise FileNotFoundError(
            f"Mapped EdNet file not found: {input_path}\n"
            "Run prepare_ednet_subset.py first."
        )

    df = pd.read_csv(input_path)

    required_columns = [
        "student_id",
        "timestamp",
        "question_id",
        "elapsed_time",
        "part",
        "tags",
        "is_correct",
    ]

    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def add_basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["student_id"] = df["student_id"].astype(str)
    df["question_id"] = df["question_id"].astype(str)
    df["part"] = df["part"].astype(str)
    df["tags"] = df["tags"].fillna("unknown").astype(str)

    df["timestamp_sort"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df["elapsed_time"] = pd.to_numeric(df["elapsed_time"], errors="coerce")
    df["elapsed_time"] = df["elapsed_time"].fillna(df["elapsed_time"].median())

    df["is_correct"] = pd.to_numeric(df["is_correct"], errors="coerce").astype(int)

    df["primary_tag"] = df["tags"].str.split(";").str[0].fillna("unknown")

    return df


def add_question_history_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("timestamp_sort").reset_index(drop=True).copy()

    question_group = df.groupby("question_id")["is_correct"]

    df["question_attempt_count_so_far"] = df.groupby("question_id").cumcount()
    df["question_correct_so_far"] = question_group.cumsum() - df["is_correct"]

    df["question_accuracy_so_far"] = (
        df["question_correct_so_far"] / df["question_attempt_count_so_far"]
    )

    df["question_accuracy_so_far"] = df["question_accuracy_so_far"].fillna(0.5)
    df["question_difficulty_estimate"] = 1 - df["question_accuracy_so_far"]

    return df


def add_student_history_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["student_id", "timestamp_sort"]).reset_index(drop=True).copy()

    student_group = df.groupby("student_id")

    df["student_attempt_count"] = student_group.cumcount()
    df["student_correct_so_far"] = (
        student_group["is_correct"].cumsum() - df["is_correct"]
    )

    df["student_accuracy_so_far"] = (
        df["student_correct_so_far"] / df["student_attempt_count"]
    )

    df["student_accuracy_so_far"] = df["student_accuracy_so_far"].fillna(0.5)

    df["previous_correct"] = student_group["is_correct"].shift(1).fillna(0)
    df["previous_elapsed_time"] = (
        student_group["elapsed_time"]
        .shift(1)
        .fillna(df["elapsed_time"].median())
    )

    df["time_since_previous_seconds"] = (
        student_group["timestamp_sort"].diff() / 1000
    ).fillna(0)

    df["rolling_accuracy_5"] = (
        student_group["is_correct"]
        .transform(lambda series: series.shift(1).rolling(5, min_periods=1).mean())
        .fillna(0.5)
    )

    df["rolling_accuracy_10"] = (
        student_group["is_correct"]
        .transform(lambda series: series.shift(1).rolling(10, min_periods=1).mean())
        .fillna(0.5)
    )

    return df


def add_topic_history_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["student_id", "primary_tag", "timestamp_sort"]).copy()

    topic_group = df.groupby(["student_id", "primary_tag"])["is_correct"]

    df["topic_attempt_count_so_far"] = (
        df.groupby(["student_id", "primary_tag"]).cumcount()
    )

    df["topic_correct_so_far"] = topic_group.cumsum() - df["is_correct"]

    df["topic_accuracy_so_far"] = (
        df["topic_correct_so_far"] / df["topic_attempt_count_so_far"]
    )

    df["topic_accuracy_so_far"] = df["topic_accuracy_so_far"].fillna(0.5)

    df = df.sort_values(["student_id", "timestamp_sort"]).reset_index(drop=True)

    return df


def select_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    output_columns = [
        "student_id",
        "question_id",
        "timestamp",
        "part",
        "tags",
        "primary_tag",
        "elapsed_time",
        "time_since_previous_seconds",
        "student_attempt_count",
        "student_accuracy_so_far",
        "previous_correct",
        "previous_elapsed_time",
        "rolling_accuracy_5",
        "rolling_accuracy_10",
        "topic_attempt_count_so_far",
        "topic_accuracy_so_far",
        "question_attempt_count_so_far",
        "question_accuracy_so_far",
        "question_difficulty_estimate",
        "is_correct",
    ]

    return df[output_columns]


def save_feature_dataset(features: pd.DataFrame, config: dict) -> None:
    output_path = PROJECT_ROOT / config["outputs"]["feature_dataset"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_path, index=False)

    print(f"Feature dataset saved to: {output_path}")
    print(f"Rows: {len(features)}")
    print(f"Columns: {len(features.columns)}")


def save_feature_summary(features: pd.DataFrame) -> None:
    output_path = (
        PROJECT_ROOT
        / "06_results"
        / "tables"
        / "ednet"
        / "ednet_feature_summary.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "rows": len(features),
        "columns": len(features.columns),
        "students": features["student_id"].nunique(),
        "questions": features["question_id"].nunique(),
        "average_correctness": round(float(features["is_correct"].mean()), 4),
        "average_student_accuracy_so_far": round(
            float(features["student_accuracy_so_far"].mean()), 4
        ),
        "average_question_difficulty_estimate": round(
            float(features["question_difficulty_estimate"].mean()), 4
        ),
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(output_path, index=False)

    print(f"Feature summary saved to: {output_path}")
    print(summary_df.to_string(index=False))


def main() -> None:
    config = load_config()

    df = load_mapped_interactions(config)
    df = add_basic_cleaning(df)
    df = add_question_history_features(df)
    df = add_student_history_features(df)
    df = add_topic_history_features(df)

    features = select_output_columns(df)

    save_feature_dataset(features, config)
    save_feature_summary(features)


if __name__ == "__main__":
    main()

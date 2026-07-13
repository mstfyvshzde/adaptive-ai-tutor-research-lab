from pathlib import Path
import time

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "02_data/processed/ednet/ednet_features_v2.csv"
OUTPUT_PATH = ROOT / "06_results/tables/ednet/ednet_error_analysis.csv"


def time_based_split(df, test_size=0.2):
    df = df.sort_values("timestamp").reset_index(drop=True)
    split_index = int(len(df) * (1 - test_size))

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    return train_df, test_df


def get_feature_columns(df):
    drop_columns = {
        "is_correct",
        "student_id",
        "question_id",
        "timestamp",
    }

    feature_columns = [col for col in df.columns if col not in drop_columns]

    categorical_columns = [
        col for col in ["part", "primary_tag"]
        if col in feature_columns
    ]

    numeric_columns = [
        col for col in feature_columns
        if col not in categorical_columns
    ]

    return numeric_columns, categorical_columns


def build_pipeline(numeric_columns, categorical_columns):
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_columns),
            ("cat", categorical_pipeline, categorical_columns),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=16,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=-1,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def safe_roc_auc(y_true, y_prob):
    if y_true.nunique() < 2:
        return np.nan

    return roc_auc_score(y_true, y_prob)


def summarize_group(df, group_col, analysis_type):
    rows = []

    for group_value, group_df in df.groupby(group_col, dropna=False):
        rows.append(
            {
                "analysis_type": analysis_type,
                "group": str(group_value),
                "rows": len(group_df),
                "actual_correctness": group_df["is_correct"].mean(),
                "predicted_correctness": group_df["predicted_label"].mean(),
                "accuracy": accuracy_score(group_df["is_correct"], group_df["predicted_label"]),
                "error_rate": group_df["is_error"].mean(),
                "roc_auc": safe_roc_auc(group_df["is_correct"], group_df["predicted_probability"]),
                "avg_confidence": group_df["confidence"].mean(),
            }
        )

    return rows


def add_analysis_buckets(df):
    df = df.copy()

    df["student_history_bucket"] = pd.cut(
        df["student_attempt_count_so_far"],
        bins=[-1, 4, 19, 49, 99, np.inf],
        labels=["0-4", "5-19", "20-49", "50-99", "100+"],
    )

    df["question_history_bucket"] = pd.cut(
        df["question_attempt_count_so_far"],
        bins=[-1, 4, 19, 49, 99, np.inf],
        labels=["0-4", "5-19", "20-49", "50-99", "100+"],
    )

    df["difficulty_bucket"] = pd.cut(
        df["question_difficulty_estimate"],
        bins=[-0.01, 0.25, 0.50, 0.75, 1.01],
        labels=["easy", "medium", "hard", "very_hard"],
    )

    df["confidence_bucket"] = pd.cut(
        df["confidence"],
        bins=[-0.01, 0.10, 0.25, 0.40, 0.51],
        labels=["low", "medium", "high", "very_high"],
    )

    return df


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH, low_memory=False)
    df["is_correct"] = pd.to_numeric(df["is_correct"], errors="coerce").fillna(0).astype(int)

    train_df, test_df = time_based_split(df, test_size=0.2)

    numeric_columns, categorical_columns = get_feature_columns(df)
    feature_columns = numeric_columns + categorical_columns

    X_train = train_df[feature_columns]
    y_train = train_df["is_correct"]

    X_test = test_df[feature_columns]
    y_test = test_df["is_correct"]

    pipeline = build_pipeline(numeric_columns, categorical_columns)

    print(f"Train rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")
    print("Training model for error analysis...")

    start_time = time.time()
    pipeline.fit(X_train, y_train)
    train_seconds = round(time.time() - start_time, 2)

    test_df = test_df.copy()
    test_df["predicted_probability"] = pipeline.predict_proba(X_test)[:, 1]
    test_df["predicted_label"] = (test_df["predicted_probability"] >= 0.5).astype(int)
    test_df["is_error"] = (test_df["is_correct"] != test_df["predicted_label"]).astype(int)
    test_df["confidence"] = (test_df["predicted_probability"] - 0.5).abs()

    metrics = {
        "accuracy": accuracy_score(y_test, test_df["predicted_label"]),
        "f1": f1_score(y_test, test_df["predicted_label"], zero_division=0),
        "roc_auc": roc_auc_score(y_test, test_df["predicted_probability"]),
        "log_loss": log_loss(y_test, test_df["predicted_probability"], labels=[0, 1]),
        "train_seconds": train_seconds,
    }

    test_df = add_analysis_buckets(test_df)

    rows = []
    rows.extend(summarize_group(test_df, "part", "by_part"))
    rows.extend(summarize_group(test_df, "student_history_bucket", "by_student_history"))
    rows.extend(summarize_group(test_df, "question_history_bucket", "by_question_history"))
    rows.extend(summarize_group(test_df, "difficulty_bucket", "by_question_difficulty"))
    rows.extend(summarize_group(test_df, "confidence_bucket", "by_model_confidence"))

    analysis = pd.DataFrame(rows)
    analysis = analysis.sort_values(["analysis_type", "error_rate"], ascending=[True, False])

    analysis.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved error analysis: {OUTPUT_PATH}")

    print("\nModel check:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    print("\nHighest error groups:")
    print(
        analysis[
            ["analysis_type", "group", "rows", "actual_correctness", "accuracy", "error_rate", "roc_auc"]
        ]
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()

from pathlib import Path
import time

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "02_data/processed/ednet/ednet_features_v2.csv"
OUTPUT_PATH = ROOT / "06_results/tables/ednet/ednet_feature_importance.csv"


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

    print(f"Train rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")
    print(f"Features: {len(feature_columns)}")

    pipeline = build_pipeline(numeric_columns, categorical_columns)

    start_time = time.time()
    pipeline.fit(X_train, y_train)
    train_seconds = round(time.time() - start_time, 2)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "log_loss": log_loss(y_test, probabilities, labels=[0, 1]),
        "train_seconds": train_seconds,
    }

    importances = pipeline.named_steps["model"].feature_importances_

    importance_df = pd.DataFrame(
        {
            "feature": feature_columns,
            "importance": importances,
        }
    ).sort_values("importance", ascending=False)

    importance_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved feature importance: {OUTPUT_PATH}")

    print("\nModel check:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    print("\nTop 20 features:")
    print(importance_df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()

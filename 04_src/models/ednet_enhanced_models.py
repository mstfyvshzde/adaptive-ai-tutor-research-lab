from pathlib import Path
import time

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, log_loss, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "02_data/processed/ednet/ednet_features_v2.csv"
CONFIG_PATH = ROOT / "05_experiments/configs/ednet_config.yaml"
OUTPUT_PATH = ROOT / "06_results/tables/ednet/ednet_enhanced_supervised_metrics.csv"


def find_test_size(config):
    if isinstance(config, dict):
        for key, value in config.items():
            if key == "test_size":
                return float(value)

            found = find_test_size(value)
            if found is not None:
                return found

    if isinstance(config, list):
        for item in config:
            found = find_test_size(item)
            if found is not None:
                return found

    return None


def load_test_size(default=0.2):
    if not CONFIG_PATH.exists():
        return default

    try:
        import yaml

        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        test_size = find_test_size(config)
        return test_size if test_size is not None else default

    except Exception:
        return default


def make_one_hot_encoder():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def time_based_split(df, test_size):
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


def build_preprocessor(numeric_columns, categorical_columns, scale_numeric=False):
    if scale_numeric:
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
    else:
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
            ]
        )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", make_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_columns),
            ("cat", categorical_pipeline, categorical_columns),
        ],
        remainder="drop",
    )


def get_models():
    return {
        "dummy_majority": DummyClassifier(strategy="most_frequent"),

        "logistic_regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            n_jobs=-1,
        ),

        "random_forest": RandomForestClassifier(
            n_estimators=120,
            max_depth=16,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1,
        ),

        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=120,
            learning_rate=0.06,
            max_depth=3,
            random_state=42,
        ),

        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=180,
            learning_rate=0.06,
            max_leaf_nodes=31,
            random_state=42,
        ),
    }


def evaluate_model(name, model, X_train, y_train, X_test, y_test, numeric_columns, categorical_columns):
    scale_numeric = name == "logistic_regression"

    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(numeric_columns, categorical_columns, scale_numeric)),
            ("model", model),
        ]
    )

    start_time = time.time()
    pipeline.fit(X_train, y_train)
    train_seconds = round(time.time() - start_time, 2)

    predictions = pipeline.predict(X_test)

    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba(X_test)[:, 1]
    else:
        probabilities = predictions

    return {
        "model": name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "log_loss": log_loss(y_test, probabilities, labels=[0, 1]),
        "train_seconds": train_seconds,
    }


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    test_size = load_test_size(default=0.2)

    print(f"Reading: {INPUT_PATH}")
    print(f"Using test_size: {test_size}")

    df = pd.read_csv(INPUT_PATH, low_memory=False)

    df["is_correct"] = pd.to_numeric(df["is_correct"], errors="coerce").fillna(0).astype(int)

    train_df, test_df = time_based_split(df, test_size)

    numeric_columns, categorical_columns = get_feature_columns(df)
    feature_columns = numeric_columns + categorical_columns

    X_train = train_df[feature_columns]
    y_train = train_df["is_correct"]

    X_test = test_df[feature_columns]
    y_test = test_df["is_correct"]

    print(f"Train rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")
    print(f"Numeric features: {len(numeric_columns)}")
    print(f"Categorical features: {categorical_columns}")

    results = []

    for name, model in get_models().items():
        print(f"\nTraining: {name}")

        result = evaluate_model(
            name=name,
            model=model,
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
        )

        results.append(result)

        print(
            f"{name} | "
            f"accuracy={result['accuracy']:.4f} | "
            f"f1={result['f1']:.4f} | "
            f"roc_auc={result['roc_auc']:.4f} | "
            f"log_loss={result['log_loss']:.4f}"
        )

    metrics = pd.DataFrame(results)
    metrics = metrics.sort_values("roc_auc", ascending=False)

    metrics.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved metrics: {OUTPUT_PATH}")
    print("\nBest models:")
    print(metrics[["model", "accuracy", "f1", "roc_auc", "log_loss", "train_seconds"]].to_string(index=False))


if __name__ == "__main__":
    main()
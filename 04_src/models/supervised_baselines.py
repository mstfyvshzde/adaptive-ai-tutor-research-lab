"""
Train supervised baseline models for knowledge tracing.

This script uses the feature dataset created by build_features.py.

Goal:
Predict whether a student will answer a question correctly.

Target:
is_correct

This is the first real machine learning step of the project.
"""

from pathlib import Path
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


INPUT_PATH = Path("02_data/processed/demo_features.csv")
OUTPUT_DIR = Path("06_results/tables")
OUTPUT_PATH = OUTPUT_DIR / "supervised_baseline_metrics.csv"

RANDOM_SEED = 17
TARGET_COLUMN = "is_correct"


NUMERIC_FEATURES = [
    "difficulty_score",
    "elapsed_time",
    "student_attempt_count",
    "student_accuracy_so_far",
    "previous_correct",
    "previous_elapsed_time",
    "rolling_accuracy_5",
    "rolling_accuracy_10",
    "time_since_previous_seconds",
    "topic_attempt_count_so_far",
    "topic_accuracy_so_far",
    "question_attempt_count_so_far",
    "question_accuracy_so_far",
    "question_difficulty_estimate",
]


CATEGORICAL_FEATURES = [
    "part",
    "tags",
    "difficulty",
]


def load_features(path: Path) -> pd.DataFrame:
    """Load the feature dataset."""

    if not path.exists():
        raise FileNotFoundError(
            f'mising feature file {path}. run build_feature.py first'
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    return dataframe


def create_time_based_split(
        dataframe: pd.DataFrame,
        train_ratio: float = 0.8
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data by time to make evaluation more realistic."""

    dataframe = dataframe.sort_values('timestamp').reset_index(drop=True)

    split_index = int(len(dataframe) * train_ratio)

    train_df = dataframe.iloc[:split_index].copy()
    test_df = dataframe.iloc[split_index:].copy()

    return train_df, test_df


def build_preprocessor() -> ColumnTransformer:
    """Create preprocessing steps for numeric and categorical features."""

    numeric_transformer = Pipeline(
        steps=[
            ('scaler', StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'))
        ]
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, NUMERIC_FEATURES),
            ('categorical', categorical_transformer, CATEGORICAL_FEATURES)
        ]
    )

    return preprocessor


def build_models() -> dict:
    """Create supervised baseline models."""

    preprocessor = build_preprocessor()

    models = {
        'majority_class_baseline': DummyClassifier(strategy='most_frequent'),
        'logistic_regression': Pipeline(
            steps=[
                ('preprocessor', preprocessor),
                (
                    'model',
                    LogisticRegression(
                        max_iter=1000,
                        random_state=RANDOM_SEED
                    )
                )
            ]
        ),
        'random_forest': Pipeline(
            steps=[
                ('preprocessor', preprocessor),
                (
                    'model', 
                    RandomForestClassifier(
                        n_estimators=150,
                        max_depth=8,
                        random_state=RANDOM_SEED,
                        n_jobs=-1
                    )
                )
            ]
        ),
        'gradient_boosting': Pipeline(
            steps=[
                ('preprocessor', preprocessor),
                (
                    'model',
                    GradientBoostingClassifier(
                        random_state=RANDOM_SEED
                    )
                )
            ]
        )
    }

    return models


def safe_roc_auc(y_true: pd.Series, y_probability: list[float]) -> None:
    """Calculate ROC-AUC safely."""

    if y_true.nunique() < 2:
        return float('nan')
    
    return float(roc_auc_score(y_true, y_probability))
# Model doğru cevapları ve yanlış cevapları ne kadar iyi ayırıyor, onu ölçüyor.
# y_true -> gerçek sonuçlar: doğru mu yanlış mı?
# y_probability -> modelin “doğru olur” ihtimali tahmini
# roc_auc_score -> bu ayrımı puanlıyor


def evaluate_model(
    model_name: str,
    model,
    x_train: pd.DataFrame, # feature tablosu oldugu icin dataframe
    y_train: pd.Series, # colon oldugu icin series
    x_test: pd.DataFrame,
    y_test: pd.Series
) -> dict:
    """Train and evaluate one model."""

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    if hasattr(model, 'predict_proba'):
        y_probability = model.predict_proba(x_test)[:, 1]
    else:
        y_probability = y_pred
    # Bu kod modelden doğru cevaplama ihtimali almaya çalışıyor. Model ihtimal verebiliyorsa % doğru yapma ihtimali alınır; veremiyorsa normal 0/1 tahmini kullanılır.


    metrics = {
        "model": model_name,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": safe_roc_auc(y_test, y_probability),
        "log_loss": log_loss(y_test, y_probability, labels=[0, 1]),
    }

    return metrics


def train_and_evaluate_models(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Train and evaluate all supervised baseline models."""

    train_df, test_df = create_time_based_split(dataframe)

    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    x_train = train_df[feature_columns]
    y_train = train_df[TARGET_COLUMN]

    x_test = test_df[feature_columns]
    y_test = test_df[TARGET_COLUMN]

    models = build_models()
    results = []

    for model_name, model in models.items():
        print(f"Training model: {model_name}")

        metrics = evaluate_model(
            model_name=model_name,
            model=model,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test
        )

        results.append(metrics)

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by='roc_auc', ascending=False)

    return results_df


def main() -> None:
    """Run supervised baseline training."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = load_features(INPUT_PATH)
    results_df = train_and_evaluate_models(dataframe)

    results_df.to_csv(OUTPUT_PATH, index=False)

    print("\nSupervised baseline results:")
    print(results_df.round(4))
    print(f"\nSaved results to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


# # ------------------------------------------------------------
# # NOTES
# # ------------------------------------------------------------

# # This file trains the first supervised machine learning models.

# # Main goal:
# # Predict is_correct.

# # is_correct means:
# # - 1 = student answered correctly
# # - 0 = student answered incorrectly

# # Why this matters:
# # This is the first knowledge tracing baseline.
# # The model learns from student history and question features.

# # Input:
# # 02_data/processed/demo_features.csv

# # Output:
# # 06_results/tables/supervised_baseline_metrics.csv

# # Models:
# # - majority_class_baseline
# # - logistic_regression
# # - random_forest
# # - gradient_boosting

# # majority_class_baseline:
# # Always predicts the most common class.
# # Real models should beat this baseline.

# # logistic_regression:
# # Simple and interpretable baseline.

# # random_forest:
# # Tree-based model that can capture non-linear patterns.

# # gradient_boosting:
# # Stronger tree-based baseline.

# # Important evaluation idea:
# # We use a time-based split.
# # Older interactions are used for training.
# # Later interactions are used for testing.

# # This is more realistic than random splitting for learning data.

# # Important research idea:
# # We do not only care about accuracy.
# # ROC-AUC and Log Loss matter because the tutor needs reliable probability estimates.

# # If this script works:
# # The project has its first real ML experiment.
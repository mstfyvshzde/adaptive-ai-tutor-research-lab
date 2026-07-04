"""
Build modeling features for the Adaptive AI Tutor Research Lab.

This script takes the validated demo interaction dataset and creates
machine learning features for knowledge tracing.

The main goal is to predict:

Will the student answer the current question correctly?

Important rule:
Features must be created from past information only.
This helps avoid data leakage.
"""


from pathlib import Path
import pandas as pd

INPUT_PATH = Path("07_demo/demo_data/demo_interactions.csv")
OUTPUT_DIR = Path("02_data/processed")
OUTPUT_PATH = OUTPUT_DIR / "demo_features.csv"


def load_interactions(path: Path) -> pd.DataFrame:
    """Load demo interactions and sort by student and time."""

    if not path.exists():
        raise FileNotFoundError(
            f'missing file: {path}. run create_demo_datset.py first'
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    dataframe = dataframe.sort_values(
        by=['student_id', 'timestamp']
    ).reset_index(drop=True)

    return dataframe

def add_student_history_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add features based only on each student's past performance."""

    dataframe = dataframe.copy()

    dataframe["student_attempt_count"] = dataframe.groupby("student_id").cumcount()

    dataframe["student_correct_so_far"] = (
        dataframe.groupby("student_id")["is_correct"]
        .transform(lambda values: values.shift(1).cumsum())
        .fillna(0)
    )

    dataframe["student_accuracy_so_far"] = (
        dataframe["student_correct_so_far"]
        / dataframe["student_attempt_count"].replace(0, pd.NA)
    ).fillna(0.5)

    dataframe["previous_correct"] = (
        dataframe.groupby("student_id")["is_correct"]
        .shift(1)
        .fillna(0.5)
    )

    dataframe["previous_elapsed_time"] = (
        dataframe.groupby("student_id")["elapsed_time"]
        .shift(1)
        .fillna(dataframe["elapsed_time"].median())
    )

    return dataframe



def add_rolling_accuracy_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add recent accuracy features for each student."""

    dataframe = dataframe.copy()

    dataframe["rolling_accuracy_5"] = (
        dataframe.groupby("student_id")["is_correct"]
        .transform(lambda values: values.shift(1).rolling(5, min_periods=1).mean())
        .fillna(0.5)
    )

    dataframe["rolling_accuracy_10"] = (
        dataframe.groupby("student_id")["is_correct"]
        .transform(lambda values: values.shift(1).rolling(10, min_periods=1).mean())
        .fillna(0.5)
    )

    return dataframe


def add_time_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add time gap features between student interactions."""

    dataframe = dataframe.copy()

    dataframe["previous_timestamp"] = dataframe.groupby("student_id")[
        "timestamp"
    ].shift(1)

    dataframe["time_since_previous_seconds"] = (
        dataframe["timestamp"] - dataframe["previous_timestamp"]
    ).dt.total_seconds()

    dataframe["time_since_previous_seconds"] = dataframe[
        "time_since_previous_seconds"
    ].fillna(0)

    dataframe = dataframe.drop(columns=["previous_timestamp"])

    return dataframe


def add_topic_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add student-topic history features without using future information."""

    dataframe = dataframe.copy()

    group_columns = ["student_id", "tags"]

    dataframe["topic_attempt_count_so_far"] = dataframe.groupby(
        group_columns
    ).cumcount()

    dataframe["topic_correct_so_far"] = (
        dataframe.groupby(group_columns)["is_correct"]
        .transform(lambda values: values.shift(1).cumsum())
        .fillna(0)
    )

    dataframe["topic_accuracy_so_far"] = (
        dataframe["topic_correct_so_far"]
        / dataframe["topic_attempt_count_so_far"].replace(0, pd.NA)
    ).fillna(0.5)

    return dataframe


def add_question_history_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add question-level history features using only previous attempts."""

    dataframe = dataframe.copy()
    dataframe = dataframe.sort_values(by=["timestamp"]).reset_index(drop=True)

    dataframe["question_attempt_count_so_far"] = dataframe.groupby(
        "question_id"
    ).cumcount()

    dataframe["question_correct_so_far"] = (
        dataframe.groupby("question_id")["is_correct"]
        .transform(lambda values: values.shift(1).cumsum())
        .fillna(0)
    )

    dataframe["question_accuracy_so_far"] = (
        dataframe["question_correct_so_far"]
        / dataframe["question_attempt_count_so_far"].replace(0, pd.NA)
    ).fillna(0.5)

    dataframe["question_difficulty_estimate"] = (
        1 - dataframe["question_accuracy_so_far"]
    )

    dataframe = dataframe.sort_values(
        by=["student_id", "timestamp"]
    ).reset_index(drop=True)

    return dataframe


def select_modeling_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Select the final columns for the first modeling dataset."""

    selected_columns = [
        "student_id",
        "question_id",
        "timestamp",
        "part",
        "tags",
        "difficulty",
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
        "is_correct",
    ]

    return dataframe[selected_columns]


def build_features() -> pd.DataFrame:
    """Run the full feature engineering pipeline."""

    dataframe = load_interactions(INPUT_PATH)

    dataframe = add_student_history_features(dataframe)
    dataframe = add_rolling_accuracy_features(dataframe)
    dataframe = add_time_features(dataframe)
    dataframe = add_topic_features(dataframe)
    dataframe = add_question_history_features(dataframe)

    features_df = select_modeling_columns(dataframe)

    return features_df


def main() -> None:
    """Build and save the feature dataset."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    features_df = build_features()
    features_df.to_csv(OUTPUT_PATH, index=False)

    print("Feature dataset created successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Rows: {len(features_df)}")
    print(f"Columns: {len(features_df.columns)}")
    print(f"Average target correctness: {features_df['is_correct'].mean():.3f}")


if __name__ == "__main__":
    main()


# # ------------------------------------------------------------
# # NOTES
# # ------------------------------------------------------------

# # This file creates the first machine learning feature dataset.
# # It uses demo_interactions.csv and saves demo_features.csv.

# # Main idea:
# # Raw interaction data is not enough for modeling.
# # We need features that describe the student's past behavior.

# # Important target:
# # is_correct is the value we want to predict.

# # Important rule:
# # Features must use only past information.
# # We should not use future answers to predict current answers.

# # Main feature groups:
# # - student history features
# # - rolling accuracy features
# # - time gap features
# # - topic-level features
# # - question-level features

# # student_accuracy_so_far:
# # Shows how well the student performed before the current question.

# # rolling_accuracy_5:
# # Shows recent student performance over the last 5 questions.

# # topic_accuracy_so_far:
# # Shows how well the student performed in the same topic before now.

# # question_difficulty_estimate:
# # Estimates question difficulty from previous student attempts.

# # Why this file matters:
# # This is the bridge between raw data and machine learning models.
# # Without good feature engineering, the model will not understand student behavior well.
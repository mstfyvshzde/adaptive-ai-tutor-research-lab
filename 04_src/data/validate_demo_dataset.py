"""
Validate the demo dataset for the Adaptive AI Tutor Research Lab.

This script checks whether the generated demo dataset has the expected structure.
It helps us catch data problems before moving to preprocessing and modeling.
"""

from pathlib import Path

import pandas as pd

INTERACTIONS_PATH = Path("07_demo/demo_data/demo_interactions.csv")
QUESTIONS_PATH = Path("07_demo/demo_data/demo_questions.csv")


REQUIRED_INTERACTION_COLUMNS = [
    "student_id",
    "timestamp",
    "solving_id",
    "question_id",
    "user_answer",
    "correct_answer",
    "elapsed_time",
    "part",
    "tags",
    "difficulty",
    "difficulty_score",
    "is_correct",
]


REQUIRED_QUESTION_COLUMNS = [
    "question_id",
    "part",
    "tags",
    "difficulty",
    "difficulty_score",
    "correct_answer",
]


def check_file_exists(path: Path) -> None:
    """Check whether a dataset file exists."""

    if not path.exists():
        raise FileNotFoundError(
            f'missing file: {path}. run create_demo_dataset.py first'
        )


def check_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
    dataset_name: str
) -> None:
    """Check whether all required columns exist."""

    missing_columns = [
        column for column in required_columns if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f'{dataset_name} is missing required column: {missing_columns}'
        )
    
def check_missing_values(dataframe: pd.DataFrame, dataset_name: str) -> None:
    """Check whether the dataset contains missing values."""
    missing_counts = dataframe.isna().sum()
    missing_counts = missing_counts[missing_counts > 0]

    if not missing_counts.empty:
        raise ValueError(
            f'{dataset_name} contains missing values: \n{missing_counts}'
        )
    

def check_correctness_column(interactions_df: pd.DataFrame) -> None:
    """Check whether is_correct was calculated correctly."""
    expected_is_correct = (
        interactions_df['user_answer'] == interactions_df['correct_answer']
    ).astype(int)

    mismatches = interactions_df[
        interactions_df['is_correct'] != expected_is_correct
    ]

    if not mismatches.empty:
        raise ValueError(
            f'is correct has {len(mismatches)} incorrect rows'
        )
    
def check_timestamp_order(interactions_df: pd.DataFrame) -> None:
    """Check whether each student's interactions are sorted by timestamp."""
    
    interactions_df = interactions_df.copy()
    interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'])

    sorted_df = interactions_df.sort_values(
        by=['student_id', 'timestamp']
    ).reset_index(drop=True)

    original_df = interactions_df.reset_index(drop=True)

    if not original_df[['student_id', 'timestamp']].equals(
        sorted_df[['student_id', 'timestamp']]
    ):
        raise ValueError(
            'interactions are not sorted by student_id and timestamp'
        )


def check_question_links(
    interactions_df: pd.DataFrame,
    question_df: pd.DataFrame
) -> None:
    """Check whether every interaction question exists in question metadata."""

    interaction_question_ids = set(interactions_df['question_id'].unique())
    metadata_question_ids = set(question_df['question_id'].unique())

    missing_question_ids = interaction_question_ids - metadata_question_ids

    if missing_question_ids:
        raise ValueError(
            f"Some interaction question IDs are missing from metadata: "
            f"{sorted(missing_question_ids)[:10]}"
        )


def print_summary(
    interactions_df: pd.DataFrame,
    questions_df: pd.DataFrame,
) -> None:
    """Print a short dataset summary."""

    print("Demo dataset validation passed.")
    print(f"Number of students: {interactions_df['student_id'].nunique()}")
    print(f"Number of questions in metadata: {len(questions_df)}")
    print(f"Number of used questions: {interactions_df['question_id'].nunique()}")
    print(f"Number of interactions: {len(interactions_df)}")
    print(f"Average correctness: {interactions_df['is_correct'].mean():.3f}")
    print(f"Average elapsed time: {interactions_df['elapsed_time'].mean():.1f} ms")


def main() -> None:
    """Run all validation checks."""

    check_file_exists(INTERACTIONS_PATH)
    check_file_exists(QUESTIONS_PATH)

    interactions_df = pd.read_csv(INTERACTIONS_PATH)
    questions_df = pd.read_csv(QUESTIONS_PATH)

    check_required_columns(
        dataframe=interactions_df,
        required_columns=REQUIRED_INTERACTION_COLUMNS,
        dataset_name="demo_interactions.csv",
    )

    check_required_columns(
        dataframe=questions_df,
        required_columns=REQUIRED_QUESTION_COLUMNS,
        dataset_name="demo_questions.csv",
    )

    check_missing_values(interactions_df, "demo_interactions.csv")
    check_missing_values(questions_df, "demo_questions.csv")
    check_correctness_column(interactions_df)
    check_timestamp_order(interactions_df)
    check_question_links(interactions_df, questions_df)

    print_summary(interactions_df, questions_df)


if __name__ == "__main__":
    main()


# # ------------------------------------------------------------
# # NOTES
# # ------------------------------------------------------------

# # This file validates the demo dataset created by create_demo_dataset.py.
# # It checks whether the generated CSV files are usable before modeling.

# # Main checks:
# # - Required files exist
# # - Required columns exist
# # - No missing values
# # - is_correct is calculated correctly
# # - Student histories are sorted by timestamp
# # - Every interaction question_id exists in question metadata

# # Why this matters:
# # Bad data creates bad models.
# # Before feature engineering or model training, we need to make sure the dataset is clean.

# # Important project idea:
# # This validation step protects the research pipeline.
# # If the data is wrong, later results cannot be trusted.

# # In professional ML projects:
# # Data validation is not optional.
# # It is one of the first serious steps before training models.
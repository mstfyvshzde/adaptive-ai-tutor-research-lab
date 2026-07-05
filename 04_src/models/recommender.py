"""
Recommendation baselines for the Adaptive AI Tutor Research Lab.

This script creates simple next-question recommendation baselines.

Goal:
Recommend a next learning activity for each student.

Baselines:
- Random recommendation
- Difficulty-based recommendation
- Weak-topic recommendation

Input:
02_data/processed/demo_features.csv

Outputs:
06_results/tables/recommendation_examples.csv
06_results/tables/recommender_baseline_metrics.csv
"""

from pathlib import Path

import numpy as np 
import pandas as pd


INPUT_PATH = Path("02_data/processed/demo_features.csv")

OUTPUT_TABLE_DIR = Path("06_results/tables")
RECOMMENDATION_EXAMPLES_PATH = OUTPUT_TABLE_DIR / "recommendation_examples.csv"
RECOMMENDER_METRICS_PATH = OUTPUT_TABLE_DIR / "recommender_baseline_metrics.csv"

RANDOM_SEED = 17


def load_features(path: Path) -> pd.DataFrame:
    """Load feature dataset."""

    if not path.exists():
        raise FileNotFoundError(
            f'missing feature file: {path}. run build_fatures.py first'
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    return dataframe


def build_question_bank(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create a clean question bank from interaction data."""

    question_bank = (
        dataframe.groupby('question_id')
        .agg(
            part=('part', 'first'),
            tags=('tags', 'first'),
            difficulty=('difficulty', 'first'),
            difficulty_score=('difficulty_score', 'mean'),
            historical_accuracy = ('is_correct', 'mean'),
            attemp_count=('is_correct', 'count')
        )
        .reset_index()
    )

    return question_bank



def calculate_recent_accuracy(student_df: pd.DataFrame, window_size: int = 5) -> float:
    """Calculate recent accuracy for one student."""

    recent_answers = student_df.sort_values("timestamp").tail(window_size)

    return float(recent_answers["is_correct"].mean())


def find_weak_topic(student_df: pd.DataFrame) -> str:
    """Find the topic where the student has the lowest accuracy."""

    topic_accuracy = student_df.groupby("tags")["is_correct"].mean()

    return str(topic_accuracy.idxmin())


def build_student_profiles(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create student profiles for recommendation."""

    student_rows = []

    for student_id, student_df in dataframe.groupby("student_id"):
        student_rows.append(
            {
                "student_id": student_id,
                "student_accuracy": float(student_df["is_correct"].mean()),
                "student_recent_accuracy": calculate_recent_accuracy(student_df),
                "student_attempt_count": len(student_df),
                "weak_topic": find_weak_topic(student_df),
            }
        )

    return pd.DataFrame(student_rows)


def sample_question(
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    """Sample one question from a question bank."""

    selected_question = question_bank.sample(
        1,
        random_state=int(rng.integers(0, 1_000_000)),
    ).iloc[0]

    return selected_question.to_dict()


def recommend_random(
    student_profile: pd.Series,
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    """Recommend a random question."""

    question = sample_question(question_bank, rng)

    return {
        "student_id": student_profile["student_id"],
        "method": "random",
        "recommended_question_id": question["question_id"],
        "recommended_topic": question["tags"],
        "recommended_difficulty": question["difficulty"],
        "difficulty_score": question["difficulty_score"],
        "weak_topic": student_profile["weak_topic"],
        "reason": "Randomly selected question.",
    }


def choose_target_difficulty(student_recent_accuracy: float) -> str:
    """Choose target difficulty based on recent student accuracy."""

    if student_recent_accuracy < 0.55:
        return "easy"

    if student_recent_accuracy < 0.75:
        return "medium"

    return "hard"


def recommend_difficulty_based(
    student_profile: pd.Series,
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    """Recommend a question based on student recent accuracy."""

    target_difficulty = choose_target_difficulty(
        student_profile["student_recent_accuracy"]
    )

    candidates = question_bank[question_bank["difficulty"] == target_difficulty]

    if candidates.empty:
        candidates = question_bank

    question = sample_question(candidates, rng)

    return {
        "student_id": student_profile["student_id"],
        "method": "difficulty_based",
        "recommended_question_id": question["question_id"],
        "recommended_topic": question["tags"],
        "recommended_difficulty": question["difficulty"],
        "difficulty_score": question["difficulty_score"],
        "weak_topic": student_profile["weak_topic"],
        "reason": (
            f"Student recent accuracy is "
            f"{student_profile['student_recent_accuracy']:.2f}, "
            f"so the system selected a {target_difficulty} question."
        ),
    }


def recommend_weak_topic(
    student_profile: pd.Series,
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    """Recommend a question from the student's weakest topic."""

    weak_topic = student_profile["weak_topic"]
    candidates = question_bank[question_bank["tags"] == weak_topic]

    if candidates.empty:
        candidates = question_bank

    target_difficulty = choose_target_difficulty(
        student_profile["student_recent_accuracy"]
    )

    difficulty_candidates = candidates[
        candidates["difficulty"] == target_difficulty
    ]

    if not difficulty_candidates.empty:
        candidates = difficulty_candidates

    question = sample_question(candidates, rng)

    return {
        "student_id": student_profile["student_id"],
        "method": "weak_topic",
        "recommended_question_id": question["question_id"],
        "recommended_topic": question["tags"],
        "recommended_difficulty": question["difficulty"],
        "difficulty_score": question["difficulty_score"],
        "weak_topic": weak_topic,
        "reason": (
            f"The student's weakest topic is {weak_topic}. "
            f"The system recommended a {question['difficulty']} question "
            f"from this topic."
        ),
    }


def estimate_recommendation_quality(
    recommendation: dict,
    student_profile: pd.Series,
) -> dict:
    """Create simple proxy metrics for recommendation quality."""

    student_recent_accuracy = float(student_profile["student_recent_accuracy"])
    difficulty_score = float(recommendation["difficulty_score"])

    predicted_success_probability = (
        student_recent_accuracy - difficulty_score + 0.55
    )

    predicted_success_probability = float(
        np.clip(predicted_success_probability, 0.05, 0.95)
    )

    ideal_difficulty = float(np.clip(student_recent_accuracy, 0.20, 0.85))

    challenge_match = 1 - abs(difficulty_score - ideal_difficulty)
    challenge_match = float(np.clip(challenge_match, 0.0, 1.0))

    weak_topic_match = int(
        recommendation["recommended_topic"] == student_profile["weak_topic"]
    )

    proxy_learning_value = (
        0.50 * predicted_success_probability
        + 0.30 * challenge_match
        + 0.20 * weak_topic_match
    )

    return {
        "predicted_success_probability": predicted_success_probability,
        "challenge_match": challenge_match,
        "weak_topic_match": weak_topic_match,
        "proxy_learning_value": proxy_learning_value,
    }


def create_recommendations(
    student_profiles_df: pd.DataFrame,
    question_bank: pd.DataFrame,
) -> pd.DataFrame:
    """Create recommendations for each student using all baseline methods."""

    rng = np.random.default_rng(RANDOM_SEED)

    recommendation_rows = []

    for _, student_profile in student_profiles_df.iterrows():
        recommendations = [
            recommend_random(student_profile, question_bank, rng),
            recommend_difficulty_based(student_profile, question_bank, rng),
            recommend_weak_topic(student_profile, question_bank, rng),
        ]

        for recommendation in recommendations:
            quality = estimate_recommendation_quality(
                recommendation=recommendation,
                student_profile=student_profile,
            )

            recommendation.update(quality)
            recommendation_rows.append(recommendation)

    return pd.DataFrame(recommendation_rows)


def summarize_recommendation_methods(
    recommendations_df: pd.DataFrame,
) -> pd.DataFrame:
    """Create summary metrics for each recommendation method."""

    summary_df = (
        recommendations_df.groupby("method")
        .agg(
            avg_predicted_success_probability=(
                "predicted_success_probability",
                "mean",
            ),
            avg_challenge_match=("challenge_match", "mean"),
            weak_topic_match_rate=("weak_topic_match", "mean"),
            avg_proxy_learning_value=("proxy_learning_value", "mean"),
        )
        .round(3)
        .reset_index()
    )

    return summary_df


def main() -> None:
    """Run recommender baseline generation."""

    OUTPUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = load_features(INPUT_PATH)

    question_bank = build_question_bank(dataframe)
    student_profiles_df = build_student_profiles(dataframe)

    recommendations_df = create_recommendations(
        student_profiles_df=student_profiles_df,
        question_bank=question_bank,
    )

    summary_df = summarize_recommendation_methods(recommendations_df)

    recommendations_df.to_csv(RECOMMENDATION_EXAMPLES_PATH, index=False)
    summary_df.to_csv(RECOMMENDER_METRICS_PATH, index=False)

    print("Recommendation baselines completed successfully.")
    print(f"Recommendation examples saved to: {RECOMMENDATION_EXAMPLES_PATH}")
    print(f"Recommender metrics saved to: {RECOMMENDER_METRICS_PATH}")
    print("\nMethod summary:")
    print(summary_df)


if __name__ == "__main__":
    main()


# # ------------------------------------------------------------
# # NOTES
# # ------------------------------------------------------------

# # This file creates the first recommendation baselines.

# # Main goal:
# # Recommend the next question or activity for each student.

# # Input:
# # 02_data/processed/demo_features.csv

# # Outputs:
# # recommendation_examples.csv
# # recommender_baseline_metrics.csv

# # Baseline 1:
# # random
# # Selects a random question.
# # This is the weakest baseline.

# # Baseline 2:
# # difficulty_based
# # Selects easy, medium, or hard questions based on recent student accuracy.

# # Baseline 3:
# # weak_topic
# # Finds the student's weakest topic and recommends a question from that topic.

# # Why recommender systems matter:
# # Knowledge tracing predicts performance.
# # Recommendation decides what the student should do next.

# # Important idea:
# # Educational recommendation is different from movie recommendation.
# # The goal is not only preference.
# # The goal is learning improvement.

# # Proxy metrics:
# # predicted_success_probability:
# # Estimated chance that the student can answer the recommended question correctly.

# # challenge_match:
# # Measures whether the difficulty is suitable for the student.

# # weak_topic_match:
# # Checks whether the recommendation targets the student's weak topic.

# # proxy_learning_value:
# # A simple combined score for demo evaluation.
# # This is not a final real-world learning metric.
# # It is only a first proxy metric for testing the recommendation pipeline.

# # Research warning:
# # Final results must come from real experiments.
# # These proxy metrics are useful for testing the pipeline before real evaluation.
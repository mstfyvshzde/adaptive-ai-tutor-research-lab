"""
Create a small demo dataset for the Adaptive AI Tutor Research Lab.

This script creates synthetic student-question interaction data.
The purpose is not to replace the real EdNet dataset.

The purpose is to test the full project pipeline before working with large real data.
"""

from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


RANDOM_SEED = 17
NUM_STUDENTS = 40
NUM_QUESTIONS = 80
MIN_INTERACTIONS_PER_STUDENT = 25
MAX_INTERACTIONS_PER_STUDENT = 45

OUTPUT_DIR = Path("07_demo/demo_data")
INTERACTIONS_PATH = OUTPUT_DIR / "demo_interactions.csv"
QUESTIONS_PATH = OUTPUT_DIR / "demo_questions.csv"


def create_question_metadata(rng: np.random.Generator) -> pd.DataFrame:
    """Create synthetic question metadata."""

    topics = [
        "algebra",
        "geometry",
        "probability",
        "statistics",
        "functions",
        "logic",
    ]

    questions = []

    for question_id in range(1, NUM_QUESTIONS + 1):
        topic = rng.choice(topics)
        difficulty = rng.choice(["easy", "medium", "hard"], p=[0.35, 0.45, 0.20])
        correct_answer = int(rng.integers(1, 5))

        if difficulty == "easy":
            difficulty_score = rng.uniform(0.15, 0.35)
        elif difficulty == "medium":
            difficulty_score = rng.uniform(0.36, 0.65)
        else:
            difficulty_score = rng.uniform(0.66, 0.90)

        questions.append(
            {
                "question_id": question_id,
                "part": topic,
                "tags": topic,
                "difficulty": difficulty,
                "difficulty_score": round(float(difficulty_score), 3),
                "correct_answer": correct_answer,
            }
        )

    return pd.DataFrame(questions)


def create_student_profiles(rng: np.random.Generator) -> dict:
    """Create hidden student ability profiles."""

    student_profiles = {}

    for student_id in range(1, NUM_STUDENTS + 1):
        base_ability = rng.uniform(0.35, 0.85)

        topic_strengths = {
            "algebra": rng.normal(base_ability, 0.12),
            "geometry": rng.normal(base_ability, 0.12),
            "probability": rng.normal(base_ability, 0.12),
            "statistics": rng.normal(base_ability, 0.12),
            "functions": rng.normal(base_ability, 0.12),
            "logic": rng.normal(base_ability, 0.12),
        }

        topic_strengths = {
            topic: float(np.clip(value, 0.05, 0.95))
            for topic, value in topic_strengths.items()
        }

        student_profiles[student_id] = {
            "base_ability": float(base_ability),
            "topic_strengths": topic_strengths,
        }

    return student_profiles


def simulate_answer(
    rng: np.random.Generator,
    topic_strength: float,
    difficulty_score: float,
    correct_answer: int,
) -> int:
    """Simulate the student's submitted answer."""

    probability_correct = topic_strength - difficulty_score + 0.55
    probability_correct = float(np.clip(probability_correct, 0.05, 0.95))

    is_correct = int(rng.random() < probability_correct)

    if is_correct:
        return correct_answer

    wrong_options = [option for option in [1, 2, 3, 4] if option != correct_answer]
    return int(rng.choice(wrong_options))


def create_interactions(
    rng: np.random.Generator,
    questions_df: pd.DataFrame,
    student_profiles: dict,
) -> pd.DataFrame:
    """Create synthetic student-question interactions."""

    interactions = []
    base_time = datetime(2026, 1, 1, 9, 0, 0)

    for student_id, profile in student_profiles.items():
        num_interactions = rng.integers(
            MIN_INTERACTIONS_PER_STUDENT,
            MAX_INTERACTIONS_PER_STUDENT + 1,
        )

        current_time = base_time + timedelta(days=int(student_id))

        for interaction_index in range(num_interactions):
            question = questions_df.sample(
                1,
                random_state=int(rng.integers(0, 1_000_000)),
            ).iloc[0]

            topic = question["tags"]
            topic_strength = profile["topic_strengths"][topic]
            difficulty_score = float(question["difficulty_score"])
            correct_answer = int(question["correct_answer"])

            user_answer = simulate_answer(
                rng=rng,
                topic_strength=topic_strength,
                difficulty_score=difficulty_score,
                correct_answer=correct_answer,
            )

            if question["difficulty"] == "easy":
                elapsed_time = rng.integers(12_000, 45_000)
            elif question["difficulty"] == "medium":
                elapsed_time = rng.integers(30_000, 90_000)
            else:
                elapsed_time = rng.integers(60_000, 150_000)

            current_time += timedelta(minutes=int(rng.integers(2, 20)))

            interactions.append(
                {
                    "student_id": student_id,
                    "timestamp": current_time.isoformat(),
                    "solving_id": f"{student_id}_{interaction_index + 1}",
                    "question_id": int(question["question_id"]),
                    "user_answer": int(user_answer),
                    "correct_answer": correct_answer,
                    "elapsed_time": int(elapsed_time),
                    "part": question["part"],
                    "tags": question["tags"],
                    "difficulty": question["difficulty"],
                    "difficulty_score": round(difficulty_score, 3),
                    "is_correct": int(user_answer == correct_answer),
                }
            )

    return pd.DataFrame(interactions)


def main() -> None:
    """Create and save demo dataset."""

    rng = np.random.default_rng(RANDOM_SEED)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    questions_df = create_question_metadata(rng)
    student_profiles = create_student_profiles(rng)
    interactions_df = create_interactions(rng, questions_df, student_profiles)

    interactions_df = interactions_df.sort_values(
        by=["student_id", "timestamp"]
    ).reset_index(drop=True)

    questions_df.to_csv(QUESTIONS_PATH, index=False)
    interactions_df.to_csv(INTERACTIONS_PATH, index=False)

    print("Demo dataset created successfully.")
    print(f"Questions saved to: {QUESTIONS_PATH}")
    print(f"Interactions saved to: {INTERACTIONS_PATH}")
    print(f"Number of students: {interactions_df['student_id'].nunique()}")
    print(f"Number of questions: {interactions_df['question_id'].nunique()}")
    print(f"Number of interactions: {len(interactions_df)}")
    print(f"Average correctness: {interactions_df['is_correct'].mean():.3f}")


if __name__ == "__main__":
    main()



# ------------------------------------------------------------
# NOTES
# ------------------------------------------------------------

# This file creates a small synthetic demo dataset.
# It does NOT replace the real EdNet dataset.
# Its purpose is to test the project pipeline before using large real data.

# Why do we create demo data first?
# - Real educational datasets can be very large.
# - Before using real data, we need to check whether our code structure works.
# - This demo dataset helps us test preprocessing, feature engineering, modeling, and demo app logic.

# Main output files:
# - 07_demo/demo_data/demo_questions.csv
# - 07_demo/demo_data/demo_interactions.csv

# demo_questions.csv contains question metadata:
# - question_id: unique question number
# - part: broad topic name
# - tags: skill or topic label
# - difficulty: easy, medium, or hard
# - difficulty_score: numeric difficulty value
# - correct_answer: correct answer option

# demo_interactions.csv contains student-question interactions:
# - student_id: unique learner number
# - timestamp: when the student answered the question
# - solving_id: unique interaction/session id
# - question_id: question answered by the student
# - user_answer: student's selected answer
# - correct_answer: correct option
# - elapsed_time: time spent on the question
# - part/tags: topic information
# - difficulty/difficulty_score: question difficulty
# - is_correct: target variable for supervised learning

# Function summary:

# create_question_metadata()
# Creates synthetic questions with topic, difficulty, difficulty score, and correct answer.

# create_student_profiles()
# Creates hidden student ability profiles.
# Each student has a general ability and different strengths for each topic.

# simulate_answer()
# Simulates whether a student answers a question correctly.
# The probability of correctness depends on:
# - student topic strength
# - question difficulty
# - random variation

# create_interactions()
# Creates the full student-question history.
# It simulates multiple question attempts for each student and stores them as rows.

# main()
# Runs the full script:
# 1. Creates question metadata
# 2. Creates student profiles
# 3. Creates interaction data
# 4. Sorts interactions by student and time
# 5. Saves both CSV files

# Important project idea:
# This script is the first safe step before real dataset processing.
# If this demo dataset works, we can later replace it with real EdNet-KT1 data.

# Important ML idea:
# The column "is_correct" will become the first supervised learning target.
# Later, models will try to predict whether a student answers the next question correctly.

# Important research idea:
# This dataset lets us test the adaptive tutor pipeline:
# student history -> knowledge tracing -> recommendation -> RL policy -> evaluation
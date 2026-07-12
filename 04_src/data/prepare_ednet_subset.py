"""
Prepare a controlled EdNet KT1 subset for V2 real-dataset validation.

This script is EdNet-specific.

Input:
- 02_data/external/ednet/KT1/*.csv
- 02_data/external/ednet/contents/questions.csv

Output:
- 02_data/processed/ednet/ednet_interactions_mapped.csv
- 02_data/processed/ednet/ednet_subset_metadata.json
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "05_experiments" / "configs" / "ednet_config.yaml"


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_question_metadata(raw_dir: Path) -> pd.DataFrame:
    questions_path = raw_dir / "contents" / "questions.csv"

    if not questions_path.exists():
        raise FileNotFoundError(f"questions.csv not found: {questions_path}")

    questions = pd.read_csv(questions_path)

    required_columns = ["question_id", "correct_answer", "part", "tags"]
    missing = [column for column in required_columns if column not in questions.columns]

    if missing:
        raise ValueError(f"Missing columns in questions.csv: {missing}")

    questions = questions[required_columns].copy()
    questions["question_id"] = questions["question_id"].astype(str)
    questions["correct_answer"] = questions["correct_answer"].astype(str).str.strip()
    questions["part"] = questions["part"].astype(str)
    questions["tags"] = questions["tags"].astype(str)

    return questions


def student_id_from_file(file_path: Path) -> str:
    return file_path.stem


def map_student_file(file_path: Path, questions: pd.DataFrame) -> pd.DataFrame | None:
    interactions = pd.read_csv(file_path)

    required_columns = [
        "timestamp",
        "solving_id",
        "question_id",
        "user_answer",
        "elapsed_time",
    ]

    missing = [column for column in required_columns if column not in interactions.columns]

    if missing:
        return None

    interactions = interactions[required_columns].copy()

    if len(interactions) == 0:
        return None

    interactions["student_id"] = student_id_from_file(file_path)
    interactions["question_id"] = interactions["question_id"].astype(str)
    interactions["user_answer"] = interactions["user_answer"].astype(str).str.strip()

    mapped = interactions.merge(questions, on="question_id", how="left")
    mapped = mapped.dropna(subset=["correct_answer"]).copy()

    if len(mapped) == 0:
        return None

    mapped["is_correct"] = (
        mapped["user_answer"] == mapped["correct_answer"]
    ).astype(int)

    mapped["difficulty"] = "unknown"
    mapped["difficulty_score"] = 0.5

    output_columns = [
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

    return mapped[output_columns]


def create_ednet_subset(config: dict) -> pd.DataFrame:
    raw_dir = PROJECT_ROOT / config["dataset"]["raw_data_dir"]
    kt1_dir = raw_dir / "KT1"

    if not kt1_dir.exists():
        raise FileNotFoundError(f"KT1 folder not found: {kt1_dir}")

    questions = load_question_metadata(raw_dir)

    target_students = int(config["dataset"]["target_students"])
    target_interactions = int(config["dataset"]["target_interactions"])
    min_interactions = int(config["dataset"]["min_interactions_per_student"])
    max_interactions = int(config["dataset"]["max_interactions_per_student"])

    selected_frames = []
    selected_students = 0
    total_interactions = 0
    scanned_files = 0

    print("Preparing EdNet KT1 subset...")
    print(f"Target students: {target_students}")
    print(f"Target interactions: {target_interactions}")

    for file_path in kt1_dir.glob("*.csv"):
        scanned_files += 1

        mapped = map_student_file(file_path, questions)

        if mapped is None:
            continue

        if len(mapped) < min_interactions:
            continue

        mapped = mapped.sort_values("timestamp").head(max_interactions)

        selected_frames.append(mapped)
        selected_students += 1
        total_interactions += len(mapped)

        if selected_students % 500 == 0:
            print(
                f"Selected students: {selected_students}, "
                f"interactions: {total_interactions}, "
                f"scanned files: {scanned_files}"
            )

        if selected_students >= target_students or total_interactions >= target_interactions:
            break

    if not selected_frames:
        raise ValueError("No eligible EdNet student files were selected.")

    subset = pd.concat(selected_frames, ignore_index=True)

    if len(subset) > target_interactions:
        subset = subset.head(target_interactions)

    subset = subset.sort_values(["student_id", "timestamp"]).reset_index(drop=True)

    return subset


def save_subset(subset: pd.DataFrame, config: dict) -> None:
    output_path = PROJECT_ROOT / config["outputs"]["mapped_interactions"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    subset.to_csv(output_path, index=False)

    student_counts = subset.groupby("student_id").size()

    metadata = {
        "students": int(subset["student_id"].nunique()),
        "questions": int(subset["question_id"].nunique()),
        "interactions": int(len(subset)),
        "average_correctness": round(float(subset["is_correct"].mean()), 4),
        "min_interactions_per_student": int(student_counts.min()),
        "max_interactions_per_student": int(student_counts.max()),
        "output_file": str(output_path.relative_to(PROJECT_ROOT)),
    }

    metadata_path = output_path.parent / "ednet_subset_metadata.json"

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    print("\nEdNet subset created successfully.")
    print(json.dumps(metadata, indent=2))


def main() -> None:
    config = load_config()
    subset = create_ednet_subset(config)
    save_subset(subset, config)


if __name__ == "__main__":
    main()

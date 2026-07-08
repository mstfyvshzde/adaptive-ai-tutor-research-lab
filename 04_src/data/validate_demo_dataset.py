"""
Validate the synthetic demo dataset.

Goal:
Check that demo_questions.csv and demo_interactions.csv are usable
before feature engineering and modeling.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QUESTIONS_PATH = PROJECT_ROOT / "07_demo" / "demo_data" / "demo_questions.csv"
INTERACTIONS_PATH = PROJECT_ROOT / "07_demo" / "demo_data" / "demo_interactions.csv"


REQUIRED_QUESTION_COLUMNS = [
    "question_id",
    "part",
    "tags",
    "difficulty",
    "difficulty_score",
    "correct_answer",
]

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


# 1. check_file_exists
# Ne Yapar? Belirtilen dosya yolunda dosyanın gerçekten var olup olmadığını kontrol eder; dosya bulunamazsa hata (FileNotFoundError) fırlatır.
def check_file_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")



# 2. check_required_columns
# Ne Yapar? Tabloda olması zorunlu olan sütunların (kolonların) eksiksiz yer alıp almadığına bakar; eksik sütun varsa hata verir.
def check_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
    dataset_name: str,
) -> None:
    missing_columns = [
        column for column in required_columns if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: {missing_columns}"
        )



# 3. check_missing_values
# Ne Yapar? Veri setinde boş bırakılmış (NaN/None) hücreler olup olmadığını denetler; eksik veri bulursa hangi sütunda kaç tane olduğunu rapor ederek hata fırlatır.
def check_missing_values(dataframe: pd.DataFrame, dataset_name: str) -> None:
    missing_counts = dataframe.isna().sum()
    missing_counts = missing_counts[missing_counts > 0]

    if not missing_counts.empty:
        raise ValueError(
            f"{dataset_name} has missing values:\n{missing_counts}"
        )


# 4. check_correctness_column
# Ne Yapar? is_correct (doğru mu) sütununun mantığını denetler; öğrencinin cevabı ile doğru cevap uyuştuğunda bu değerin 1, uyuşmadığında 0 olduğunu teyit eder.
def check_correctness_column(interactions_df: pd.DataFrame) -> None:
    expected_is_correct = (
        interactions_df["user_answer"] == interactions_df["correct_answer"]
    ).astype(int)

    if not (interactions_df["is_correct"] == expected_is_correct).all():
        raise ValueError("is_correct column does not match answers.")



# 5. check_question_references
# Ne Yapar? Etkileşimler tablosundaki tüm soru ID'lerinin, ana soru havuzunda (questions_df) mevcut olup olmadığını kontrol eder (yabancı anahtar/foreign key kontrolü).
def check_question_references(
    questions_df: pd.DataFrame,
    interactions_df: pd.DataFrame,
) -> None:
    question_ids = set(questions_df["question_id"])
    interaction_question_ids = set(interactions_df["question_id"])

    missing_question_ids = interaction_question_ids - question_ids

    if missing_question_ids:
        raise ValueError(
            f"Interactions contain unknown question_ids: {missing_question_ids}"
        )



# 6. check_timestamp_order
# Ne Yapar? Her öğrencinin çözdüğü soruların zaman damgalarını (timestamp) kronolojik olarak inceler; zaman sırasının geçmişten geleceğe doğru düzenli akıp akmadığına bakar.
def check_timestamp_order(interactions_df: pd.DataFrame) -> None:
    interactions_df = interactions_df.copy()
    interactions_df["timestamp"] = pd.to_datetime(interactions_df["timestamp"])

    for student_id, student_df in interactions_df.groupby("student_id"):
        if not student_df["timestamp"].is_monotonic_increasing:
            raise ValueError(
                f"Timestamps are not sorted for student: {student_id}"
            )



# 7. main
# Ne Yapar? Tüm bu kontrol fonksiyonlarını sırasıyla çalıştıran ana motor görevi görür. Veriler tüm testlerden başarıyla geçerse ekrana onay mesajı ve temel istatistikleri yazdırır.
def main() -> None:
    check_file_exists(QUESTIONS_PATH)
    check_file_exists(INTERACTIONS_PATH)

    questions_df = pd.read_csv(QUESTIONS_PATH)
    interactions_df = pd.read_csv(INTERACTIONS_PATH)

    check_required_columns(
        questions_df,
        REQUIRED_QUESTION_COLUMNS,
        "questions_df",
    )

    check_required_columns(
        interactions_df,
        REQUIRED_INTERACTION_COLUMNS,
        "interactions_df",
    )

    check_missing_values(questions_df, "questions_df")
    check_missing_values(interactions_df, "interactions_df")

    check_correctness_column(interactions_df)
    check_question_references(questions_df, interactions_df)
    check_timestamp_order(interactions_df)

    print("Demo dataset validation passed.")
    print(f"Questions: {len(questions_df)}")
    print(f"Interactions: {len(interactions_df)}")
    print(f"Students: {interactions_df['student_id'].nunique()}")
    print(f"Average correctness: {interactions_df['is_correct'].mean():.3f}")
    print(f"Average elapsed time: {interactions_df['elapsed_time'].mean():.1f} ms")


if __name__ == "__main__":
    main()
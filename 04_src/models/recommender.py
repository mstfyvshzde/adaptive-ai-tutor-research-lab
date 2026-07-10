"""
Simple recommendation baselines for the Adaptive AI Tutor Research Lab.

Goal:
Recommend the next question for each student using simple baseline methods.

Input:
02_data/processed/demo_features.csv

Output:
06_results/tables/recommendation_examples.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "02_data" / "processed" / "demo_features.csv"
OUTPUT_DIR = PROJECT_ROOT / "06_results" / "tables"
OUTPUT_PATH = OUTPUT_DIR / "recommendation_examples.csv"

RANDOM_SEED = 17


def load_features(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"missing file: {path}. run build_features.py first."
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    return dataframe



def build_question_bank(dataframe: pd.DataFrame) -> pd.DataFrame:
    question_bank = (
        dataframe.groupby('question_id')
        .agg(
            tags=('tags', 'first'),
            difficulty=('difficulty', 'first'),
            difficulty_score=('difficulty_score', 'mean')
        )
        # tags=('tags', 'first'): Her sorunun birden fazla satırı varsa, o soruya ait ilk satırdaki etiketleri (tags) alır. Genelde etiketler aynı sorunun altında değişmediği için "ilkini al geç" mantığıyla çalışır.
        # difficulty=('difficulty', 'first'): Benzer şekilde, o sorunun ilk satırdaki zorluk derecesini (difficulty) (örneğin: "Kolay", "Zor" gibi metinleri) alır.
        # difficulty_score=('difficulty_score', 'mean'): Eğer bir soruya farklı öğrencilerden veya değerlendirmelerden birden fazla zorluk puanı geldiyse, o soruya ait tüm zorluk puanlarının ortalamasını (mean) hesaplar.
        .reset_index()
    )

    return question_bank



# build_student_profiles: Her öğrencinin çözdüğü son 5 sorudaki başarı oranını (doğruluk yüzdesini) hesaplar ve en çok yanlış yapıp başarısız olduğu zayıf konuyu (weak_topic) tespit ederek öğrenci profillerini çıkarır.
def build_student_profiles(dataframe: pd.DataFrame) -> pd.DataFrame:
    student_rows = []

    for student_id, student_df in dataframe.groupby("student_id"):
        student_df = student_df.sort_values("timestamp")

        recent_accuracy = student_df.tail(5)["is_correct"].mean()
        weak_topic = student_df.groupby("tags")["is_correct"].mean().idxmin()

        student_rows.append(
            {
                "student_id": student_id,
                "recent_accuracy": float(recent_accuracy),
                "weak_topic": weak_topic,
            }
        )

    return pd.DataFrame(student_rows)


# choose_difficulty: Öğrencinin son başarı oranına bakar; %55'in altındaysa "kolay", %75'in altındaysa "orta", daha yüksekse "zor" bir soru seviyesi seçilmesi gerektiğine karar verir.
def choose_difficulty(recent_accuracy: float) -> str:
    if recent_accuracy < 0.55:
        return "easy"

    if recent_accuracy < 0.75:
        return "medium"

    return "hard"




def sample_question(
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.Series:
    return question_bank.sample(
        1,
        random_state=int(rng.integers(0, 1_000_000)),
    ).iloc[0]



# recommend_random: Öğrencinin durumuna hiç bakmaksızın, soru bankasından tamamen rastgele bir soru seçer ve önerir.
def recommend_random(
    student: pd.Series,
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    question = sample_question(question_bank, rng)

    return {
        "student_id": student["student_id"],
        "method": "random",
        "recommended_question_id": question["question_id"],
        "recommended_topic": question["tags"],
        "recommended_difficulty": question["difficulty"],
        "reason": "Random question selected.",
    }



# recommend_difficulty_based: choose_difficulty fonksiyonunun belirlediği zorluk seviyesine uygun havuzdan rastgele bir soru seçerek öğrenciye seviyesine uygun öneri yapar.
def recommend_difficulty_based(
    student: pd.Series,
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    target_difficulty = choose_difficulty(student["recent_accuracy"])

    candidates = question_bank[
        question_bank["difficulty"] == target_difficulty
    ]

    if candidates.empty:
        candidates = question_bank

    question = sample_question(candidates, rng)

    return {
        "student_id": student["student_id"],
        "method": "difficulty_based",
        "recommended_question_id": question["question_id"],
        "recommended_topic": question["tags"],
        "recommended_difficulty": question["difficulty"],
        "reason": f"Recent accuracy suggests a {target_difficulty} question.",
    }



# recommend_weak_topic: Öğrencinin en çok zorlandığı zayıf konuyu (weak_topic) hedef alır ve sadece o konuya ait sorulardan rastgele birini seçerek eksik kapatmasını amaçlar.
def recommend_weak_topic(
    student: pd.Series,
    question_bank: pd.DataFrame,
    rng: np.random.Generator,
) -> dict:
    candidates = question_bank[
        question_bank["tags"] == student["weak_topic"]
    ]

    if candidates.empty:
        candidates = question_bank

    question = sample_question(candidates, rng)

    return {
        "student_id": student["student_id"],
        "method": "weak_topic",
        "recommended_question_id": question["question_id"],
        "recommended_topic": question["tags"],
        "recommended_difficulty": question["difficulty"],
        "reason": f"Student's weakest topic is {student['weak_topic']}.",
    }


# create_recommendations: Tüm öğrencileri tek tek dönerek yukarıdaki 3 farklı öneri yöntemini de her bir öğrenci için çalıştırır ve sonuçları bir araya getirip toplu bir tablo oluşturur.
def create_recommendations(
    student_profiles: pd.DataFrame,
    question_bank: pd.DataFrame,
) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)

    recommendation_rows = []

    for _, student in student_profiles.iterrows():
        recommendation_rows.append(
            recommend_random(student, question_bank, rng)
        )
        recommendation_rows.append(
            recommend_difficulty_based(student, question_bank, rng)
        )
        recommendation_rows.append(
            recommend_weak_topic(student, question_bank, rng)
        )

    return pd.DataFrame(recommendation_rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = load_features(INPUT_PATH)

    question_bank = build_question_bank(dataframe)
    student_profiles = build_student_profiles(dataframe)

    recommendations_df = create_recommendations(
        student_profiles=student_profiles,
        question_bank=question_bank,
    )

    recommendations_df.to_csv(OUTPUT_PATH, index=False)

    print("Recommendation examples created successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nPreview:")
    print(recommendations_df.head())


if __name__ == "__main__":
    main()
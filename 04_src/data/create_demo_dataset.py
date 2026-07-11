"""
Create a synthetic demo dataset for the Adaptive AI Tutor Research Lab.

This script creates a small student-question interaction dataset.

Goal:
Build a controllable demo dataset before using a real dataset.

Outputs:
07_demo/demo_data/demo_questions.csv
07_demo/demo_data/demo_interactions.csv
"""

from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# PROJECT_ROOT: Projenin ana dizininin (kök klasörünün) bilgisayardaki konumunu otomatik olarak bulur ve saklar.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# OUTPUT_DIR: Üretilecek sahte verilerin kaydedileceği hedef klasörün (07_demo/demo_data) yolunu belirler.
OUTPUT_DIR = PROJECT_ROOT / "07_demo" / "demo_data"

# QUESTIONS_PATH: Oluşturulacak soru verilerinin kaydedileceği CSV dosyasının tam yolunu tutar.
QUESTIONS_PATH = OUTPUT_DIR / "demo_questions.csv"

# INTERACTIONS_PATH: Öğrenci-soru etkileşimlerinin (cevapların) kaydedileceği CSV dosyasının tam yolunu tutar.
INTERACTIONS_PATH = OUTPUT_DIR / "demo_interactions.csv"

# RANDOM_SEED: Rastgele veri üretilirken her çalıştırmada aynı sonuçların (aynı sayıların ve seçimlerin) birebir tekrar elde edilmesini sağlayan kilittir.
RANDOM_SEED = 17

# NUM_STUDENTS: Veri setinde toplam kaç adet sahte öğrenci tanımlanacağını (40) belirler.
NUM_STUDENTS = 40

# NUM_QUESTIONS: Havuzda toplam kaç adet benzersiz soru oluşturulacağını (80) belirler.
NUM_QUESTIONS = 80

# MIN_INTERACTIONS_PER_STUDENT: Bir öğrencinin veri setinde minimum kaç soruya cevap vermiş olacağını (25) sınırlar.
MIN_INTERACTIONS_PER_STUDENT = 25

# MAX_INTERACTIONS_PER_STUDENT: Bir öğrencinin veri setinde maksimum kaç soruya cevap vermiş olacağını (45) sınırlar.
MAX_INTERACTIONS_PER_STUDENT = 45

# TOPICS: Soruların rastgele dağıtılacağı matematik konularının listesini içerir.
TOPICS = [
    "algebra",
    "geometry",
    "probability",
    "statistics",
    "functions",
]

# DIFFICULTIES: Soruların zorluk derecelerini ("easy", "medium", "hard") ve bunlara karşılık gelen zorluk katsayılarını/oranlarını eşleştirir.
DIFFICULTIES = [
    ("easy", 0.25),
    ("medium", 0.50),
    ("hard", 0.75),
]

# ANSWER_CHOICES: Soruların sahip olacağı çoktan seçmeli şık seçeneklerini (A, B, C, D) tanımlar.
ANSWER_CHOICES = ["A", "B", "C", "D"]





# 1. create_question_bank
# Ne Yapar? Belirlediğin parametrelere göre (80 adet) sahte soru üretir.
# Detay: Her soruya rastgele bir konu (topic), zorluk seviyesi (difficulty), bölüm (part) ve doğru cevap şıkkı (A, B, C, D) atayarak bunları bir tablo (DataFrame) haline getirir.
def create_question_bank(rng: np.random.Generator) -> pd.DataFrame:
    question_rows = []

    for question_id in range(1, NUM_QUESTIONS + 1):
        topic = str(rng.choice(TOPICS))
        difficulty, difficulty_score = DIFFICULTIES[
            int(rng.integers(0, len(DIFFICULTIES)))
        ]

        question_rows.append(
            {
                "question_id": question_id,
                "part": int(rng.integers(1, 4)),
                "tags": topic,
                "difficulty": difficulty,
                "difficulty_score": difficulty_score,
                "correct_answer": str(rng.choice(ANSWER_CHOICES)),
            }
        )

    return pd.DataFrame(question_rows)



# 2. choose_wrong_answer
# Ne Yapar? Öğrenci soruyu yanlış çözdüğünde, ona yanlış bir şık seçer.
# Detay: Sorunun doğru cevabını listeden eler ve geriye kalan 3 yanlış şık arasından rastgele birini seçerek geri döndürür.
def choose_wrong_answer(
    correct_answer: str,
    rng: np.random.Generator,
) -> str:
    wrong_choices = [
        answer for answer in ANSWER_CHOICES if answer != correct_answer
    ]

    return str(rng.choice(wrong_choices))




# 3. create_student_interactions
# Ne Yapar? Öğrencilerin sorularla olan etkileşimlerini (test çözme simülasyonunu) yaratır.
# Detay: Her öğrenciye rastgele bir yetenek skoru ve konu yatkınlığı verir. Öğrencinin soruyu doğru bilme ihtimalini Yetenek + Konu Yatkınlığı - Soru Zorluğu formülüyle hesaplar. Doğru veya yanlış bilmesine göre harcadığı süreyi (elapsed_time) ve verdiği cevabı belirleyip büyük bir etkileşim tablosu oluşturur.
def create_student_interactions(
    questions_df: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    interaction_rows = []
    solving_id = 1

    start_time = datetime(2026, 1, 1, 9, 0, 0)

    for student_number in range(1, NUM_STUDENTS + 1):
        student_id = f"student_{student_number:03d}"

        student_ability = float(rng.normal(0.65, 0.12))
        student_ability = float(np.clip(student_ability, 0.25, 0.95))

        topic_adjustments = {
            topic: float(rng.normal(0.0, 0.12)) for topic in TOPICS
        }

        number_of_interactions = int(
            rng.integers(
                MIN_INTERACTIONS_PER_STUDENT,
                MAX_INTERACTIONS_PER_STUDENT + 1,
            )
        )

        current_time = start_time + timedelta(days=student_number)

        for _ in range(number_of_interactions):
            question = questions_df.sample(
                1,
                random_state=int(rng.integers(0, 1_000_000)),
            ).iloc[0]

            topic = question["tags"]
            difficulty_score = float(question["difficulty_score"])

            probability_correct = (
                student_ability
                + topic_adjustments[topic]
                - difficulty_score
                + 0.45
            )

            probability_correct = float(
                np.clip(probability_correct, 0.05, 0.95)
            )

            is_correct = int(rng.random() < probability_correct)

            correct_answer = question["correct_answer"]

            if is_correct:
                user_answer = correct_answer
            else:
                user_answer = choose_wrong_answer(correct_answer, rng)

            elapsed_time = (
                30_000
                + difficulty_score * 60_000
                + rng.normal(0, 8_000)
            )

            if not is_correct:
                elapsed_time += 15_000

            elapsed_time = int(max(elapsed_time, 5_000))

            current_time += timedelta(
                minutes=int(rng.integers(5, 180))
            )

            interaction_rows.append(
                {
                    "student_id": student_id,
                    "timestamp": current_time.isoformat(),
                    "solving_id": solving_id,
                    "question_id": int(question["question_id"]),
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "elapsed_time": elapsed_time,
                    "part": int(question["part"]),
                    "tags": topic,
                    "difficulty": question["difficulty"],
                    "difficulty_score": difficulty_score,
                    "is_correct": is_correct,
                }
            )

            solving_id += 1

    return pd.DataFrame(interaction_rows)



# 4. main
# Ne Yapar? Tüm sistemi başlatan ve yöneten orkestra şefidir.
# Detay: Verilerin kaydedileceği klasörü oluşturur, rastgele sayı üreticiyi (rng) başlatır, yukarıdaki fonksiyonları sırayla çağırarak soruları ve etkileşimleri üretir, bunları CSV dosyası olarak bilgisayara kaydeder ve ekrana özet istatistikleri yazdırır
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(RANDOM_SEED)

    questions_df = create_question_bank(rng)
    interactions_df = create_student_interactions(questions_df, rng)

    questions_df.to_csv(QUESTIONS_PATH, index=False)
    interactions_df.to_csv(INTERACTIONS_PATH, index=False)

    print("Demo dataset created successfully.")
    print(f"Questions saved to: {QUESTIONS_PATH}")
    print(f"Interactions saved to: {INTERACTIONS_PATH}")
    print(f"Number of students: {interactions_df['student_id'].nunique()}")
    print(f"Number of questions: {questions_df['question_id'].nunique()}")
    print(f"Number of interactions: {len(interactions_df)}")
    print(f"Average correctness: {interactions_df['is_correct'].mean():.3f}")


if __name__ == "__main__":
    main()

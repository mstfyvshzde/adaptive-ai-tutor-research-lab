"""
Build feature dataset for the Adaptive AI Tutor Research Lab.

Goal:
Convert raw student-question interactions into modeling features.

Input:
07_demo/demo_data/demo_interactions.csv

Output:
02_data/processed/demo_features.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "07_demo" / "demo_data" / "demo_interactions.csv"
OUTPUT_DIR = PROJECT_ROOT / "02_data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "demo_features.csv"



# 1. load_interactions
# Ne Yapar? Ham öğrenci etkileşim verisini bilgisayardan okur.
# Detay: Zaman damgalarını tarih formatına çevirir ve tüm tabloyu önce öğrenciye, sonra kronolojik zamana göre (student_id, timestamp) sıraya dizer.
def load_interactions(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"missing file: {path}. run create_demo_dataset.py first."
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    dataframe = dataframe.sort_values(
        ['student_id', 'timestamp']
    ).reset_index(drop=True)

    return dataframe



# 2. add_student_history_features
# Ne Yapar? Öğrencinin genel test çözme geçmişine dair performans özelliklerini üretir.
# Detay: Öğrencinin o ana kadar kaç soru çözdüğünü, genel başarı ortalamasını, bir önceki soruyu doğru bilip bilmediğini, son 5 ve son 10 sorudaki hareketli başarı yüzdesini ve iki soru arasında geçen süreyi hesaplar.
def add_student_history_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe['student_attempt_count'] = dataframe.groupby(
        'student_id'
    ).cumcount()

    student_correct_so_far = (
        dataframe.groupby("student_id")["is_correct"].cumsum()
        - dataframe["is_correct"]
    )

    dataframe['student_accuracy_so_far'] = np.where(
        dataframe['student_attempt_count'] > 0,
        student_correct_so_far / dataframe['student_attempt_count'],
        0.5
    )

    dataframe['previous_correct'] = (
        dataframe.groupby('student_id')['is_correct']
        .shift(1)
        .fillna(0.5)
    )

    dataframe["previous_elapsed_time"] = (
        dataframe.groupby("student_id")["elapsed_time"]
        .shift(1)
        .fillna(dataframe["elapsed_time"].median())
    )

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

    dataframe["time_since_previous_seconds"] = (
        dataframe.groupby("student_id")["timestamp"]
        .diff()
        .dt.total_seconds()
        .fillna(0)
    )

    return dataframe



# 3. add_topic_features
# Ne Yapar? Öğrencinin konu bazlı (örneğin sadece Cebir veya Geometri) geçmiş performansını hesaplar.
# Detay: Öğrencinin o spesifik konudan daha önce kaç soru çözdüğünü ve o konudaki başarı oranını (topic_accuracy_so_far) çıkarır.
def add_topic_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    group_columns = ["student_id", "tags"]

    dataframe["topic_attempt_count_so_far"] = dataframe.groupby(
        group_columns
    ).cumcount()

    topic_correct_so_far = (
        dataframe.groupby(group_columns)["is_correct"].cumsum()
        - dataframe["is_correct"]
    )

    dataframe["topic_accuracy_so_far"] = np.where(
        dataframe["topic_attempt_count_so_far"] > 0,
        topic_correct_so_far / dataframe["topic_attempt_count_so_far"],
        0.5,
    )

    return dataframe



# 4. add_question_features
# Ne Yapar? Soruların havuzdaki genel zorluk ve popülerlik durumunu analiz eder.
# Detay: İlgili sorunun o ana kadar tüm öğrenciler tarafından toplam kaç kez çözüldüğünü bulur ve sorunun gerçekte ne kadar zor olduğunu veri odaklı bir şekilde (1.0 - başarı oranı) tahmin eder.
def add_question_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe["question_attempt_count_so_far"] = dataframe.groupby(
        "question_id"
    ).cumcount()

    question_correct_so_far = (
        dataframe.groupby("question_id")["is_correct"].cumsum()
        - dataframe["is_correct"]
    )

    dataframe["question_accuracy_so_far"] = np.where(
        dataframe["question_attempt_count_so_far"] > 0,
        question_correct_so_far / dataframe["question_attempt_count_so_far"],
        0.5,
    )

    dataframe["question_difficulty_estimate"] = (
        1.0 - dataframe["question_accuracy_so_far"]
    )

    return dataframe



# 5. build_features
# Ne Yapar? Yukarıdaki 3 özellik ekleme fonksiyonunu sırayla çalıştırır.
# Detay: Model için gerekli olan ve yeni üretilen tüm anlamlı sütunları seçerek nihai bir veri tablosu (DataFrame) hazırlar.
def build_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Build final feature dataset."""

    dataframe = add_student_history_features(dataframe)
    dataframe = add_topic_features(dataframe)
    dataframe = add_question_features(dataframe)

    feature_columns = [
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

    return dataframe[feature_columns]


# 6. main
# Ne Yapar? Tüm süreci yöneten ana merkezdir.
# Detay: Çıktı klasörünü hazırlar, ham veriyi yükleyip özellik mühendisliği sürecinden geçirir, sonucu yeni bir CSV dosyası (demo_features.csv) olarak kaydeder ve ekrana özet bilgileri bastırır.
def main() -> None:
    """Run feature engineering pipeline."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    interactions_df = load_interactions(INPUT_PATH)
    features_df = build_features(interactions_df)

    features_df.to_csv(OUTPUT_PATH, index=False)

    print("Feature dataset created successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Rows: {len(features_df)}")
    print(f"Columns: {len(features_df.columns)}")
    print(f"Average target correctness: {features_df['is_correct'].mean():.3f}")
    print("\nFeature preview:")
    print(features_df.head())


if __name__ == "__main__":
    main()
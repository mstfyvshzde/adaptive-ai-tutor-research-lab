
from pathlib import Path
import re

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "02_data/processed/ednet/ednet_interactions_mapped.csv"
OUTPUT_PATH = ROOT / "02_data/processed/ednet/ednet_features_v2.csv"
SUMMARY_PATH = ROOT / "06_results/tables/ednet/ednet_feature_v2_summary.csv"


# parse_tags(value): Sorulara ait etiketleri (tag) temizler. Metin içindeki gereksiz köşeli parantez, tırnak gibi karakterleri atarak etiketleri tek tek listeye böler.
def parse_tags(value): 
    if pd.isna(value):
        return []
    
    text = str(value).strip()

    text = text.replace("[", " ").replace("]", " ").replace("'", "").replace('"', "")
    tokens = re.split(r"[;,\s]+", text)

    return [token for token in tokens if token]


# safe_ratio(numerator, denominator): Bölme işlemlerinde sıfıra bölünme (ZeroDivisionError) veya sonsuzluk (inf) hatası alınmasını engeller. Eğer payda 0 ise varsayılan olarak 1.0 değerini döner ve sonucu 0 ile 20 arasında sınırlar.
# Numerator (Pay): Kesir çizgisinin üstündeki sayıdır. Bölünen miktarı gösterir.
# Denominator (Payda): Kesir çizgisinin altındaki sayıdır. Bütünün kaç eşit parçaya bölündüğünü gösterir.
def safe_ratio(numerator, denominator, default=1.0):
    result = numerator / denominator.replace(0, np.nan)
    result = result.replace([np.inf, -np.inf], np.nan).fillna(default)
    return result.clip(lower=0, upper=20)



# rolling_accuracy_before(df, student_col, window): Öğrencinin çözdüğü son N sorudaki (örneğin son 3 veya son 20) hareketli başarı ortalamasını hesaplar. Önemli nokta: Hesaplamaya öğrencinin şu an çözmekte olduğu soru dahil edilmez, sadece geçmişi baz alınır.
def rolling_accuracy_before(df, student_col, window):
    previous_correct = df.groupby(student_col)["is_correct"].shift(1)
    # Ne yapar: Her öğrencinin soru geçmişini kendi içinde 1 adım aşağı kaydırır.
    # Amacı: Modelin hedef değişkeni (is_correct) tahmin etmeye çalışırken, o an çözülen sorunun cevabını kopya çekmesini engellemektir. Böylece her satırın karşısına, o sorunun cevabı değil, bir önceki sorunun cevabı gelir. İlk sorunun öncesi olmadığı için değeri NaN (boş) olur.

    result = (
        previous_correct
        .groupby(df[student_col])
        .rolling(window=window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )
    # Ne yapar: Kaydırılmış veriyi tekrar öğrenci bazında gruplar ve geriye doğru belirtilen pencere boyutu (window) kadar satırı alarak ortalamasını (mean) hesaplar. min_periods=1 sayesinde, elinde pencere boyutu kadar (örn: 3 tane) soru olmasa bile, mevcut olan tek bir soruyla bile ortalama hesaplamaya başlar.
    # reset_index(...): Pandas'ın rolling fonksiyonu çıktı üretirken öğrenci ID'sini indeks olarak başa ekler (multi-index yapar). Bu kısım o eklenen indeksi silerek veriyi ana tablonun hizasına geri getirir.

    return result.fillna(0.5)



# compute_streaks(df, student_col): Öğrencinin o anki arka arkaya doğru bilme (galibiyet) veya arka arkaya yanlış yapma (mağlubiyet) serilerini (streak) hesaplar. Öğrenci doğru bildikçe doğru serisi artar, yanlış yaptığında sıfırlanır.
def compute_streaks(df, student_col):
    correct_streak = np.zeros(len(df), dtype=np.int32)
    incorrect_streak = np.zeros(len(df), dtype=np.int32)

    for _, indexes in df.groupby(student_col, sort=False).indices.items():
        current_correct = 0
        current_incorrect = 0

        for idx in indexes:
            correct_streak[idx] = current_correct
            incorrect_streak[idx] = current_incorrect

            if df.at[idx, "is_correct"] == 1:
                current_correct += 1
                current_incorrect = 0
            else:
                current_incorrect += 1
                current_correct = 0

    return correct_streak, incorrect_streak



# compute_question_seen_features(...): Öğrencinin soru çözme alışkanlıklarını inceler. İki veri üretir:
# student_unique_questions_so_far: Öğrencinin o ana kadar çözdüğü toplam benzersiz soru sayısı.
# same_question_seen_before: Öğrencinin önünde duran soruyu daha önce çözüp çözmediği bilgisi (0 veya 1).
def compute_question_seen_features(df, student_col, question_col):
    unique_questions_so_far = np.zeros(len(df), dtype=np.int32)
    same_question_seen_before = np.zeros(len(df), dtype=np.int8)

    for _, indexes in df.groupby(student_col, sort=False).indices.items():
        seen_questions = set()

        for idx in indexes:
            question_id = df.at[idx, question_col]

            unique_questions_so_far[idx] = len(seen_questions)
            same_question_seen_before[idx] = int(question_id in seen_questions)

            seen_questions.add(question_id)

    return unique_questions_so_far, same_question_seen_before


# ompute_activity_gap_hours(df, student_col): Öğrencinin iki soru çözümü arasında ne kadar süre ara verdiğini saat cinsinden hesaplar. EdNet zaman damgalarını (milisaniye veya saniye) otomatik tespit ederek saate çevirir.
def compute_activity_gap_hours(df, student_col):
    timestamp_num = pd.to_numeric(df["timestamp"], errors="coerce")

    if timestamp_num.notna().mean() > 0.9:
        diff = timestamp_num.groupby(df[student_col]).diff()

        scale = 3_600_000.0 if timestamp_num.abs().median() > 10_000_000_000 else 3_600.0

        return (diff / scale).fillna(0).clip(lower=0)

    timestamp_dt = pd.to_datetime(df["timestamp"], errors="coerce")
    diff = timestamp_dt.groupby(df[student_col]).diff()

    return (diff.dt.total_seconds() / 3600).fillna(0).clip(lower=0)



# main() Fonksiyonu (İş Akışı ve Kombinasyon Özellikleri)
# Veriyi yükler, sıralar ve yukarıdaki fonksiyonları birleştirerek veri setine nihai şeklini verir. Burada doğrudan döngüler yerine Pandas fonksiyonlarıyla hesaplanan çok kritik hibrit (birleşik) özellikler var:
# Öğrenci Bazlı İstatistikler:
# student_accuracy_so_far: Öğrencinin o ana kadarki genel başarı oranı.
# student_avg_elapsed_time_so_far ve std_so_far: Öğrencinin geçmişte sorulara harcadığı ortalama süre ve bu sürenin standart sapması (istikrarı).

# Soru Bazlı İstatistikler:
# question_accuracy_so_far: Sorunun o ana kadar tüm öğrenciler tarafından doğru cevaplanma oranı.
# question_difficulty_estimate: Sorunun zorluk derecesi (1−soru basarısı).

# Kombinasyon (Kıyaslama) Özellikleri:
# ability_minus_difficulty: Öğrencinin genel başarısı ile sorunun zorluğu arasındaki fark. Pozitifse öğrencinin doğru bilme ihtimali yüksektir.
# recent_accuracy_minus_difficulty: Öğrencinin son 20 sorudaki formu ile sorunun zorluğu arasındaki fark.
# elapsed_time_ratio_vs_student_avg: Öğrencinin bu soruda harcadığı sürenin, kendi geçmiş ortalamasına oranı (Çok mu yavaş kaldı?).
# elapsed_time_ratio_vs_question_avg: Öğrencinin bu soruda harcadığı sürenin, o sorunun genel harcanma süresi ortalamasına oranı.
def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading: {INPUT_PATH}")
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    student_col = "student_id" if "student_id" in df.columns else "user_id"
    question_col = "question_id"

    if student_col not in df.columns:
        raise ValueError("Expected student_id or user_id column.")

    if question_col not in df.columns:
        raise ValueError("Expected question_id column.")

    if student_col != "student_id":
        df = df.rename(columns={student_col: "student_id"})

    student_col = "student_id"

    if "timestamp" not in df.columns:
        df["timestamp"] = np.arange(len(df))

    if "solving_id" not in df.columns:
        df["solving_id"] = np.arange(len(df))

    if "is_correct" not in df.columns:
        if "user_answer" not in df.columns or "correct_answer" not in df.columns:
            raise ValueError("Need either is_correct or user_answer + correct_answer columns.")

        df["is_correct"] = (
            df["user_answer"].astype(str).str.strip()
            == df["correct_answer"].astype(str).str.strip()
        ).astype(int)
    else:
        df["is_correct"] = pd.to_numeric(df["is_correct"], errors="coerce").fillna(0).astype(int)

    if "elapsed_time" not in df.columns:
        df["elapsed_time"] = 0

    df["elapsed_time"] = (
        pd.to_numeric(df["elapsed_time"], errors="coerce")
        .fillna(0)
        .clip(lower=0)
    )

    if "part" not in df.columns:
        df["part"] = "unknown"
    else:
        df["part"] = df["part"].fillna("unknown").astype(str)

    if "tags" in df.columns:
        parsed_tags = df["tags"].apply(parse_tags)
        df["tag_count"] = parsed_tags.apply(len)
        df["primary_tag"] = parsed_tags.apply(lambda tags: tags[0] if tags else "unknown")
    else:
        df["tag_count"] = 0
        df["primary_tag"] = "unknown"

    df = df.sort_values([student_col, "timestamp", "solving_id"]).reset_index(drop=True)

    # Student history features - before current row
    df["student_attempt_count_so_far"] = df.groupby(student_col).cumcount()
    df["student_correct_count_so_far"] = (
        df.groupby(student_col)["is_correct"].cumsum() - df["is_correct"]
    )

    df["student_accuracy_so_far"] = (
        df["student_correct_count_so_far"]
        / df["student_attempt_count_so_far"].replace(0, np.nan)
    ).fillna(0.5)

    df["rolling_accuracy_3"] = rolling_accuracy_before(df, student_col, window=3)
    df["rolling_accuracy_20"] = rolling_accuracy_before(df, student_col, window=20)

    (
        df["student_correct_streak"],
        df["student_incorrect_streak"],
    ) = compute_streaks(df, student_col)

    elapsed_sum_before = (
        df.groupby(student_col)["elapsed_time"].cumsum() - df["elapsed_time"]
    )

    elapsed_sq_sum_before = (
        df.groupby(student_col)["elapsed_time"]
        .transform(lambda x: (x ** 2).cumsum())
        - (df["elapsed_time"] ** 2)
    )

    df["student_avg_elapsed_time_so_far"] = (
        elapsed_sum_before / df["student_attempt_count_so_far"].replace(0, np.nan)
    ).fillna(0)

    elapsed_mean_sq_before = (
        elapsed_sq_sum_before / df["student_attempt_count_so_far"].replace(0, np.nan)
    )

    elapsed_variance_before = (
        elapsed_mean_sq_before - (df["student_avg_elapsed_time_so_far"] ** 2)
    ).clip(lower=0)

    df["student_elapsed_time_std_so_far"] = np.sqrt(elapsed_variance_before).fillna(0)

    # Question history features - before current row
    df["question_attempt_count_so_far"] = df.groupby(question_col).cumcount()

    question_correct_before = (
        df.groupby(question_col)["is_correct"].cumsum() - df["is_correct"]
    )

    df["question_accuracy_so_far"] = (
        question_correct_before
        / df["question_attempt_count_so_far"].replace(0, np.nan)
    ).fillna(0.5)

    df["question_difficulty_estimate"] = 1 - df["question_accuracy_so_far"]

    question_elapsed_sum_before = (
        df.groupby(question_col)["elapsed_time"].cumsum() - df["elapsed_time"]
    )

    df["question_avg_elapsed_time_so_far"] = (
        question_elapsed_sum_before
        / df["question_attempt_count_so_far"].replace(0, np.nan)
    ).fillna(0)

    (
        df["student_unique_questions_so_far"],
        df["same_question_seen_before"],
    ) = compute_question_seen_features(df, student_col, question_col)

    df["activity_gap_hours"] = compute_activity_gap_hours(df, student_col)

    # Combined features
    df["ability_minus_difficulty"] = (
        df["student_accuracy_so_far"] - df["question_difficulty_estimate"]
    )

    df["recent_accuracy_minus_difficulty"] = (
        df["rolling_accuracy_20"] - df["question_difficulty_estimate"]
    )

    df["elapsed_time_ratio_vs_student_avg"] = safe_ratio(
        df["elapsed_time"],
        df["student_avg_elapsed_time_so_far"],
    )

    df["elapsed_time_ratio_vs_question_avg"] = safe_ratio(
        df["elapsed_time"],
        df["question_avg_elapsed_time_so_far"],
    )

    output_columns = [
        "student_id",
        "question_id",
        "timestamp",
        "elapsed_time",
        "part",
        "primary_tag",
        "tag_count",
        "student_attempt_count_so_far",
        "student_correct_count_so_far",
        "student_accuracy_so_far",
        "rolling_accuracy_3",
        "rolling_accuracy_20",
        "student_correct_streak",
        "student_incorrect_streak",
        "student_avg_elapsed_time_so_far",
        "student_elapsed_time_std_so_far",
        "question_attempt_count_so_far",
        "question_accuracy_so_far",
        "question_difficulty_estimate",
        "question_avg_elapsed_time_so_far",
        "student_unique_questions_so_far",
        "same_question_seen_before",
        "activity_gap_hours",
        "ability_minus_difficulty",
        "recent_accuracy_minus_difficulty",
        "elapsed_time_ratio_vs_student_avg",
        "elapsed_time_ratio_vs_question_avg",
        "is_correct",
    ]

    features = df[output_columns].copy()
    features.to_csv(OUTPUT_PATH, index=False)

    summary = pd.DataFrame(
        [
            {
                "rows": len(features),
                "students": features["student_id"].nunique(),
                "questions": features["question_id"].nunique(),
                "average_correctness": features["is_correct"].mean(),
                "feature_columns": len(output_columns) - 4,
                "output_path": str(OUTPUT_PATH),
            }
        ]
    )

    summary.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved features: {OUTPUT_PATH}")
    print(f"Saved summary: {SUMMARY_PATH}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()



   

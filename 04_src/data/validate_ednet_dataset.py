"""
Validate the mapped EdNet V2 dataset.

This script checks whether the processed EdNet subset follows the project format.
It should be run after prepare_ednet_subset.py creates:

02_data/processed/ednet/ednet_interactions_mapped.csv
"""

# from __future__ import annotations satırı, Python'da henüz yazılmamış veya tanımlanmamış sınıfları/tipleri kod içinde rahatça referans gösterebilmenizi sağlar.
# Normalde Python, bir fonksiyonu tanımlarken kullandığınız veri tiplerini (örneğin def bul(x: list[str])) anında çözmeye çalışır. Ancak bu satırı eklediğinizde, tip ipuçları (type hints) birer kod parçası yerine basit birer metin (string) gibi davranır.
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "05_experiments" / "configs" / "ednet_config.yaml"


REQUIRED_COLUMNS = [
    "student_id",
    "question_id",
    "timestamp",
    "tags",
    "elapsed_time",
    "is_correct",
]


# load_config() ve load_ednet_dataset(config): Projenin ayar dosyasını (YAML) okur ve bu ayarlara göre işlenmiş ana veri setini (CSV) projeye yükler. Eğer dosyalar yerinde yoksa hata fırlatır.
def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f'config file not found')
    
    with CONFIG_PATH.open('r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def load_ednet_dataset(config: dict) -> pd.DataFrame:
    dataset_path = PROJECT_ROOT / config["outputs"]["mapped_interactions"]

    if not dataset_path.exists():
        raise FileNotFoundError(
            f'mapped EdNet dataset not found\n'
            'run prepare_ednet_subset.py first'
        )
    
    return pd.read_csv(dataset_path)


# check_required_columns(df): Veri setinde projenin çalışması için olmazsa olmaz zorunlu sütunların (student_id, question_id vb.) eksiksiz mevcut olup olmadığını kontrol eder.
def check_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"missing required columns")



# check_missing_values(df): Öğrenci ID'si, soru ID'si ve doğruluk etiketi (is_correct) gibi kritik sütunlarda boş/eksik veri (NaN) olup olmadığına bakar. Eksik varsa işlemi durdurur.
def check_missing_values(df: pd.DataFrame) -> None:
    critical_columns = ["student_id", "question_id", "is_correct"]

    missing_summary = df[critical_columns].isna().sum()
    missing_total = int(missing_summary.sum())

    if missing_total > 0:
        raise ValueError(
            "critical missing values found:\n"
            f"{missing_summary}"
        )




# check_correctness_values(df): is_correct (doğru mu) sütununda sadece 0 (yanlış) ve 1 (doğru) değerlerinin olduğunu doğrular. Arada kaynamış farklı veya hatalı bir değer varsa yakalar.
def check_correctness_values(df: pd.DataFrame) -> None:
    unique_values = sorted(df["is_correct"].dropna().unique().tolist())

    valid_values = {0, 1}

    if not set(unique_values).issubset(valid_values):
        raise ValueError(
            f"is_correct must contain only 0 and 1 values. found: {unique_values}"
        )




# check_interaction_counts(df, config): Her bir öğrencinin veri setinde yeterli sayıda işlem (soru çözme) yapıp yapmadığını denetler. Ayarlarda belirlenen minimum işlem sayısının altında kalan öğrenci varsa hata verir.
def check_interaction_counts(df: pd.DataFrame, config: dict) -> None:
    min_required = int(config["dataset"]["min_interactions_per_student"])

    counts = df.groupby("student_id").size()

    if counts.min() < min_required:
        raise ValueError(
            f"Some students have fewer than {min_required} interactions. "
            f"Minimum found: {counts.min()}"
        )



# create_validation_summary(df): Tüm testleri geçen veri setinden; toplam öğrenci sayısı, soru sayısı, toplam etkileşim, ortalama başarı oranı ve öğrenci başına düşen soru sayıları gibi istatistikleri hesaplayarak özet bir rapor tablosu oluşturur.
def create_validation_summary(df: pd.DataFrame) -> pd.DataFrame:
    student_counts = df.groupby("student_id").size()

    summary = {
        "students": df["student_id"].nunique(),
        "questions": df["question_id"].nunique(),
        "interactions": len(df),
        "average_correctness": round(float(df["is_correct"].mean()), 4),
        "min_interactions_per_student": int(student_counts.min()),
        "max_interactions_per_student": int(student_counts.max()),
        "avg_interactions_per_student": round(float(student_counts.mean()), 2),
        "missing_elapsed_time": int(df["elapsed_time"].isna().sum()),
        "unique_tags": df["tags"].nunique(),
    }

    return pd.DataFrame([summary])



# save_validation_summary(summary_df): Hazırlanan bu özet rapor tablosunu sonuçlar klasörüne (06_results/...) yeni bir CSV dosyası olarak kaydeder.
def save_validation_summary(summary_df: pd.DataFrame) -> None:
    output_path = (
        PROJECT_ROOT
        / "06_results"
        / "tables"
        / "ednet"
        / "ednet_validation_summary.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_path, index=False)

    print(f"Validation summary saved to: {output_path}")


def main() -> None:
    config = load_config()
    df = load_ednet_dataset(config)

    check_required_columns(df)
    check_missing_values(df)
    check_correctness_values(df)
    check_interaction_counts(df, config)

    summary_df = create_validation_summary(df)
    save_validation_summary(summary_df)

    print("\nEdNet dataset validation passed.")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
"""
Prepare a controlled EdNet subset for V2 real-dataset validation.

This script:
1. Reads EdNet raw CSV files from 02_data/external/ednet
2. Maps them into the project format
3. Creates a controlled subset
4. Saves the mapped interactions to 02_data/processed/ednet

Main output:
02_data/processed/ednet/ednet_interactions_mapped.csv
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml

from ednet_schema import build_column_mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "05_experiments" / "configs" / "ednet_config.yaml"


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def read_csv_preview(path: Path, nrows: int = 5) -> pd.DataFrame:
    try:
        return pd.read_csv(path, nrows=nrows)
    except UnicodeDecodeError:
        return pd.read_csv(path, nrows=nrows, encoding="latin1")


def read_csv_file(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def is_metadata_file(path: Path) -> bool:
    name = path.name.lower()
    parent = path.parent.name.lower()

    keywords = [
        "question",
        "questions",
        "content",
        "contents",
        "metadata",
        "item",
    ]

    return any(keyword in name or keyword in parent for keyword in keywords)

# find_question_metadata(raw_dir): Veri setinin içinde soru id'lerini, doğru cevap anahtarlarını ve soruların hangi konu başlıklarına ait olduğunu (etiketlerini) barındıran soru meta veri (metadata) dosyasını arayıp bulur ve hafızaya yükler.
def find_question_metadata(raw_dir: Path) -> pd.DataFrame | None:
    csv_files = sorted(raw_dir.rglob("*.csv"))

    for file_path in csv_files:
        if not is_metadata_file(file_path):
            continue

        try:
            preview = read_csv_preview(file_path)
        except Exception:
            continue

        mapping = build_column_mapping(list(preview.columns))

        question_col = mapping.get("question_id")
        correct_answer_col = mapping.get("correct_answer")
        tags_col = mapping.get("tags")

        if question_col is None or correct_answer_col is None:
            continue

        metadata = read_csv_file(file_path)

        columns_to_keep = [question_col, correct_answer_col]
        if tags_col is not None:
            columns_to_keep.append(tags_col)

        metadata = metadata[columns_to_keep].copy()
        metadata = metadata.rename(
            columns={
                question_col: "question_id",
                correct_answer_col: "correct_answer",
            }
        )

        if tags_col is not None:
            metadata = metadata.rename(columns={tags_col: "tags_from_metadata"})

        metadata["question_id"] = metadata["question_id"].astype(str)
        metadata["correct_answer"] = metadata["correct_answer"].astype(str)

        if "tags_from_metadata" in metadata.columns:
            metadata["tags_from_metadata"] = metadata["tags_from_metadata"].astype(str)

        metadata = metadata.drop_duplicates(subset=["question_id"])

        print(f"Question metadata loaded from: {file_path}")
        print(f"Metadata rows: {len(metadata)}")

        return metadata

    print("No question metadata file found.")
    return None


def derive_student_id_from_filename(path: Path) -> str:
    name = path.stem
    return f"student_{name}"


def convert_correctness(series: pd.Series) -> pd.Series:
    values = (
        series.astype(str)
        .str.lower()
        .str.strip()
        .replace(
            {
                "true": "1",
                "false": "0",
                "correct": "1",
                "incorrect": "0",
                "yes": "1",
                "no": "0",
            }
        )
    )

    return pd.to_numeric(values, errors="coerce")



# map_interaction_file(file_path, question_metadata): Tek bir öğrenciye veya etkileşime ait olan ham bir CSV dosyasını okur; sütun isimlerini projenin ana formatına (student_id, question_id, is_correct vb.) dönüştürür. Eğer dosyada is_correct (doğruluk) sütunu yoksa, öğrencinin cevabı ile meta verideki doğru cevabı karşılaştırarak doğruluk değerini kendisi hesaplar.
def map_interaction_file(
    file_path: Path,
    question_metadata: pd.DataFrame | None,
) -> pd.DataFrame | None:
    raw_df = read_csv_file(file_path)

    if raw_df.empty:
        return None

    mapping = build_column_mapping(list(raw_df.columns))

    student_col = mapping.get("student_id")
    question_col = mapping.get("question_id")
    timestamp_col = mapping.get("timestamp")
    tags_col = mapping.get("tags")
    elapsed_col = mapping.get("elapsed_time")
    correct_col = mapping.get("is_correct")
    user_answer_col = mapping.get("user_answer")
    correct_answer_col = mapping.get("correct_answer")

    if question_col is None:
        return None

    mapped = pd.DataFrame()

    if student_col is not None:
        mapped["student_id"] = raw_df[student_col].astype(str)
    else:
        mapped["student_id"] = derive_student_id_from_filename(file_path)

    mapped["question_id"] = raw_df[question_col].astype(str)

    if timestamp_col is not None:
        mapped["timestamp"] = raw_df[timestamp_col]
    else:
        mapped["timestamp"] = range(len(raw_df))

    if tags_col is not None:
        mapped["tags"] = raw_df[tags_col].astype(str)
    else:
        mapped["tags"] = "unknown"

    if elapsed_col is not None:
        mapped["elapsed_time"] = pd.to_numeric(raw_df[elapsed_col], errors="coerce")
    else:
        mapped["elapsed_time"] = pd.NA

    if correct_col is not None:
        mapped["is_correct"] = convert_correctness(raw_df[correct_col])
    else:
        if user_answer_col is None:
            return None

        temp = mapped.copy()
        temp["user_answer"] = raw_df[user_answer_col].astype(str)

        if correct_answer_col is not None:
            temp["correct_answer"] = raw_df[correct_answer_col].astype(str)
        elif question_metadata is not None:
            temp = temp.merge(question_metadata, on="question_id", how="left")
        else:
            return None

        if "correct_answer" not in temp.columns:
            return None

        temp["is_correct"] = (
            temp["user_answer"].astype(str).str.strip()
            == temp["correct_answer"].astype(str).str.strip()
        ).astype(int)

        if "tags_from_metadata" in temp.columns:
            temp["tags"] = temp["tags_from_metadata"].fillna(temp["tags"])

        mapped = temp[
            [
                "student_id",
                "question_id",
                "timestamp",
                "tags",
                "elapsed_time",
                "is_correct",
            ]
        ].copy()

    mapped = clean_mapped_data(mapped)

    if mapped.empty:
        return None

    return mapped


# clean_mapped_data(df): Dönüştürülen verideki kritik sütunları temizler. Öğrenci ID'si veya soru ID'si boş olan satırları siler; is_correct sütunundaki değerlerin sadece 0 veya 1 olmasını garanti eder.
def clean_mapped_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["student_id", "question_id", "is_correct"]).copy()

    df["is_correct"] = pd.to_numeric(df["is_correct"], errors="coerce")
    df = df.dropna(subset=["is_correct"]).copy()
    df["is_correct"] = df["is_correct"].astype(int)
    df = df[df["is_correct"].isin([0, 1])].copy()

    df["student_id"] = df["student_id"].astype(str)
    df["question_id"] = df["question_id"].astype(str)
    df["tags"] = df["tags"].fillna("unknown").astype(str)
    df["elapsed_time"] = pd.to_numeric(df["elapsed_time"], errors="coerce")

    return df[
        [
            "student_id",
            "question_id",
            "timestamp",
            "tags",
            "elapsed_time",
            "is_correct",
        ]
    ]



def collect_interaction_files(raw_dir: Path) -> list[Path]:
    csv_files = sorted(raw_dir.rglob("*.csv"))
    return [path for path in csv_files if not is_metadata_file(path)]


# create_subset(df, config): Temizlenmiş devasa veri setinden, ayarlarda (ednet_config.yaml) belirtilen kriterlere göre (örneğin: minimum şu kadar soru çözmüş olan ve rastgele seçilen X kadar öğrenci) kontrollü bir alt küme filtrelemesi yapar. Öğrenci başına düşen maksimum etkileşim sınırını ayarlar.
def create_subset(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    dataset_config = config["dataset"]

    target_students = int(dataset_config["target_students"])
    target_interactions = int(dataset_config["target_interactions"])
    min_interactions = int(dataset_config["min_interactions_per_student"])
    max_interactions = int(dataset_config["max_interactions_per_student"])
    random_seed = int(dataset_config["random_seed"])

    counts = df.groupby("student_id").size()
    eligible_students = counts[counts >= min_interactions].index

    if len(eligible_students) == 0:
        raise ValueError("No students meet the minimum interaction requirement.")

    selected_students = (
        pd.Series(eligible_students)
        .sample(frac=1.0, random_state=random_seed)
        .head(target_students)
        .tolist()
    )

    subset = df[df["student_id"].isin(selected_students)].copy()

    subset["sort_order"] = pd.to_numeric(subset["timestamp"], errors="coerce")
    subset["sort_order"] = subset["sort_order"].fillna(
        subset.groupby("student_id").cumcount()
    )

    subset = subset.sort_values(["student_id", "sort_order"])

    per_student_cap = max(
        min_interactions,
        min(max_interactions, target_interactions // max(len(selected_students), 1)),
    )

    subset = subset.groupby("student_id", group_keys=False).head(per_student_cap)
    subset = subset.drop(columns=["sort_order"])

    if len(subset) > target_interactions:
        subset = subset.head(target_interactions)

    subset = subset.reset_index(drop=True)

    return subset


# save_subset(subset, config): Oluşturulan bu filtrelenmiş veriyi işlenmiş veriler klasörüne ednet_interactions_mapped.csv adıyla kaydeder. Hemen yanına kaç öğrenci, kaç soru ve ne kadar başarı oranı olduğunu özetleyen bir ednet_subset_metadata.json raporu bırakır.
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
    print(f"Saved to: {output_path}")
    print(f"Metadata saved to: {metadata_path}")
    print(json.dumps(metadata, indent=2))


# main(): Tüm akışı yönetir. Önce soru meta verilerini bulur, ardından binlerce etkileşim dosyasını sırayla okuyup birleştirir, en son aşamada ise bunlardan hedef ölçülerde bir alt küme oluşturup kaydeder.
def main() -> None:
    config = load_config()
    raw_dir = PROJECT_ROOT / config["dataset"]["raw_data_dir"]

    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw EdNet folder not found: {raw_dir}")

    print("Preparing EdNet subset...")
    print(f"Raw directory: {raw_dir}")

    question_metadata = find_question_metadata(raw_dir)
    interaction_files = collect_interaction_files(raw_dir)

    if not interaction_files:
        print("No interaction CSV files found.")
        return

    print(f"Interaction files found: {len(interaction_files)}")

    mapped_frames = []

    for index, file_path in enumerate(interaction_files, start=1):
        mapped = map_interaction_file(file_path, question_metadata)

        if mapped is not None:
            mapped_frames.append(mapped)

        if index % 1000 == 0:
            print(f"Processed {index} files...")

    if not mapped_frames:
        raise ValueError("No usable interaction data was mapped.")

    full_mapped = pd.concat(mapped_frames, ignore_index=True)

    print(f"Mapped interactions before subset: {len(full_mapped)}")
    print(f"Mapped students before subset: {full_mapped['student_id'].nunique()}")

    subset = create_subset(full_mapped, config)
    save_subset(subset, config)


if __name__ == "__main__":
    main()
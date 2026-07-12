from itertools import islice
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "02_data" / "external" / "ednet"


def inspect_csv_file(file_path: Path, n_rows: int = 5) -> None:
    print("=" * 80)
    print(f"File: {file_path}")
    print(f"Size: {file_path.stat().st_size / 1024:.2f} KB")

    df = pd.read_csv(file_path, nrows=n_rows)

    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nPreview:")
    print(df.head(n_rows))


def main() -> None:
    contents_dir = RAW_DATA_DIR / "contents"
    kt1_dir = RAW_DATA_DIR / "KT1"

    files_to_check = []

    questions_file = contents_dir / "questions.csv"
    if questions_file.exists():
        files_to_check.append(questions_file)

    if kt1_dir.exists():
        kt1_samples = list(islice(kt1_dir.glob("*.csv"), 5))
        files_to_check.extend(kt1_samples)

    print(f"Inspecting {len(files_to_check)} sample files only.")

    for file_path in files_to_check:
        inspect_csv_file(file_path)


if __name__ == "__main__":
    main()

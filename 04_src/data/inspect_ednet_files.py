from pathlib import Path

import pandas as pd



PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "02_data" / "external" / "ednet"

# inspect_csv_file(file_path, n_rows): Verilen bir CSV dosyasının genel yapısını inceleyen ana işlevsel fonksiyondur. Dosyanın diskteki boyutunu hesaplar, içindeki sütun isimlerini listeler ve dosyanın tamamını belleğe yüklemeden sadece ilk birkaç satırını (n_rows) okuyarak hızlıca bir önizleme ekrana basar. Ayrıca Türkçe veya özel karakterlerden kaynaklanabilecek okuma hatalarını (UnicodeDecodeError) önlemek için iki farklı karakter kodlamasını (utf-8 ve latin1) dener.
def inspect_csv_file(file_path: Path, n_rows: int = 5) -> None:
    print("=" * 80)
    print(f"File: {file_path}")
    print(f"Size: {file_path.stat().st_size / (1024 * 1024):.2f} MB")

    try:
        df = pd.read_csv(file_path, nrows=n_rows)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, nrows=n_rows, encoding='latin1')
    
    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nPreview:")
    print(df.head(n_rows))


# main(): Kodun akışını ve operasyon adımlarını yöneten ana kontrol fonksiyonudur. Hedef klasörün varlığını kontrol eder, klasör altındaki tüm CSV dosyalarını bulup listeler ve döngüye girerek bu dosyaların ilk 10 tanesini sırayla yukarıdaki inspect_csv_file fonksiyonuna göndererek analizi başlatı
def main() -> None:
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw EdNet folder not found: {RAW_DATA_DIR}")

    csv_files = sorted(RAW_DATA_DIR.rglob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        print(f"Place EdNet CSV files inside: {RAW_DATA_DIR}")
        return

    print(f"Found {len(csv_files)} CSV files.")

    for file_path in csv_files[:10]:
        inspect_csv_file(file_path)


if __name__ == "__main__":
    main()
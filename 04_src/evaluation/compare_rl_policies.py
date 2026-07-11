"""
Compare RL policies for the Adaptive AI Tutor Research Lab.

Goal:
Compare random policy results with Q-learning results.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RANDOM_POLICY_PATH = PROJECT_ROOT / "06_results" / "tables" / "rl_random_policy_results.csv"
Q_LEARNING_PATH = PROJECT_ROOT / "06_results" / "tables" / "q_learning_results.csv"

OUTPUT_DIR = PROJECT_ROOT / "06_results" / "tables"
OUTPUT_PATH = OUTPUT_DIR / "rl_policy_comparison.csv"


# load_results: İki farklı yönteme ait .csv sonuç dosyalarını bilgisayardan yükler. Karışıklığı önlemek için verilerin sonuna "random_policy" veya "q_learning" yazan yeni bir ayırt edici sütun ekler.
def load_results(path: Path, policy_name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    dataframe = pd.read_csv(path)
    dataframe["policy"] = policy_name

    return dataframe


# summarize_policies: İki yöntemin tüm verilerini gruplayarak; hamle başına düşen ortalama ödülü, öğrencilerin soruları doğru yanıtlama oranını, yapay zekanın isabetli soru tahmin olasılığını ve toplam atılan adım sayısını hesaplayıp 3 basamaklı hassasiyetle özetler.
def summarize_policies(dataframe: pd.DataFrame) -> pd.DataFrame:
    summary_df = (
        dataframe.groupby("policy")
        .agg(
            average_reward=("reward", "mean"),
            average_correctness=("is_correct", "mean"),
            average_probability_correct=("probability_correct", "mean"),
            total_steps=("reward", "count"),
        )
        .round(3)
        .reset_index()
    )

    return summary_df



# main: Karşılaştırma motorudur. Her iki yöntemin verilerini yükler, pd.concat ile alt alta birleştirir, summarize_policies ile aralarındaki performans farkını hesaplar ve bu nihai karşılaştırma tablosunu ekrana basıp yeni bir .csv dosyası olarak kaydeder.
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    random_df = load_results(RANDOM_POLICY_PATH, "random_policy")
    q_learning_df = load_results(Q_LEARNING_PATH, "q_learning")

    combined_df = pd.concat([random_df, q_learning_df], ignore_index=True)

    comparison_df = summarize_policies(combined_df)
    comparison_df.to_csv(OUTPUT_PATH, index=False)

    print("RL policy comparison completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nPolicy comparison:")
    print(comparison_df)


if __name__ == "__main__":
    main()
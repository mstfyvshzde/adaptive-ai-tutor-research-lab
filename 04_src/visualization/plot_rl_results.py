"""
Plot RL results for the Adaptive AI Tutor Research Lab.

Goal:
Create visualizations for Q-learning and policy comparison results.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

Q_LEARNING_PATH = PROJECT_ROOT / "06_results" / "tables" / "q_learning_results.csv"
POLICY_COMPARISON_PATH = PROJECT_ROOT / "06_results" / "tables" / "rl_policy_comparison.csv"

OUTPUT_DIR = PROJECT_ROOT / "06_results" / "figures" / "rl"
Q_LEARNING_REWARD_PLOT = OUTPUT_DIR / "q_learning_reward_curve.png"
POLICY_COMPARISON_PLOT = OUTPUT_DIR / "rl_policy_comparison.png"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    return pd.read_csv(path)


# plot_q_learning_reward_curve: Q-Learning ajanının zaman içindeki öğrenme eğrisini (çizgi grafiğini) çizer. Her eğitim turundaki (episode) toplam ödülü silik, son 10 turun hareketli ortalamasını (rolling_reward) ise kalın bir çizgiyle gösterir; böylece yapay zekanın turlar ilerledikçe akıllanıp akıllanmadığı (çizginin yukarı gidip gitmediği) net bir şekilde anlaşılır.
def plot_q_learning_reward_curve(q_learning_df: pd.DataFrame) -> None:
    episode_summary = (
        q_learning_df.groupby("episode")
        .agg(total_reward=("reward", "sum"))
        .reset_index()
    )

    episode_summary["rolling_reward"] = (
        episode_summary["total_reward"]
        .rolling(window=10, min_periods=1)
        .mean()
    )

    plt.figure(figsize=(9, 5))
    plt.plot(
        episode_summary["episode"],
        episode_summary["total_reward"],
        label="Episode reward",
        alpha=0.5,
    )
    plt.plot(
        episode_summary["episode"],
        episode_summary["rolling_reward"],
        label="Rolling average reward",
        linewidth=2,
    )

    plt.title("Q-Learning Reward Curve")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.legend()
    plt.tight_layout()
    plt.savefig(Q_LEARNING_REWARD_PLOT, dpi=200)
    plt.close()


# plot_policy_comparison: İki yöntemin (Rastgele vs. Q-Learning) performansını kıyaslayan bir sütun (bar) grafiği oluşturur. Yan yana iki dik sütun basarak hangi politikanın adım başına daha yüksek ortalama ödül getirdiğini anında gösterir.
def plot_policy_comparison(policy_df: pd.DataFrame) -> None:
    plt.figure(figsize=(7, 5))
    plt.bar(policy_df["policy"], policy_df["average_reward"])

    plt.title("Average Reward by Policy")
    plt.xlabel("Policy")
    plt.ylabel("Average Reward")
    plt.tight_layout()
    plt.savefig(POLICY_COMPARISON_PLOT, dpi=200)
    plt.close()


# main: Grafikleri kaydetmek için bilgisayarda bir klasör (figures/rl) oluşturur, .csv sonuç dosyalarını içeri aktarır, yukarıdaki iki görselleştirme fonksiyonunu tetikleyip grafikleri .png formatında resim olarak kaydeder
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    q_learning_df = load_csv(Q_LEARNING_PATH)
    policy_df = load_csv(POLICY_COMPARISON_PATH)

    plot_q_learning_reward_curve(q_learning_df)
    plot_policy_comparison(policy_df)

    print("RL plots created successfully.")
    print(f"Q-learning reward curve saved to: {Q_LEARNING_REWARD_PLOT}")
    print(f"Policy comparison plot saved to: {POLICY_COMPARISON_PLOT}")


if __name__ == "__main__":
    main()
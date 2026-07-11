"""
Simple RL tutor environment for the Adaptive AI Tutor Research Lab.

Goal:
Create a small simulation where the tutor chooses question difficulty
and receives reward based on student performance.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "02_data" / "processed" / "demo_features.csv"
OUTPUT_DIR = PROJECT_ROOT / "06_results" / "tables"
OUTPUT_PATH = OUTPUT_DIR / "rl_random_policy_results.csv"

RANDOM_SEED = 17
MAX_STEPS = 10

ACTIONS = ["easy", "medium", "hard"]

# TutorEnvironment (Sınıf): Yapay zekanın içinde oynayacağı eğitim simülatörüdür (ortamıdır). Soru bankasını hazırlar, öğrencileri sisteme yükler ve yapay zekanın hamlelerine göre öğrencilerin doğru cevap verip vermeyeceğini simüle eder.
class TutorEnvironment:
    def __init__(self, data: pd.DataFrame, random_seed: int = RANDOM_SEED):
        self.data = data
        self.rng = np.random.default_rng(random_seed)
        self.question_bank = self._build_question_bank()

        self.student_profile = None
        self.recent_results = []
        self.current_step = 0

    def _build_question_bank(self) -> pd.DataFrame:
        return (
            self.data.groupby("question_id")
            .agg(
                tags=("tags", "first"),
                difficulty=("difficulty", "first"),
                difficulty_score=("difficulty_score", "mean"),
            )
            .reset_index()
        )
    
    # reset: Yeni bir eğitim seansı (bölümü) başlatır. Rastgele bir öğrenci seçer, bu öğrencinin son başarı oranını ve en zayıf olduğu konuyu (weak_topic) belirleyerek sistemi başlangıç durumuna getirir.
    def reset(self) -> dict:
        student_id = self.rng.choice(self.data["student_id"].unique())
        student_df = self.data[self.data["student_id"] == student_id]

        weak_topic = student_df.groupby("tags")["is_correct"].mean().idxmin()
        recent_accuracy = (
            student_df.sort_values("timestamp")
            .tail(5)["is_correct"]
            .mean()
        )

        self.student_profile = {
            "student_id": student_id,
            "recent_accuracy": float(recent_accuracy),
            "weak_topic": weak_topic,
        }

        self.recent_results = []
        self.current_step = 0

        return self._get_state()
    
    def _get_state(self) -> dict:
        if self.recent_results:
            recent_accuracy = float(np.mean(self.recent_results))
        else:
            recent_accuracy = self.student_profile["recent_accuracy"]

        return {
            "student_id": self.student_profile["student_id"],
            "recent_accuracy": recent_accuracy,
            "weak_topic": self.student_profile["weak_topic"],
            "step": self.current_step,
        }

    def _sample_question(self, difficulty: str) -> pd.Series:
        candidates = self.question_bank[
            self.question_bank["difficulty"] == difficulty
        ]

        if candidates.empty:
            candidates = self.question_bank

        return candidates.sample(
            1,
            random_state=int(self.rng.integers(0, 1_000_000)),
        ).iloc[0]
    

    # step: Yapay zekanın seçtiği zorluk derecesine ("easy", "medium", "hard") göre havuzdan rastgele bir soru çeker. Öğrencinin güncel başarı durumu ile sorunun zorluğunu kıyaslayarak soruyu doğru bilip bilemeyeceğine dair bir olasılık hesabı yapar ve soruyu bilirse sisteme artı ödül (reward), bilemezse eksi/düşük ödül döndürür. Eğer soru öğrencinin zayıf olduğu konudansa fazladan ödül ekler; çok kolay veya çok zor kaldıysa ceza puanı keser.
    def step(self, action: str) -> tuple[dict, float, bool, dict]:
        if action not in ACTIONS:
            raise ValueError(f"Invalid action: {action}")

        question = self._sample_question(action)

        state = self._get_state()
        recent_accuracy = state["recent_accuracy"]
        difficulty_score = float(question["difficulty_score"])

        probability_correct = recent_accuracy - difficulty_score + 0.55
        probability_correct = float(np.clip(probability_correct, 0.05, 0.95))

        is_correct = int(self.rng.random() < probability_correct)

        reward = float(is_correct)

        if question["tags"] == self.student_profile["weak_topic"]:
            reward += 0.25

        if probability_correct > 0.90:
            reward -= 0.10

        if probability_correct < 0.20:
            reward -= 0.20

        self.recent_results.append(is_correct)
        self.current_step += 1

        done = self.current_step >= MAX_STEPS
        next_state = self._get_state()

        info = {
            "recommended_question_id": int(question["question_id"]),
            "recommended_topic": question["tags"],
            "recommended_difficulty": question["difficulty"],
            "probability_correct": probability_correct,
            "is_correct": is_correct,
        }

        return next_state, reward, done, info


def load_features(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}. Run build_features.py first."
        )

    dataframe = pd.read_csv(path)
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])

    return dataframe


# run_random_policy: Yazılan bu RL ortamını test etmek için çalışan ana döngüdür. Yapay zeka gibi davranarak tamamen rastgele zorluklar seçer (easy, medium veya hard), bunları ortama gönderir ve her adımdaki ödülleri, doğruluk durumlarını toplayarak bir tabloya kaydeder.
def run_random_policy(
    environment: TutorEnvironment,
    episodes: int = 20,
) -> pd.DataFrame:
    rows = []

    for episode in range(1, episodes + 1):
        state = environment.reset()
        done = False
        total_reward = 0.0

        while not done:
            action = str(environment.rng.choice(ACTIONS))
            next_state, reward, done, info = environment.step(action)

            total_reward += reward

            rows.append(
                {
                    "episode": episode,
                    "step": state["step"],
                    "student_id": state["student_id"],
                    "action": action,
                    "reward": reward,
                    "total_reward_so_far": total_reward,
                    "recommended_question_id": info["recommended_question_id"],
                    "recommended_topic": info["recommended_topic"],
                    "recommended_difficulty": info["recommended_difficulty"],
                    "probability_correct": info["probability_correct"],
                    "is_correct": info["is_correct"],
                }
            )

            state = next_state

    return pd.DataFrame(rows)


# main: Tüm süreci başlatan ana motordur. Veriyi yükler, simülatörü (TutorEnvironment) kurar, rastgele politayı çalıştırır ve elde edilen başarı/ödül sonuçlarını en sonda bir .csv dosyası olarak bilgisayara kaydeder.
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_features(INPUT_PATH)
    environment = TutorEnvironment(data)

    results_df = run_random_policy(environment)
    results_df.to_csv(OUTPUT_PATH, index=False)

    print("RL environment test completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Average reward: {results_df['reward'].mean():.3f}")
    print(f"Average correctness: {results_df['is_correct'].mean():.3f}")


if __name__ == "__main__":
    main()
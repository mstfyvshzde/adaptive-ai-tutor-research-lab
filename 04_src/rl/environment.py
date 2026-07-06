"""
Simple RL tutor environment for the Adaptive AI Tutor Research Lab.

Goal:
Create a small simulation environment where an AI tutor chooses the next question difficulty.

This is the first reinforcement learning foundation of the project.
"""

from pathlib import Path

import numpy as np
import pandas as pd


INPUT_PATH = Path("02_data/processed/demo_features.csv")
OUTPUT_DIR = Path("06_results/tables")
OUTPUT_PATH = OUTPUT_DIR / "rl_random_policy_results.csv"

RANDOM_SEED = 17
MAX_STEPS = 10

ACTIONS = ["easy", "medium", "hard"]


class TutorEnvironment:
    """A simple tutoring environment for RL experiments."""

    def __init__(self, data: pd.DataFrame, random_seed: int = RANDOM_SEED):
        self.data = data
        self.rng = np.random.default_rng(random_seed)
        self.question_bank = self._build_question_bank()
        self.student_profile = None
        self.recent_results = []
        self.current_step = 0

    def _build_question_bank(self) -> pd.DataFrame:
        """Create unique question bank."""

        return (
            self.data.groupby("question_id")
            .agg(
                tags=("tags", "first"),
                difficulty=("difficulty", "first"),
                difficulty_score=("difficulty_score", "mean"),
            )
            .reset_index()
        )

    def reset(self) -> dict:
        """Start a new student episode."""

        student_id = self.rng.choice(self.data["student_id"].unique())
        student_df = self.data[self.data["student_id"] == student_id]

        weak_topic = student_df.groupby("tags")["is_correct"].mean().idxmin()
        recent_accuracy = student_df.sort_values("timestamp").tail(5)["is_correct"].mean()

        self.student_profile = {
            "student_id": student_id,
            "recent_accuracy": float(recent_accuracy),
            "weak_topic": weak_topic,
        }

        self.recent_results = []
        self.current_step = 0

        return self._get_state()

    def _get_state(self) -> dict:
        """Return current environment state."""

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
        """Sample a question with selected difficulty."""

        candidates = self.question_bank[self.question_bank["difficulty"] == difficulty]

        if candidates.empty:
            candidates = self.question_bank

        return candidates.sample(
            1,
            random_state=int(self.rng.integers(0, 1_000_000)),
        ).iloc[0]

    def step(self, action: str) -> tuple[dict, float, bool, dict]:
        """Take one tutor action."""

        if action not in ACTIONS:
            raise ValueError(f"Invalid action: {action}. Choose from {ACTIONS}.")

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
    """Load feature dataset."""

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}. Run build_features.py first.")

    dataframe = pd.read_csv(path)
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])

    return dataframe


def run_random_policy(environment: TutorEnvironment, episodes: int = 20) -> pd.DataFrame:
    """Run a random policy as the first RL baseline."""

    rows = []

    for episode in range(1, episodes + 1):
        state = environment.reset()
        done = False
        total_reward = 0

        while not done:
            action = environment.rng.choice(ACTIONS)
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


def main() -> None:
    """Run the first RL environment test."""

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


# NOTES
# This file creates the first simple RL tutoring environment.
#
# Agent:
# The AI tutor.
#
# State:
# Student recent accuracy, weak topic, and current step.
#
# Action:
# Choose question difficulty: easy, medium, or hard.
#
# Reward:
# Positive reward for correct answer.
# Small bonus for targeting weak topic.
# Small penalty for questions that are too easy or too hard.
#
# This is not the final RL system.
# It is the first working environment for testing RL logic.
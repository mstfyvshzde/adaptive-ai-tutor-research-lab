"""
Q-Learning agent for the Adaptive AI Tutor Research Lab.

Goal:
Train a simple RL agent that learns which difficulty level to recommend:
easy, medium, or hard.

This script uses the TutorEnvironment from environment.py.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from environment import ACTIONS, INPUT_PATH, TutorEnvironment, load_features


OUTPUT_DIR = Path("06_results/tables")
OUTPUT_PATH = OUTPUT_DIR / "q_learning_results.csv"

RANDOM_SEED = 17
EPISODES = 100
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.2


def state_to_key(state: dict) -> str:
    """Convert continuous state into a simple discrete state key."""

    recent_accuracy = state["recent_accuracy"]

    if recent_accuracy < 0.50:
        accuracy_level = "low"
    elif recent_accuracy < 0.75:
        accuracy_level = "medium"
    else:
        accuracy_level = "high"

    return f"{accuracy_level}_step_{state['step']}"


def choose_action(
    q_table: dict,
    state_key: str,
    rng: np.random.Generator,
) -> str:
    """Choose action using epsilon-greedy strategy."""

    if rng.random() < EPSILON:
        return str(rng.choice(ACTIONS))

    if state_key not in q_table:
        q_table[state_key] = {action: 0.0 for action in ACTIONS}

    return max(q_table[state_key], key=q_table[state_key].get)


def update_q_value(
    q_table: dict,
    state_key: str,
    action: str,
    reward: float,
    next_state_key: str,
) -> None:
    """Update Q-value using the Q-learning formula."""

    if state_key not in q_table:
        q_table[state_key] = {action_name: 0.0 for action_name in ACTIONS}

    if next_state_key not in q_table:
        q_table[next_state_key] = {action_name: 0.0 for action_name in ACTIONS}

    old_value = q_table[state_key][action]
    best_next_value = max(q_table[next_state_key].values())

    new_value = old_value + ALPHA * (
        reward + GAMMA * best_next_value - old_value
    )

    q_table[state_key][action] = new_value


def train_q_learning_agent(environment: TutorEnvironment) -> pd.DataFrame:
    """Train Q-learning agent in the tutor environment."""

    rng = np.random.default_rng(RANDOM_SEED)
    q_table = {}
    rows = []

    for episode in range(1, EPISODES + 1):
        state = environment.reset()
        done = False
        total_reward = 0.0

        while not done:
            state_key = state_to_key(state)
            action = choose_action(q_table, state_key, rng)

            next_state, reward, done, info = environment.step(action)
            next_state_key = state_to_key(next_state)

            update_q_value(
                q_table=q_table,
                state_key=state_key,
                action=action,
                reward=reward,
                next_state_key=next_state_key,
            )

            total_reward += reward

            rows.append(
                {
                    "episode": episode,
                    "step": state["step"],
                    "state_key": state_key,
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
    """Run Q-learning training."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_features(INPUT_PATH)
    environment = TutorEnvironment(data)

    results_df = train_q_learning_agent(environment)
    results_df.to_csv(OUTPUT_PATH, index=False)

    episode_summary = (
        results_df.groupby("episode")
        .agg(
            total_reward=("reward", "sum"),
            avg_correctness=("is_correct", "mean"),
        )
        .reset_index()
    )

    print("Q-learning training completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Average reward per step: {results_df['reward'].mean():.3f}")
    print(f"Average correctness: {results_df['is_correct'].mean():.3f}")
    print("\nLast 5 episode summaries:")
    print(episode_summary.tail())


if __name__ == "__main__":
    main()


# NOTES
# This file trains a simple Q-learning agent.
#
# State:
# We convert recent_accuracy into low / medium / high.
#
# Action:
# The agent chooses easy, medium, or hard.
#
# Reward:
# Comes from the TutorEnvironment.
#
# Epsilon-greedy:
# Sometimes the agent explores random actions.
# Other times it chooses the best known action.
#
# Q-table:
# Stores how valuable each action is for each state.
#
# This is the first learning-based RL policy.
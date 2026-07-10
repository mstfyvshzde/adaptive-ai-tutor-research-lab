"""
Run the full Adaptive AI Tutor Research Lab pipeline.

Goal:
Execute data creation, validation, feature engineering, models,
evaluation, and visualization with one command.
"""

import subprocess
import sys


SCRIPTS = [
    "04_src/data/create_demo_dataset.py",
    "04_src/data/validate_demo_dataset.py",
    "04_src/features/build_features.py",
    "04_src/models/supervised_baselines.py",
    "04_src/models/clustering.py",
    "04_src/models/recommender.py",
    "04_src/rl/environment.py",
    "04_src/rl/q_learning_agent.py",
    "04_src/evaluation/compare_rl_policies.py",
    "04_src/visualization/plot_supervised_results.py",
    "04_src/visualization/plot_rl_results.py",
]


def run_script(script_path: str) -> None:
    print("\n" + "=" * 70)
    print(f"Running: {script_path}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, script_path],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline stopped. Failed script: {script_path}")


def main() -> None:
    """Run all project scripts in order."""

    for script in SCRIPTS:
        run_script(script)

    print("\nFull pipeline completed successfully.")


if __name__ == "__main__":
    main()
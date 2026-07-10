"""
Smoke test for the Adaptive AI Tutor Research Lab.

Goal:
Check that the full pipeline runs successfully and creates key outputs.
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_OUTPUTS = [
    "07_demo/demo_data/demo_questions.csv",
    "07_demo/demo_data/demo_interactions.csv",
    "02_data/processed/demo_features.csv",
    "06_results/tables/supervised_baseline_metrics.csv",
    "06_results/tables/student_clusters.csv",
    "06_results/tables/cluster_summary.csv",
    "06_results/tables/recommendation_examples.csv",
    "06_results/tables/rl_random_policy_results.csv",
    "06_results/tables/q_learning_results.csv",
    "06_results/tables/rl_policy_comparison.csv",
    "06_results/figures/supervised/supervised_roc_auc_comparison.png",
    "06_results/figures/supervised/supervised_log_loss_comparison.png",
    "06_results/figures/clustering/student_clusters_pca.png",
    "06_results/figures/rl/q_learning_reward_curve.png",
    "06_results/figures/rl/rl_policy_comparison.png",
]


def test_full_pipeline_runs_successfully() -> None:
    """Run the full pipeline and check expected output files."""

    result = subprocess.run(
        [sys.executable, "run_pipeline.py"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, (
        "Pipeline failed.\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )

    for output_path in EXPECTED_OUTPUTS:
        full_path = PROJECT_ROOT / output_path
        assert full_path.exists(), f"Missing expected output: {output_path}"
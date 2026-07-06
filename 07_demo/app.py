"""
Streamlit demo app for the Adaptive AI Tutor Research Lab.

Run:
streamlit run 07_demo/app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SUPERVISED_RESULTS_PATH = PROJECT_ROOT / "06_results/tables/supervised_baseline_metrics.csv"
CLUSTER_SUMMARY_PATH = PROJECT_ROOT / "06_results/tables/cluster_summary.csv"
RECOMMENDATIONS_PATH = PROJECT_ROOT / "06_results/tables/recommendation_examples.csv"
RL_COMPARISON_PATH = PROJECT_ROOT / "06_results/tables/rl_policy_comparison.csv"

SUPERVISED_ROC_PLOT = PROJECT_ROOT / "06_results/figures/supervised/supervised_roc_auc_comparison.png"
SUPERVISED_LOG_LOSS_PLOT = PROJECT_ROOT / "06_results/figures/supervised/supervised_log_loss_comparison.png"
Q_LEARNING_PLOT = PROJECT_ROOT / "06_results/figures/rl/q_learning_reward_curve.png"
RL_POLICY_PLOT = PROJECT_ROOT / "06_results/figures/rl/rl_policy_comparison.png"
CLUSTER_PLOT = PROJECT_ROOT / "06_results/figures/clustering/student_clusters_pca.png"


def load_csv(path: Path) -> pd.DataFrame:
    """Load CSV safely."""

    if not path.exists():
        st.warning(f"Missing file: {path}")
        return pd.DataFrame()

    return pd.read_csv(path)


def show_image(path: Path, caption: str) -> None:
    """Show image if it exists."""

    if path.exists():
        st.image(str(path), caption=caption)
    else:
        st.warning(f"Missing plot: {path}")


def main() -> None:
    """Run Streamlit demo."""

    st.set_page_config(
        page_title="Adaptive AI Tutor Research Lab",
        layout="wide",
    )

    st.title("Adaptive AI Tutor Research Lab")
    st.write(
        "A research-style AI project combining knowledge tracing, "
        "student clustering, recommendation baselines, and reinforcement learning."
    )

    st.info(
        "If tables or plots are missing, run: python run_pipeline.py"
    )

    tab_overview, tab_supervised, tab_clusters, tab_recommender, tab_rl = st.tabs(
        [
            "Overview",
            "Knowledge Tracing",
            "Student Clusters",
            "Recommendations",
            "Reinforcement Learning",
        ]
    )

    with tab_overview:
        st.header("Project Overview")
        st.write(
            """
            This project simulates an adaptive AI tutor.

            The system:
            - creates a demo student-learning dataset
            - builds student knowledge features
            - trains supervised baseline models
            - groups students into behavior clusters
            - recommends next questions
            - compares random policy and Q-learning policy
            """
        )

    with tab_supervised:
        st.header("Knowledge Tracing Results")

        supervised_df = load_csv(SUPERVISED_RESULTS_PATH)

        if not supervised_df.empty:
            st.dataframe(supervised_df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            show_image(SUPERVISED_ROC_PLOT, "ROC-AUC Comparison")

        with col2:
            show_image(SUPERVISED_LOG_LOSS_PLOT, "Log Loss Comparison")

    with tab_clusters:
        st.header("Student Behavior Clusters")

        cluster_df = load_csv(CLUSTER_SUMMARY_PATH)

        if not cluster_df.empty:
            st.dataframe(cluster_df, use_container_width=True)

        show_image(CLUSTER_PLOT, "Student Clusters PCA Plot")

    with tab_recommender:
        st.header("Recommendation Examples")

        recommendations_df = load_csv(RECOMMENDATIONS_PATH)

        if not recommendations_df.empty:
            st.dataframe(
                recommendations_df.head(30),
                use_container_width=True,
            )

    with tab_rl:
        st.header("Reinforcement Learning Results")

        rl_df = load_csv(RL_COMPARISON_PATH)

        if not rl_df.empty:
            st.dataframe(rl_df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            show_image(Q_LEARNING_PLOT, "Q-Learning Reward Curve")

        with col2:
            show_image(RL_POLICY_PLOT, "RL Policy Comparison")


if __name__ == "__main__":
    main()

"""
Streamlit demo app for the Adaptive AI Tutor Research Lab.

Goal:
Show the project results in a simple interactive dashboard.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURES_PATH = PROJECT_ROOT / "02_data" / "processed" / "demo_features.csv"
SUPERVISED_RESULTS_PATH = PROJECT_ROOT / "06_results" / "tables" / "supervised_baseline_metrics.csv"
CLUSTER_SUMMARY_PATH = PROJECT_ROOT / "06_results" / "tables" / "cluster_summary.csv"
RECOMMENDATIONS_PATH = PROJECT_ROOT / "06_results" / "tables" / "recommendation_examples.csv"
RL_COMPARISON_PATH = PROJECT_ROOT / "06_results" / "tables" / "rl_policy_comparison.csv"

SUPERVISED_ROC_PLOT = (
    PROJECT_ROOT
    / "06_results"
    / "figures"
    / "supervised"
    / "supervised_roc_auc_comparison.png"
)

SUPERVISED_LOG_LOSS_PLOT = (
    PROJECT_ROOT
    / "06_results"
    / "figures"
    / "supervised"
    / "supervised_log_loss_comparison.png"
)

CLUSTER_PLOT = (
    PROJECT_ROOT
    / "06_results"
    / "figures"
    / "clustering"
    / "student_clusters_pca.png"
)

RL_REWARD_PLOT = (
    PROJECT_ROOT
    / "06_results"
    / "figures"
    / "rl"
    / "q_learning_reward_curve.png"
)

RL_POLICY_PLOT = (
    PROJECT_ROOT
    / "06_results"
    / "figures"
    / "rl"
    / "rl_policy_comparison.png"
)


st.set_page_config(
    page_title="Adaptive AI Tutor Research Lab",
    page_icon="🧠",
    layout="wide",
)


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def show_missing_file_message(path: Path) -> None:
    st.warning(
        f"Missing file: `{path}`. "
        "Please run `python run_pipeline.py` first."
    )


def show_project_overview(features_df: pd.DataFrame) -> None:
    st.title("🧠 Adaptive AI Tutor Research Lab")

    st.write(
        "This project explores how an AI tutor can estimate student knowledge, "
        "recommend learning activities, and improve decisions using reinforcement learning."
    )

    if features_df.empty:
        show_missing_file_message(FEATURES_PATH)
        return

    total_students = features_df["student_id"].nunique()
    total_questions = features_df["question_id"].nunique()
    total_interactions = len(features_df)
    average_correctness = features_df["is_correct"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Students", total_students)
    col2.metric("Questions", total_questions)
    col3.metric("Interactions", total_interactions)
    col4.metric("Average Correctness", f"{average_correctness:.2%}")


def show_data_section(features_df: pd.DataFrame) -> None:
    st.header("1. Student Learning Data")

    st.write(
        "The project uses a synthetic student interaction dataset. "
        "Each row represents one student answering one question."
    )

    if features_df.empty:
        show_missing_file_message(FEATURES_PATH)
        return

    st.dataframe(features_df.head(20), use_container_width=True)

    st.subheader("Average Correctness by Topic")
    topic_summary = (
        features_df.groupby("tags")
        .agg(
            attempts=("is_correct", "count"),
            average_correctness=("is_correct", "mean"),
        )
        .round(3)
        .reset_index()
    )

    st.dataframe(topic_summary, use_container_width=True)


def show_supervised_section(supervised_df: pd.DataFrame) -> None:
    st.header("2. Supervised Knowledge Tracing")

    st.write(
        "This section predicts whether a student will answer correctly using "
        "features such as previous accuracy, topic history, and question difficulty."
    )

    if supervised_df.empty:
        show_missing_file_message(SUPERVISED_RESULTS_PATH)
        return

    st.dataframe(supervised_df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if SUPERVISED_ROC_PLOT.exists():
            st.image(str(SUPERVISED_ROC_PLOT), caption="ROC-AUC comparison")
        else:
            show_missing_file_message(SUPERVISED_ROC_PLOT)

    with col2:
        if SUPERVISED_LOG_LOSS_PLOT.exists():
            st.image(str(SUPERVISED_LOG_LOSS_PLOT), caption="Log Loss comparison")
        else:
            show_missing_file_message(SUPERVISED_LOG_LOSS_PLOT)


def show_clustering_section(cluster_df: pd.DataFrame) -> None:
    st.header("3. Student Clustering")

    st.write(
        "This section groups students based on learning behavior such as "
        "accuracy, activity level, topic diversity, and progress."
    )

    if cluster_df.empty:
        show_missing_file_message(CLUSTER_SUMMARY_PATH)
        return

    st.dataframe(cluster_df, use_container_width=True)

    if CLUSTER_PLOT.exists():
        st.image(str(CLUSTER_PLOT), caption="Student clusters using PCA")
    else:
        show_missing_file_message(CLUSTER_PLOT)


def show_recommender_section(recommendations_df: pd.DataFrame) -> None:
    st.header("4. Recommendation System")

    st.write(
        "This section shows example recommendations from simple tutor policies: "
        "random recommendation, difficulty-based recommendation, and weak-topic recommendation."
    )

    if recommendations_df.empty:
        show_missing_file_message(RECOMMENDATIONS_PATH)
        return

    st.dataframe(recommendations_df.head(30), use_container_width=True)


def show_rl_section(rl_df: pd.DataFrame) -> None:
    st.header("5. Reinforcement Learning Tutor")

    st.write(
        "This section compares a random tutor policy with a Q-learning tutor. "
        "The goal is to test whether the tutor can learn better decisions over time."
    )

    if rl_df.empty:
        show_missing_file_message(RL_COMPARISON_PATH)
        return

    st.dataframe(rl_df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if RL_REWARD_PLOT.exists():
            st.image(str(RL_REWARD_PLOT), caption="Q-learning reward curve")
        else:
            show_missing_file_message(RL_REWARD_PLOT)

    with col2:
        if RL_POLICY_PLOT.exists():
            st.image(str(RL_POLICY_PLOT), caption="RL policy comparison")
        else:
            show_missing_file_message(RL_POLICY_PLOT)


def main() -> None:
    features_df = load_csv(FEATURES_PATH)
    supervised_df = load_csv(SUPERVISED_RESULTS_PATH)
    cluster_df = load_csv(CLUSTER_SUMMARY_PATH)
    recommendations_df = load_csv(RECOMMENDATIONS_PATH)
    rl_df = load_csv(RL_COMPARISON_PATH)

    show_project_overview(features_df)

    st.divider()
    show_data_section(features_df)

    st.divider()
    show_supervised_section(supervised_df)

    st.divider()
    show_clustering_section(cluster_df)

    st.divider()
    show_recommender_section(recommendations_df)

    st.divider()
    show_rl_section(rl_df)


if __name__ == "__main__":
    main()
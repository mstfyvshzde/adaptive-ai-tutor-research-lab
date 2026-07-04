"""
Student behavior clustering for the Adaptive AI Tutor Research Lab.

This script groups students based on their learning behavior.

Goal:
Find different learner profiles such as:

- strong learners
- struggling learners
- slow but improving learners
- inconsistent learners

Input:
02_data/processed/demo_features.csv

Outputs:
06_results/tables/student_clusters.csv
06_results/tables/cluster_summary.csv
06_results/figures/clustering/student_clusters_pca.png
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


INPUT_PATH = Path("02_data/processed/demo_features.csv")

OUTPUT_TABLE_DIR = Path("06_results/tables")
OUTPUT_FIGURE_DIR = Path("06_results/figures/clustering")

STUDENT_CLUSTERS_PATH = OUTPUT_TABLE_DIR / "student_clusters.csv"
CLUSTER_SUMMARY_PATH = OUTPUT_TABLE_DIR / "cluster_summary.csv"
CLUSTER_PLOT_PATH = OUTPUT_FIGURE_DIR / "student_clusters_pca.png"

RANDOM_SEED = 17
N_CLUSTERS = 4


STUDENT_FEATURE_COLUMNS = [
    "student_total_attempts",
    "student_final_accuracy",
    "student_avg_elapsed_time",
    "student_avg_difficulty_score",
    "student_topic_diversity",
    "student_recent_accuracy",
    "student_accuracy_change",
]


def load_features(path: Path) -> pd.DataFrame:
    """Load feature dataset."""

    if not path.exists():
        raise FileNotFoundError(
            f"missing feature file: {path}. Run build_features.py first."
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    return dataframe


def calculate_recent_accuracy(student_df: pd.DataFrame, window_size: int = 5) -> float:
    """Calculate recent accuracy for one student."""

    recent_answers = student_df.sort_values('timestamp').tail(window_size)

    return float(recent_answers['is_coreect'].mean())


def calculate_accuracy_change(student_df: pd.DataFrame) -> float:
    """Calculate difference between early accuracy and recent accuracy."""

    student_df = student_df.sort_values('timestamp')

    first_answers = student_df.head(5)
    last_answers = student_df.tail(5)

    eary_accuracy = first_answers['is_correct'].mean()
    recent_accuracy = last_answers['is_correct'].mean()

    return float(recent_accuracy - eary_accuracy)


def build_student_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create student-level behavior features."""

    student_rows = []

    for student_id, student_df in dataframe.groupby('student_id'):
        student_rows.append(
            {
                "student_id": student_id,
                "student_total_attempts": len(student_df),
                "student_final_accuracy": student_df["is_correct"].mean(),
                "student_avg_elapsed_time": student_df["elapsed_time"].mean(),
                "student_avg_difficulty_score": student_df[
                    "difficulty_score"
                ].mean(),
                "student_topic_diversity": student_df["tags"].nunique(),
                "student_recent_accuracy": calculate_recent_accuracy(student_df),
                "student_accuracy_change": calculate_accuracy_change(student_df),
            }
        )

    return pd.DataFrame(student_rows)


def run_kmeans_clustering(student_features_df: pd.DataFrame) -> pd.DataFrame:
    """Run K-Means clustering on student behavior features."""

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        student_features_df[STUDENT_FEATURE_COLUMNS]
    )

    kmeans = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_SEED,
        n_init=10
    )
    # K-Means başlangıçta cluster merkezlerini rastgele seçer.
    # Kötü başlangıç seçerse kötü cluster sonucu çıkabilir.
    # n_init=10
    # demek:
    # K-Means’i 10 farklı rastgele başlangıçla dene, en iyi sonucu seç.
    # Yani daha güvenli sonuç verir.

    cluster_labels = kmeans.fit_predict(scaled_features)

    clustered_df = student_features_df.copy()
    clustered_df['cluster'] = cluster_labels

    score = silhouette_score(scaled_features, cluster_labels)
    # Öğrenciler kendi cluster’ına yakın mı, diğer cluster’lardan uzak mı?
    # +1'e yakın → çok iyi cluster
    # 0 civarı → clusterlar karışık
    # -1'e yakın → kötü cluster

    print(f"Silhouette score: {score:.3f}")

    return clustered_df


def create_cluster_summary(clustered_df: pd.DataFrame) -> pd.DataFrame:
    """Create a summary table for each cluster."""

    summary_df = (
        clustered_df.groupby('cluster')[STUDENT_FEATURE_COLUMNS]
        .mean()
        .round(3)
        .reset_index()
    )

    summary_df['student_count'] = (
        clustered_df.groupby('cluster')['student_id']
        .count()
        .values
    )

    return summary_df


def plot_clusters(clustered_df: pd.DataFrame) -> None:
    """Create a 2D PCA plot of student clusters."""
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(clustered_df[STUDENT_FEATURE_COLUMNS])

    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    pca_features = pca.fit_transform(scaled_features)

    plot_df = pd.DataFrame(
        {
            'pca_1': pca_features[:, 0],
            'pca_2': pca_features[:, 1],
            'cluster': clustered_df['cluster']
        }
    )

    plt.figure(figsize=(8, 6))

    for cluster_id in sorted(plot_df["cluster"].unique()):
        cluster_points = plot_df[plot_df["cluster"] == cluster_id]

        plt.scatter(
            cluster_points["pca_1"],
            cluster_points["pca_2"],
            label=f"Cluster {cluster_id}",
            alpha=0.8,
        )

    plt.title("Student Behavior Clusters")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(CLUSTER_PLOT_PATH, dpi=200)
    plt.close()


def main() -> None:
    """Run student behavior clustering."""

    OUTPUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = load_features(INPUT_PATH)

    student_features_df = build_student_features(dataframe)
    clustered_df = run_kmeans_clustering(student_features_df)
    summary_df = create_cluster_summary(clustered_df)

    clustered_df.to_csv(STUDENT_CLUSTERS_PATH, index=False)
    summary_df.to_csv(CLUSTER_SUMMARY_PATH, index=False)

    plot_clusters(clustered_df)

    print("Student clustering completed successfully.")
    print(f"Student clusters saved to: {STUDENT_CLUSTERS_PATH}")
    print(f"Cluster summary saved to: {CLUSTER_SUMMARY_PATH}")
    print(f"Cluster plot saved to: {CLUSTER_PLOT_PATH}")
    print("\nCluster summary:")
    print(summary_df)


if __name__ == "__main__":
    main()


# # ------------------------------------------------------------
# # NOTES
# # ------------------------------------------------------------

# # This file groups students based on learning behavior.

# # Main idea:
# # Students are not all the same.
# # Some students are accurate, some are slow, some improve, and some struggle.

# # Input:
# # 02_data/processed/demo_features.csv

# # Output:
# # student_clusters.csv
# # cluster_summary.csv
# # student_clusters_pca.png

# # Main features:
# # student_total_attempts:
# # How many questions the student answered.

# # student_final_accuracy:
# # Overall correctness rate.

# # student_avg_elapsed_time:
# # Average time spent on questions.

# # student_avg_difficulty_score:
# # Average difficulty of attempted questions.

# # student_topic_diversity:
# # How many different topics the student practiced.

# # student_recent_accuracy:
# # Accuracy on the last few questions.

# # student_accuracy_change:
# # Recent accuracy minus early accuracy.
# # Positive value means the student improved.

# # K-Means:
# # Groups similar students together.

# # PCA plot:
# # Converts many behavior features into 2D so we can visualize clusters.

# # Why this matters:
# # Clustering helps the tutor understand different learner types.
# # Later, recommendations and RL policies can be analyzed by student cluster.
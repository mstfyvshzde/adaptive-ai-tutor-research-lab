"""
Student behavior clustering for the Adaptive AI Tutor Research Lab.

Goal:
Group students based on their learning behavior.

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


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "02_data" / "processed" / "demo_features.csv"

OUTPUT_TABLE_DIR = PROJECT_ROOT / "06_results" / "tables"
OUTPUT_FIGURE_DIR = PROJECT_ROOT / "06_results" / "figures" / "clustering"

STUDENT_CLUSTERS_PATH = OUTPUT_TABLE_DIR / "student_clusters.csv"
CLUSTER_SUMMARY_PATH = OUTPUT_TABLE_DIR / "cluster_summary.csv"
CLUSTER_PLOT_PATH = OUTPUT_FIGURE_DIR / "student_clusters_pca.png"

RANDOM_SEED = 17

# N_CLUSTERS = 4, K-Means gibi kümeleme (clustering) algoritmalarında, verilerin toplam kaç farklı gruba/kümeye ayrılacağını belirler.
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
    if not path.exists():
        raise FileNotFoundError(
            f"missing feature file: {path}. run build_features.py first."
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])
    # Kod içindeki pd.to_datetime(dataframe['timestamp']) satırı ise, bu tarih bilgisini düz bir metin (yazı) olmaktan çıkarıp bilgisayarın kronolojik sıralama ve zaman analizi yapabileceği gerçek bir tarih/saat formatına dönüştürür.
    # Bu sayede sistem, öğrencilerin geçmişten geleceğe doğru hangi sırayla soru çözdüğünü hatasız şekilde takip edebilir.

    return dataframe


# 1. calculate_recent_accuracy
# Ne Yapar? Bir öğrencinin test çözerken gösterdiği son durumdaki başarısını ölçer.
# Detay: Öğrencinin kronolojik olarak çözdüğü son 5 soruyu alır ve bunların başarı ortalamasını hesaplar.
def calculate_recent_accuracy(student_df: pd.DataFrame, window_size: int = 5) -> float:
    recent_answers = student_df.sort_values('timestamp').tail(window_size)

    return float(recent_answers['is_correct'].mean())


# 2. calculate_accuracy_change
# Ne Yapar? Öğrencinin süreç içindeki gelişim/ilerleme hızını hesaplar.
# Detay: Öğrencinin ilk çözdüğü 5 soru ile son çözdüğü 5 soru arasındaki başarı farkını bulur (Son başarı - İlk başarı). Sonuç pozitifse öğrenci kendini geliştirmiş demektir.
def calculate_accuracy_change(student_df: pd.DataFrame) -> float:
    student_df = student_df.sort_values('timestamp')

    first_answers = student_df.head(5)
    last_answers = student_df.tail(5)

    early_accuracy = first_answers['is_correct'].mean()
    recent_accuracy = last_answers['is_correct'].mean()

    return float(recent_accuracy - early_accuracy)



# 3. build_student_features
# Ne Yapar? Ham etkileşim verilerini, öğrenci bazlı özet davranış raporlarına dönüştürür.
# Detay: Veriyi öğrenci öğrenci gruplar; her öğrencinin toplam soru sayısını, genel başarısını, hızını, çözdüğü konuların çeşitliliğini ve üstteki iki fonksiyonu kullanarak gelişim metriklerini tek bir satıra indirger.
def build_student_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    student_rows = []

    for student_id, student_df in dataframe.groupby('student_id'):
        student_rows.append(
            {
                'student_id': student_id,
                'student_total_attempts': len(student_df),
                'student_final_accuracy': student_df['is_correct'].mean(), 
                "student_avg_elapsed_time": student_df["elapsed_time"].mean(),
                "student_avg_difficulty_score": student_df["difficulty_score"].mean(),
                "student_topic_diversity": student_df["tags"].nunique(),
                "student_recent_accuracy": calculate_recent_accuracy(student_df),
                "student_accuracy_change": calculate_accuracy_change(student_df),
            }
        )

    return pd.DataFrame(student_rows)


# 4. run_kmeans_clustering
# Ne Yapar? Öğrencileri davranış benzerliklerine göre yapay zekayla gruplara ayırır.
# Detay: Önce tüm verileri StandardScaler ile eşit ölçeğe getirir, ardından KMeans algoritmasıyla öğrencileri belirlenen küme sayısına (4 gruba) böler ve silhouette_score ile bu bölme işleminin ne kadar kaliteli olduğunu ölçer.
def run_kmeans_clustering(student_features_df: pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        student_features_df[STUDENT_FEATURE_COLUMNS]
    )

    kmeans = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_SEED,
        n_init=10,
    )
    # K-Means algoritması ilk başlarken küme merkezlerini rastgele seçer ve bazen kötü bir başlangıç noktası yüzünden yanlış gruplama yapabilir. n_init=10 parametresi, algoritmanın 10 kez birbirinden bağımsız ve farklı rastgele noktalarla baştan başlayarak gruplama yapmasını söyler. Algoritma bu 10 deneme içinden en başarılı ve en kararlı olan sonucu seçer.

    cluster_labels = kmeans.fit_predict(scaled_features)

    clustered_df = student_features_df.copy()
    clustered_df["cluster"] = cluster_labels

    score = silhouette_score(scaled_features, cluster_labels)
    # Bu skor, yapay zekanın yaptığı kümeleme/gruplama işleminin ne kadar kaliteli ve doğru olduğunu ölçen bir başarı metriğidir.
    # Mantığı: Oluşturulan grupların kendi içinde ne kadar sıkı (birbirine yakın) ve diğer gruplardan ne kadar uzak (net ayrılmış) olduğunu kontrol eder.

    print(f"Silhouette score: {score:.3f}")

    return clustered_df


# 5. create_cluster_summary
# Ne Yapar? Oluşan öğrenci gruplarının karakteristik özelliklerini (profilini) çıkarır.
# Detay: Oluşan 4 kümenin her birinin ortalama hızını, başarısını ve o kümede kaç öğrenci olduğunu gösteren bir özet tablo hazırlar. (Örn: "2. Küme: Çok hızlı çözen ama başarısı düşük olanlar").
def create_cluster_summary(clustered_df: pd.DataFrame) -> pd.DataFrame:
    summary_df = (
        clustered_df.groupby("cluster")[STUDENT_FEATURE_COLUMNS]
        .mean()
        .round(3)
        .reset_index()
    )

    summary_df["student_count"] = (
        clustered_df.groupby("cluster")["student_id"]
        .count()
        .values
    )

    return summary_df


# 6. plot_clusters
# Ne Yapar? Öğrenci gruplarını bizim görebileceğimiz şekilde grafiğe döker.
# Detay: Elimizdeki çok sayıda özelliği (7 adet) grafik üzerinde gösterebilmek için PCA algoritmasıyla 2 boyuta indirger ve her öğrenci kümesini farklı bir renkle ekrana çizip bilgisayara kaydeder.
def plot_clusters(clustered_df: pd.DataFrame) -> None:
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(clustered_df[STUDENT_FEATURE_COLUMNS])

    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    pca_features = pca.fit_transform(scaled_features)

    plot_df = pd.DataFrame(
        {
            "pca_1": pca_features[:, 0],
            "pca_2": pca_features[:, 1],
            "cluster": clustered_df["cluster"],
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


# 7. main
# Ne Yapar? Tüm bu kümeleme ve analiz sürecini baştan sona yöneten ana şeftir.
# Detay: Klasörleri kontrol eder, veriyi yükler, öğrencilerin özelliklerini çıkartıp gruplama yapar ve sonuç raporları ile grafikleri ilgili klasörlere kaydeder.
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
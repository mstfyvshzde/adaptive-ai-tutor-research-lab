"""
Train supervised baseline models for knowledge tracing.

Goal:
Predict whether a student will answer a question correctly.

Input:
02_data/processed/demo_features.csv

Output:
06_results/tables/supervised_baseline_metrics.csv
"""


from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import  (
    accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "02_data" / "processed" / "demo_features.csv"
OUTPUT_DIR = PROJECT_ROOT / "06_results" / "tables"
OUTPUT_PATH = OUTPUT_DIR / "supervised_baseline_metrics.csv"

RANDOM_SEED = 17
TEST_SIZE = 0.20


NUMERIC_FEATURES = [
    "difficulty_score",
    "elapsed_time",
    "student_attempt_count",
    "student_accuracy_so_far",
    "previous_correct",
    "previous_elapsed_time",
    "rolling_accuracy_5",
    "rolling_accuracy_10",
    "time_since_previous_seconds",
    "topic_attempt_count_so_far",
    "topic_accuracy_so_far",
    "question_attempt_count_so_far",
    "question_accuracy_so_far",
    "question_difficulty_estimate",
]

CATEGORICAL_FEATURES = [
    "part",
    "tags",
    "difficulty",
]

TARGET_COLUMN = "is_correct"


def load_features(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"missing feature file: {path}. run build_features.py first."
        )
    
    dataframe = pd.read_csv(path)
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    return dataframe


def create_time_based_split(
    dataframe: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    dataframe = dataframe.sort_values('timestamp').reset_index(drop=True)

    split_index = int(len(dataframe) * (1 - TEST_SIZE))

    train_df = dataframe.iloc[:split_index]
    test_df = dataframe.iloc[split_index:]

    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    X_train = train_df[feature_columns]
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df[feature_columns]
    y_test = test_df[TARGET_COLUMN]

    return X_train, X_test, y_train, y_test


def build_preprocessor() -> ColumnTransformer:
    try:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    except TypeError:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # Buradaki sparse (veya yeni adıyla sparse_output), One-Hot Encoder'ın dönüştürme işlemi sonucunda ürettiği matrisin formatını belirler:
        # False yapıldığında, veri setini sıkıştırılmış ve okunması zor özel bir matris formatı yerine, üzerinde rahatça işlem yapabileceğiniz standart, açık ve okunabilir bir NumPy dizisi (array) olarak döndürür.

    preprocessor = ColumnTransformer(
        transformers = [
            ('numeric', StandardScaler(), NUMERIC_FEATURES),
            ('categorical', encoder, CATEGORICAL_FEATURES)
        ]
    )
    # ColumnTransformer, veri setindeki farklı türdeki sütunları ayırarak her birine kendi yapısına uygun ön işleme adımını aynı anda uygulayan bir dönüştürücüdür.
    # Bu kodda, sayısal sütunları StandardScaler ile standart bir ölçeğe getirirken, kategorik (metinsel) sütunları OneHotEncoder ile modelin anlayabileceği 0 ve 1'lere dönüştürür ve hepsini tek bir temiz tabloda birleştirir.

    return preprocessor



def build_models() -> dict[str, object]:
    return {
        'dumpy_majority': DummyClassifier(strategy='most_frequent'),
        # Nedir? Hiçbir kalıp öğrenmeyen, sadece veri setindeki en çok tekrarlayan sonuca (örneğin herkes soruyu doğru bildiyse herkese "doğru" cevabı verir) göre körü körüne tahmin yapan en temel modeldir.
        # Amacı: Diğer gelişmiş modellerin başarısını ölçmek için bir taban çizgisi (baseline) oluşturur; gerçek modellerin en azından bundan daha iyi performans göstermesi beklenir.

        'logistic_regression': LogisticRegression(max_iter=1000),
        # Nedir? Veriler arasındaki doğrusal ilişkileri kullanarak bir durumun gerçekleşme olasılığını (örneğin soruyu doğru bilme/bilememe) hesaplayan klasik ve hızlı bir istatistiksel modeldir.
        # max_iter=1000: Modelin en doğru sonuçları bulabilmek için veriyi en fazla 1000 kez tarayarak optimizasyon (çözüm arama) yapmasına izin verir.
        
        'random_forest': RandomForestClassifier(
            n_estimators=150, 
            random_state=RANDOM_SEED
        ),
        # Nedir? Veriyi analiz ederken birbirinden bağımsız yüzlerce karar ağacı (decision tree) oluşturan ve her ağacın verdiği tahminlerin çoğunluk oyuna göre nihai kararı veren güçlü bir topluluk (ensemble) modelidir.
        # n_estimators=150: Arka planda tam 150 adet farklı karar ağacı dikileceğini ve eğitileceğini belirtir.
        # random_state=RANDOM_SEED: Model her çalıştırıldığında ağaçların hep aynı rastgele mantıkla kurulmasını ve sonuçların tutarlı kalmasını sağlar.

        'gradient_boosting': GradientBoostingClassifier(
            random_state=RANDOM_SEED
        )
        # Nedir? Tıpkı Random Forest gibi karar ağaçlarını kullanır; ancak ağaçları bağımsız kurmak yerine, sırayla kurarak her yeni ağacın bir önceki ağacın yaptığı hataları ve eksikleri düzeltmesini sağlayan çok yüksek başarı oranına sahip bir algoritmadır.
        # random_state=RANDOM_SEED: Rastgelelik içeren adımların her çalıştırmada birebir aynı şekilde tekrarlanmasını garantiler.
    }



# ROC AUC, bir sınıflandırma modelinin (örneğin, bir öğrencinin soruyu doğru mu yoksa yanlış mı bileceğini tahmin eden sistemin) iki sınıfı birbirinden ayırt etme gücünü ölçen en popüler başarı metriğidir.
# Bu fonksiyon, modelin tahmin başarısını ölçen ROC AUC skorunu kodun çökmesini engelleyerek güvenli bir şekilde hesaplar. Eğer test verisinde hem 0 hem 1 sınıfı (yani hem doğru hem yanlış cevap) yoksa fonksiyon hata fırlatmak yerine güvenli bir şekilde NaN (belirsiz) değerini döndürür; aksi takdirde normal başarı skorunu hesaplar.
def safe_roc_auc(y_true: pd.Series, y_probability: np.ndarray) -> float:
    if y_true.nunique() < 2: # Bu kod satırı, test verisindeki gerçek cevapların (0 ve 1'lerin) içinde en az iki farklı sınıfın bulunup bulunmadığını kontrol eder.
        return float('nan')
    
    return float(roc_auc_score(y_true, y_probability))



# Bu fonksiyon, modelin tahmin hatalarını cezalandıran Log Loss (Lojistik Kayıp) skorunu, matematiksel hataları engellemek için güvenli bir şekilde hesaplar.
def safe_log_loss(y_true: pd.Series, y_probability: np.ndarray) -> float:
    y_probability = np.clip(y_probability, 0.01, 0.999)
    # np.clip(y_probability, 0.01, 0.999): Modelin verdiği olasılık tahminlerini 0.01 ile 0.999 arasına sıkıştırır. Eğer bir model bir cevaba kesinlikle %100 emin şekilde 0 veya 1 derse ve yanılırsa, Log Loss formülündeki logaritma hesabı yüzünden sonuç sonsuz (∞) çıkar ve kod çöker. Bu satır o uç değerleri tıraşlayarak çökme riskini önler.

    return float(log_loss(y_true, y_probability, labels=[0, 1]))
    # log_loss(..., labels=[0, 1]): Sıkıştırılmış bu güvenli olasılıklar ile gerçek sonuçları (y_true) karşılaştırarak gerçek Log Loss değerini hesaplar. labels=[0, 1] parametresi ise, o anki test verisinde sadece 0 veya sadece 1 denk gelse bile fonksiyonun şaşırmayıp iki sınıfı da tanımasını sağlar.



def evaluate_model(
    model_name: str,
    model: object,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    y_train: pd.Series
) -> dict:
    pipeline = Pipeline(
        steps=[
            ('preprocessor', build_preprocessor()),
            ('model', model)
        ]
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    bak

#     if hasattr(pipeline, "predict_proba"):
#         y_probability = pipeline.predict_proba(x_test)[:, 1]
#     else:
#         y_probability = y_pred

#     return {
#         "model": model_name,
#         "accuracy": accuracy_score(y_test, y_pred),
#         "precision": precision_score(y_test, y_pred, zero_division=0),
#         "recall": recall_score(y_test, y_pred, zero_division=0),
#         "f1": f1_score(y_test, y_pred, zero_division=0),
#         "roc_auc": safe_roc_auc(y_test, y_probability),
#         "log_loss": safe_log_loss(y_test, y_probability),
#     }


# def main() -> None:
#     """Train and evaluate all supervised baselines."""

#     OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#     dataframe = load_features(INPUT_PATH)

#     x_train, x_test, y_train, y_test = create_time_based_split(dataframe)

#     models = build_models()

#     result_rows = []

#     for model_name, model in models.items():
#         print(f"Training model: {model_name}")

#         result = evaluate_model(
#             model_name=model_name,
#             model=model,
#             x_train=x_train,
#             x_test=x_test,
#             y_train=y_train,
#             y_test=y_test,
#         )

#         result_rows.append(result)

#     results_df = pd.DataFrame(result_rows).round(4)
#     results_df.to_csv(OUTPUT_PATH, index=False)

#     print("Supervised baselines completed successfully.")
#     print(f"Saved to: {OUTPUT_PATH}")
#     print("\nResults:")
#     print(results_df)


# if __name__ == "__main__":
#     main()
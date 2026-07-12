"""
Train supervised baseline models on the EdNet V2 feature dataset.

Input:
- 02_data/processed/ednet/ednet_features.csv

Output:
- 06_results/tables/ednet/ednet_supervised_metrics.csv

Task:
Predict whether a student will answer a question correctly.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
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
CONFIG_PATH = PROJECT_ROOT / "05_experiments" / "configs" / "ednet_config.yaml"


NUMERIC_FEATURES = [
    "elapsed_time",
    "time_since_previous_seconds",
    "student_attempt_count",
    "student_accuracy_so_far",
    "previous_correct",
    "previous_elapsed_time",
    "rolling_accuracy_5",
    "rolling_accuracy_10",
    "topic_attempt_count_so_far",
    "topic_accuracy_so_far",
    "question_attempt_count_so_far",
    "question_accuracy_so_far",
    "question_difficulty_estimate",
]


CATEGORICAL_FEATURES = [
    "part",
    "primary_tag",
]


TARGET_COLUMN = "is_correct"


# 2. load_config()
# ednet_config.yaml dosyasını okur. Kodun içine dosya yollarını veya test oranlarını (test_size) elle yazmak yerine, projenin merkezi ayarlarını bu fonksiyonla bir sözlük (dict) olarak içeri alır.
def load_config() -> dict:
    with CONFIG_PATH.open('r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    


# 3. load_features(config)
# Eğitimde kullanılacak olan ednet_features.csv dosyasını yükler. Yüklerken iki önemli kontrol yapar:
# Dosya gerçekten var mı? (Yoksa hata fırlatır).
# Modelin ihtiyaç duyduğu tüm sayısal ve kategorik sütunlar bu dosyada mevcut mu? (Eksik varsa uyarır).
def load_features(config: dict) -> pd.DataFrame:
    feature_path = PROJECT_ROOT / config["outputs"]["feature_dataset"]

    if not feature_path.exists():
        raise FileNotFoundError(
            f"EdNet feature dataset not found: {feature_path}\n"
            "run build_ednet_features.py first"
        )
    
    df = pd.read_csv(feature_path)

    required_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN, 'timestamp']
    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"missing required columns: {missing}")

    return df



# 4. time_based_split(df, test_size)
# Veriyi zamana göre tren (train) ve test seti olarak ikiye böler. Öğrenci verilerinde geleceği tahmin etmek istediğimiz için veriyi rastgele değil, timestamp sütununa göre kronolojik sıralayıp böler. Örneğin test_size 0.2 ise, verinin ilk %80'ini eğitime, son %20'sini teste ayırır.
def time_based_split(df: pd.DataFrame, test_size: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df['timestamp_sort'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df = df.sort_values(by='timestamp_sort').reset_index(drop=True)

    split_index = int(len(df) * (1 - test_size))

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    return train_df, test_df




# 5. build_preprocessor()
# Veriyi modele sokmadan önce temizleyen ve hazırlayan bir dönüştürücü (ColumnTransformer) oluşturur:
# Sayısal özellikleri (StandardScaler ile) standartlaştırır (ortalamayı 0, standart sapmayı 1 yapar).
# Kategorik özellikleri (OneHotEncoder ile) bilgisayarların anlayacağı 0 ve 1'lerden oluşan matrislere dönüştürür.
def buil_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ('numeric', StandardScaler(), NUMERIC_FEATURES),
            (
                'categorical',
                OneHotEncoder(handle_unknown='ignore'),
                CATEGORICAL_FEATURES
            )
        ]
    )




# 6. build_models()
# Performanslarını birbiriyle kıyaslayacağın 4 farklı algoritmayı hazırlar:
# DummyClassifier: Her şeye en çok tekrar eden sınıfı (örn: hep "doğru") tahmin eden, başarı kıstası (baseline) oluşturmak için kullanılan en basit model.
# LogisticRegression: Hızlı ve doğrusal bir sınıflandırıcı.
# RandomForestClassifier & GradientBoostingClassifier: Ağaç tabanlı, daha karmaşık ve genellikle daha yüksek başarı veren güçlü modeller.
def build_models() -> dict[str, object]:
    return {
        'dummy_majority': DummyClassifier(strategy='most_frequent'),
        'logistic_regression': LogisticRegression(max_iter=1000),
        'random_forest': RandomForestClassifier(
            n_estimators=150,
            random_state=17,
            n_jobs=-1
        ),
        'gradient_boosting': GradientBoostingClassifier(random_state=17)
    }





# 7. evaluate_model(model_name, pipeline, X_test, y_test)
# Eğitilen modelin hiç görmediği test verisi (X_test) üzerindeki başarısını ölçer. Sadece doğruluğa (accuracy) değil; dengesiz veri setlerinde çok önemli olan F1-skoru, Hassasiyet (Precision), Duyarlılık (Recall), ROC-AUC ve Log-Loss gibi gelişmiş metrikleri hesaplayıp bir sözlük olarak döner.
def evaluate_model(
    model_name: str,
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> dict:
    predictions = pipeline.predict(X_test)

    if hasattr(pipeline, 'predict_proba'):
        probabilities = pipeline.predict_proba(X_test)[:, 1]
    else:
        probabilities = predictions

    metrics = {
        'model': model_name,

        # 1. Accuracy (Doğruluk)
        # Neyi ölçer: Genel başarıyı. Modelin (doğru veya yanlış fark etmeksizin) yaptığı tüm tahminlerin yüzde kaçının doğru olduğunu gösterir.
        # Örnek: Model 100 sorudan toplam 80 tanesini (ister doğru desin ister yanlış) tam isabet bildiyse, Accuracy = %80 (0.80) olur.
        'accuracy': round(accuracy_score(y_test, predictions), 4),

        #2. Precision (Kesinlik / Hassasiyet)
        # Neyi ölçer: Modelin "Doğru yapacak" dediği tahminlerin kalitesini.
        # Örnek: Modelimiz 60 soru için "Bu öğrenci kesin Doğru cevaplar" dedi. Gidip baktık, bu 60 sorudan sadece 45'ini öğrenciler gerçekten doğru bilmiş. Bu durumda modelin nokta atışı başarısı Precision = 45/60 = %75 (0.75) olur.
        'precision': round(
            precision_score(y_test, predictions, zero_division=0),
            4
        ),

        # 3. Recall (Duyarlılık / Yakalama Oranı) 
        # Neyi ölçer: Gerçekte doğru olan yanıtların yüzde kaçını modelin fark edip yakalayabildiğini.
        # Örnek: Sınıfta öğrencilerin gerçekten doğru bildiği toplam 70 soru vardı. Modelimiz bu 70 sorudan ancak 42 tanesini "Doğru cevaplanır" diye önceden sezebildi. Bu durumda model gerçeğin ne kadarını yakalamış? Recall = 42/70 = %60 (0.60).
        'recall': round(
            recall_score(y_test, predictions, zero_division=0),
            4
        ),

        # 4. F1-Score
        # Neyi ölçer: Precision ve Recall değerlerinin dengeli bir ortalamasını. Eğer verilerinde doğru/yanlış sayısı çok dengesizse (örneğin herkes hep doğru cevaplıyorsa) sadece Accuracy'ye bakmak yanıltır; F1-Score modelin gerçek kalitesini gösterir. 1'e yakın olması mükemmel denge demektir. 
        # Örnek: Yukarıdaki örnekte Precision %75, Recall %60 çıkmıştı. İkisinin harmonik ortalaması alınır ve F1-Score = %66.6 (0.666) olarak iki metriğin ortak performansını özetler.
        'f1': round(
            f1_score(y_test, predictions, zero_division=0),
            4
        )
    }

    # 5. ROC-AUC 
    # Neyi ölçer: Modelin "doğru cevaplanacak soru" ile "yanlış cevaplanacak soru"yu birbirinden ayırt etme yeteneğini. Olasılık skorlarına bakar. 0.5 çıkarsa yazı tura atmak gibidir, 1.0 çıkarsa kusursuz ayırt ediyordur.
    # Örnek: Model, gerçekten doğru cevaplanan bir soruya %90 ihtimalle doğru derken, yanlış cevaplanan bir soruya %10 ihtimalle doğru diyorsa ayırt etme gücü çok yüksektir ve ROC-AUC 0.90'a yakın çıkar.
    try:
        metrics['roc_auc'] = round(roc_auc_score(y_test, probabilities), 4)
    except ValueError:
        metrics['roc_auc'] = None


    # 6. Log-Loss (Logaritmik Kayıp)
    # Neyi ölçer: Modelin tahminlerindeki özgüven hatasını. Model sadece 1 veya 0 demez, olasılık verir. Eğer model %99 ihtimalle "Doğru" dediği bir soruda çuvallarsa, Log-Loss cezası çok büyür. Bu skorda hedef sıfıra (0) olabildiğince yakın olmaktır.
    # Örnek: Model bir soruya %51 ihtimalle "Doğru" deyip yanılırsa az ceza alır. Ama %99 emin olup yanılırsa çok ağır ceza alır ve Log-Loss skoru yükselir (kötüleşir).
    try:
        metrics['log_loss'] = round(log_loss(y_test, probabilities), 4)
    except ValueError:
        metrics['log_loss'] = None

    return metrics



# 8. train_and_evaluate(df, config)
# Tüm modelleri döngüye sokarak sırayla eğiten ana mutfaktır:
# Veriyi böler.
# Her model için build_preprocessor ve modeli birleştiren bir Pipeline kurar.
# pipeline.fit() ile modeli eğitir.
# evaluate_model ile performansını ölçer ve tüm modellerin sonuçlarını bir tabloda (DataFrame) toplar.
def train_and_evaluate(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    test_size = float(config['task']['test_size'])

    train_df, test_df = time_based_split(df, test_size)

    X_train = train_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_test = test_df[TARGET_COLUMN]

    print("EdNet supervised baseline training")
    print(f"Train rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")
    print(f"Train correctness: {y_train.mean():.4f}")
    print(f"Test correctness: {y_test.mean():.4f}")

    results = []

    for model_name, model in build_models().items():
        pipeline = Pipeline(
            steps=[
                ('preprocessor', buil_preprocessor()),
                ('model', model)
            ]
        )

        pipeline.fit(X_train, y_train)

        metrics = evaluate_model(
            model_name=model_name,
            pipeline=pipeline,
            X_test=X_test,
            y_test=y_test
        )

        results.append(metrics)

        print(
            f"{model_name}: "
            f"accuracy={metrics['accuracy']}, "
            f"f1={metrics['f1']}, "
            f"roc_auc={metrics['roc_auc']}"
        )

    return pd.DataFrame(results)


# 9. save_metrics(metrics_df, config)
# Elde edilen başarı sonuçlarını ekrana şık bir tablo olarak bastırır ve gelecekte raporlarda kullanabilmen için 06_results/tables/ednet/ednet_supervised_metrics.csv yoluna kalıcı olarak kaydeder
def save_metrics(metrics_df: pd.DataFrame, config: dict) -> None:
    output_path = PROJECT_ROOT / config["outputs"]["supervised_metrics"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(output_path, index=False)

    print(f"\nMetrics saved to: {output_path}")
    print(metrics_df.to_string(index=False))



# 1. main() (Ana Yönetici)
# Her şeyin başladığı yerdir. Diğer tüm fonksiyonları doğru sırayla çağırarak tüm süreci baştan sona yönetir:
# Konfigürasyonu yükler.
# Özellik (feature) veri setini okur.
# Modelleri eğitip test eder.
# Sonuçları bir CSV dosyasına kaydeder.
def main() -> None:
    config = load_config()
    df = load_features(config)

    metrics_df = train_and_evaluate(df, config)
    save_metrics(metrics_df, config)


if __name__ == "__main__":
    main()



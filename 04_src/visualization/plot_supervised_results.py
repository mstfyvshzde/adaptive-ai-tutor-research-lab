"""
Plot supervised baseline results.

Goal:
Visualize model comparison for knowledge tracing.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "06_results" / "tables" / "supervised_baseline_metrics.csv"
OUTPUT_DIR = PROJECT_ROOT / "06_results" / "figures" / "supervised"

ROC_AUC_PLOT = OUTPUT_DIR / "supervised_roc_auc_comparison.png"
LOG_LOSS_PLOT = OUTPUT_DIR / "supervised_log_loss_comparison.png"


def load_results(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}. Run supervised_baselines.py first."
        )

    return pd.read_csv(path)

# ROC-AUC (Ayırt Etme Gücü): Modelin, doğru cevap verecek öğrenci ile yanlış cevap verecek öğrenciyi birbirinden ayırt etme yeteneğidir. Puanı 0 ile 1 arasındadır. 1'e ne kadar yakınsa model o kadar mükemmeldir; yani kimin yapıp kimin yapamayacağını çok iyi seziyor demektir. (Bu grafikte sütunun UZUN olması istenir).
# plot_roc_auc: Modellerin ROC-AUC puanlarını karşılaştıran bir grafik oluşturur. ROC-AUC, modellerin "doğru ve yanlış cevapları birbirinden ayırt etme" yeteneğini ölçer; yani bu grafikte sütunun daha yüksek olması modelin daha başarılı olduğunu gösterir.
def plot_roc_auc(results_df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(results_df["model"], results_df["roc_auc"])
    plt.title("Supervised Model Comparison — ROC-AUC")
    plt.xlabel("Model")
    plt.ylabel("ROC-AUC")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(ROC_AUC_PLOT, dpi=200)
    plt.close()


# Log Loss (Tahmin Hatası): Modelin yaptığı tahminlerde ne kadar yanıldığı ve kendine ne kadar gereksiz güvendiğidir. Örneğin model bir öğrenciye "%99 kesinlikle doğru yapacak" deyip öğrenci çuvallarsa, Log Loss cezası çok büyük olur. Değeri 0'a ne kadar yakınsa model o kadar az hata yapıyor demektir. (Bu grafikte sütunun KISA olması istenir).
# plot_log_loss: Modellerin Log Loss (Hata Oranı / Lojistik Kayıp) değerlerini kıyaslar. Log Loss, modelin yaptığı tahminlerin olasılık bazında ne kadar hatalı olduğunu ölçer; yani bu grafikte sütunun daha alçak/düşük olması modelin daha az hata yaptığını ve daha başarılı olduğunu gösterir.
def plot_log_loss(results_df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(results_df["model"], results_df["log_loss"])
    plt.title("Supervised Model Comparison — Log Loss")
    plt.xlabel("Model")
    plt.ylabel("Log Loss")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(LOG_LOSS_PLOT, dpi=200)
    plt.close()


# main: Kayıt klasörünü (figures/supervised) hazırlar, modellerin başarı metriklerini içeren .csv dosyasını yükler, her iki grafik fonksiyonunu da çalıştırarak bunları .png formatında birer resim dosyası olarak kaydeder.
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results_df = load_results(INPUT_PATH)

    plot_roc_auc(results_df)
    plot_log_loss(results_df)

    print("Supervised result plots created successfully.")
    print(f"ROC-AUC plot saved to: {ROC_AUC_PLOT}")
    print(f"Log Loss plot saved to: {LOG_LOSS_PLOT}")


if __name__ == "__main__":
    main()
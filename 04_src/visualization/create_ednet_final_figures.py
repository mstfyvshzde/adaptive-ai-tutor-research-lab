from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

FINAL_COMPARISON_PATH = ROOT / "06_results/tables/ednet/final_v1_v2_comparison.csv"
ABLATION_PATH = ROOT / "06_results/tables/ednet/ednet_feature_ablation_500k.csv"
FEATURE_IMPORTANCE_PATH = ROOT / "06_results/tables/ednet/ednet_feature_importance.csv"
ERROR_ANALYSIS_PATH = ROOT / "06_results/tables/ednet/ednet_error_analysis.csv"

OUTPUT_DIR = ROOT / "06_results/figures/ednet"


def save_figure(filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / filename

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def plot_pipeline_diagram():
    steps = [
        "Raw EdNet\nKT1 Data",
        "Validation\n& Subset",
        "Leakage-Aware\nFeatures",
        "Supervised\nModels",
        "Evaluation\nMetrics",
        "Ablation\n& Analysis",
        "Research\nReport",
    ]

    fig, ax = plt.subplots(figsize=(14, 3))
    ax.axis("off")

    x_positions = range(len(steps))

    for i, step in enumerate(steps):
        ax.text(
            i,
            0.5,
            step,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.45", linewidth=1.2),
        )

        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(i + 0.72, 0.5),
                xytext=(i + 0.28, 0.5),
                arrowprops=dict(arrowstyle="->", linewidth=1.4),
            )

    ax.set_xlim(-0.6, len(steps) - 0.4)
    ax.set_ylim(0, 1)

    plt.title("Adaptive AI Tutor V2 Research Pipeline", fontsize=14, weight="bold")
    save_figure("pipeline_diagram.png")


def plot_roc_auc_by_scale():
    df = pd.read_csv(FINAL_COMPARISON_PATH)

    ednet_df = df[df["stage"].str.startswith("EdNet")].copy()

    ednet_df["scale"] = ednet_df["stage"].str.replace("EdNet ", "", regex=False)
    ednet_df["scale"] = ednet_df["scale"].str.replace(" Final", "", regex=False)

    plt.figure(figsize=(8, 5))
    plt.plot(ednet_df["scale"], ednet_df["roc_auc"], marker="o", linewidth=2)

    for _, row in ednet_df.iterrows():
        plt.text(
            row["scale"],
            row["roc_auc"] + 0.004,
            f"{row['roc_auc']:.4f}",
            ha="center",
            fontsize=9,
        )

    plt.title("ROC-AUC by EdNet Dataset Scale", fontsize=14, weight="bold")
    plt.xlabel("Dataset scale")
    plt.ylabel("ROC-AUC")
    plt.ylim(0.58, 0.76)
    plt.grid(True, alpha=0.3)

    save_figure("roc_auc_by_scale.png")


def plot_feature_ablation():
    df = pd.read_csv(ABLATION_PATH)

    labels = df["feature_set"].str.replace("_", " ").str.title()

    plt.figure(figsize=(7, 5))
    plt.bar(labels, df["roc_auc"])

    for i, value in enumerate(df["roc_auc"]):
        plt.text(i, value + 0.002, f"{value:.4f}", ha="center", fontsize=9)

    plt.title("Baseline vs Enhanced Feature Set", fontsize=14, weight="bold")
    plt.xlabel("Feature set")
    plt.ylabel("ROC-AUC")
    plt.ylim(0.70, 0.75)
    plt.grid(axis="y", alpha=0.3)

    save_figure("feature_ablation.png")


def plot_top_feature_importance(top_n=10):
    df = pd.read_csv(FEATURE_IMPORTANCE_PATH)
    top_df = df.sort_values("importance", ascending=False).head(top_n).copy()
    top_df = top_df.sort_values("importance", ascending=True)

    plt.figure(figsize=(9, 6))
    plt.barh(top_df["feature"], top_df["importance"])

    plt.title("Top Feature Importance Signals", fontsize=14, weight="bold")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.grid(axis="x", alpha=0.3)

    save_figure("top_feature_importance.png")


def plot_error_group(analysis_type, filename, title, order=None):
    df = pd.read_csv(ERROR_ANALYSIS_PATH)
    group_df = df[df["analysis_type"] == analysis_type].copy()

    if order is not None:
        group_df["group"] = pd.Categorical(group_df["group"], categories=order, ordered=True)
        group_df = group_df.sort_values("group")
    else:
        group_df = group_df.sort_values("error_rate", ascending=False)

    group_df["error_rate_percent"] = group_df["error_rate"] * 100

    plt.figure(figsize=(8, 5))
    plt.bar(group_df["group"].astype(str), group_df["error_rate_percent"])

    for i, value in enumerate(group_df["error_rate_percent"]):
        plt.text(i, value + 0.7, f"{value:.1f}%", ha="center", fontsize=9)

    plt.title(title, fontsize=14, weight="bold")
    plt.xlabel("Group")
    plt.ylabel("Error rate (%)")
    plt.ylim(0, max(group_df["error_rate_percent"]) + 8)
    plt.grid(axis="y", alpha=0.3)

    save_figure(filename)


def main():
    required_files = [
        FINAL_COMPARISON_PATH,
        ABLATION_PATH,
        FEATURE_IMPORTANCE_PATH,
        ERROR_ANALYSIS_PATH,
    ]

    missing_files = [path for path in required_files if not path.exists()]

    if missing_files:
        missing_text = "\n".join(str(path) for path in missing_files)
        raise FileNotFoundError(f"Missing required input files:\n{missing_text}")

    plot_pipeline_diagram()
    plot_roc_auc_by_scale()
    plot_feature_ablation()
    plot_top_feature_importance(top_n=10)

    plot_error_group(
        analysis_type="by_model_confidence",
        filename="error_by_confidence.png",
        title="Error Rate by Model Confidence",
        order=["low", "medium", "high", "very_high"],
    )

    plot_error_group(
        analysis_type="by_student_history",
        filename="error_by_student_history.png",
        title="Error Rate by Student History",
        order=["0-4", "5-19", "20-49", "50-99", "100+"],
    )

    plot_error_group(
        analysis_type="by_question_difficulty",
        filename="error_by_difficulty.png",
        title="Error Rate by Question Difficulty",
        order=["easy", "medium", "hard", "very_hard"],
    )

    print("\nAll EdNet V2 final figures created successfully.")


if __name__ == "__main__":
    main()


from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_features.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "gradient_boosting_tuned.joblib"
)

REPORT_DIR = PROJECT_ROOT / "reports"
IMPORTANCE_DIR = REPORT_DIR / "feature_importance"

IMPORTANCE_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = IMPORTANCE_DIR / "permutation_importance.csv"
PLOT_PATH = IMPORTANCE_DIR / "global_feature_importance.png"

TARGET = "Churn"

RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    return X, y


def calculate_importance(model, X_test, y_test):
    print("\nCalculating permutation importance...")

    result = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="f1",
        n_repeats=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    importance_df = pd.DataFrame(
        {
            "feature": X_test.columns,
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
        }
    )

    importance_df = importance_df.sort_values(
        by="importance_mean",
        ascending=False,
    )

    return importance_df


def save_results(importance_df):
    importance_df.to_csv(
        CSV_PATH,
        index=False,
    )

    print(f"\nFeature importance saved to:")
    print(CSV_PATH)


def create_plot(importance_df):
    top_features = importance_df.head(15).copy()

    top_features = top_features.sort_values(
        by="importance_mean",
        ascending=True,
    )

    plt.figure(figsize=(10, 7))

    plt.barh(
        top_features["feature"],
        top_features["importance_mean"],
        xerr=top_features["importance_std"],
    )

    plt.xlabel("Mean decrease in F1 after permutation")
    plt.ylabel("Feature")
    plt.title("KINETICS - Global Feature Importance")
    plt.tight_layout()

    plt.savefig(
        PLOT_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print("\nFeature importance plot saved to:")
    print(PLOT_PATH)


def main():
    print("=" * 70)
    print("KINETICS - MODEL EXPLAINABILITY")
    print("=" * 70)

    X, y = load_data()

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print(f"\nTest samples: {len(X_test)}")

    model = joblib.load(MODEL_PATH)

    importance_df = calculate_importance(
        model,
        X_test,
        y_test,
    )

    print("\nTop 15 features:")
    print(
        importance_df.head(15).to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}",
        )
    )

    save_results(importance_df)
    create_plot(importance_df)

    print("\n" + "=" * 70)
    print("EXPLAINABILITY COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
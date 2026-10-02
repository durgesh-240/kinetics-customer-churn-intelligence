from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_features.csv"
)

LOGISTIC_PATH = PROJECT_ROOT / "models" / "logistic_regression_tuned.joblib"
GB_PATH = PROJECT_ROOT / "models" / "gradient_boosting_tuned.joblib"

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = REPORT_DIR / "tuned_model_evaluation.csv"


TARGET = "Churn"

RANDOM_STATE = 42
TEST_SIZE = 0.20


def load_data():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    return X, y


def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model": name,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "pr_auc": average_precision_score(y_test, y_prob),
    }

    cm = confusion_matrix(y_test, y_pred)

    print()
    print("=" * 70)
    print(f"{name}")
    print("=" * 70)

    print(f"Accuracy : {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall   : {metrics['recall']:.4f}")
    print(f"F1       : {metrics['f1']:.4f}")
    print(f"ROC-AUC  : {metrics['roc_auc']:.4f}")
    print(f"PR-AUC   : {metrics['pr_auc']:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["Stayed", "Churned"],
            zero_division=0,
        )
    )

    return metrics


def main():
    print("=" * 70)
    print("KINETICS - FINAL TUNED MODEL EVALUATION")
    print("=" * 70)

    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples:     {len(X_test)}")
    print(f"Test churn rate:  {y_test.mean():.4f}")

    logistic_model = joblib.load(LOGISTIC_PATH)
    gb_model = joblib.load(GB_PATH)

    results = []

    results.append(
        evaluate_model(
            "Tuned Logistic Regression",
            logistic_model,
            X_test,
            y_test,
        )
    )

    results.append(
        evaluate_model(
            "Tuned Gradient Boosting",
            gb_model,
            X_test,
            y_test,
        )
    )

    results_df = pd.DataFrame(results)

    results_df.to_csv(RESULTS_PATH, index=False)

    print()
    print("=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print(f"\nResults saved to:")
    print(RESULTS_PATH)


if __name__ == "__main__":
    main()
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


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
    / "logistic_regression_baseline.joblib"
)

METRICS_PATH = (
    PROJECT_ROOT
    / "reports"
    / "baseline_metrics.txt"
)


NUMERIC_FEATURES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "ServiceCount",
    "AverageMonthlySpend",
]


CATEGORICAL_FEATURES = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]


TARGET_COLUMN = "Churn"


def load_data() -> pd.DataFrame:
    """Load the feature-engineered dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Feature dataset not found at: {DATA_PATH}\n"
            "Run: python -m src.features.build_features"
        )

    return pd.read_csv(DATA_PATH)


def build_pipeline() -> Pipeline:
    """Build preprocessing + Logistic Regression pipeline."""

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(),
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )

    model = LogisticRegression(
        max_iter=2000,
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    return pipeline


def evaluate_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """Calculate classification metrics."""

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    metrics = {
        "accuracy": accuracy_score(
            y_test,
            predictions,
        ),
        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),
        "pr_auc": average_precision_score(
            y_test,
            probabilities,
        ),
    }

    return metrics


def save_metrics(
    metrics: dict,
    report: str,
) -> None:
    """Save model metrics and classification report."""

    METRICS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "KINETICS - LOGISTIC REGRESSION BASELINE\n"
        )
        file.write(
            "=" * 60 + "\n\n"
        )

        for name, value in metrics.items():
            file.write(
                f"{name.upper():<15}: "
                f"{value:.4f}\n"
            )

        file.write(
            "\nClassification Report\n"
        )
        file.write(
            "-" * 60 + "\n"
        )
        file.write(report)

    print(
        f"\nMetrics saved to:\n"
        f"{METRICS_PATH}"
    )


def main() -> None:
    print("=" * 70)
    print("KINETICS - LOGISTIC REGRESSION BASELINE")
    print("=" * 70)

    df = load_data()

    X = df[
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ]

    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y,
        )
    )

    print(
        f"\nTraining samples: "
        f"{len(X_train):,}"
    )

    print(
        f"Test samples: "
        f"{len(X_test):,}"
    )

    print(
        f"Training churn rate: "
        f"{y_train.mean() * 100:.2f}%"
    )

    print(
        f"Test churn rate: "
        f"{y_test.mean() * 100:.2f}%"
    )

    model = build_pipeline()

    print(
        "\nTraining Logistic Regression..."
    )

    model.fit(
        X_train,
        y_train,
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test,
    )

    predictions = model.predict(X_test)

    report = classification_report(
        y_test,
        predictions,
        target_names=[
            "Stayed",
            "Churned",
        ],
        zero_division=0,
    )

    confusion = confusion_matrix(
        y_test,
        predictions,
    )

    print(
        "\n" + "=" * 70
    )
    print("BASELINE RESULTS")
    print("=" * 70)

    print(
        f"\nAccuracy : "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"Precision: "
        f"{metrics['precision']:.4f}"
    )

    print(
        f"Recall   : "
        f"{metrics['recall']:.4f}"
    )

    print(
        f"F1 Score : "
        f"{metrics['f1']:.4f}"
    )

    print(
        f"ROC-AUC  : "
        f"{metrics['roc_auc']:.4f}"
    )

    print(
        f"PR-AUC   : "
        f"{metrics['pr_auc']:.4f}"
    )

    print(
        "\nConfusion Matrix:"
    )

    print(confusion)

    print(
        "\nClassification Report:"
    )

    print(report)

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"Model saved to:\n"
        f"{MODEL_PATH}"
    )

    save_metrics(
        metrics,
        report,
    )

    print(
        "\nBaseline training complete."
    )


if __name__ == "__main__":
    main()
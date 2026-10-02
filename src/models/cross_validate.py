from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_features.csv"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "cross_validation.csv"
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
    """Load feature-engineered data."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH)


def build_preprocessor() -> ColumnTransformer:
    """Build shared preprocessing pipeline."""

    return ColumnTransformer(
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


def build_models() -> dict:
    """Create models for comparison."""

    return {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            random_state=42,
        ),
    }


def build_pipeline(classifier) -> Pipeline:
    """Combine preprocessing and classifier."""

    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                classifier,
            ),
        ]
    )


def main() -> None:

    print("=" * 70)
    print("KINETICS - CROSS VALIDATION")
    print("=" * 70)

    df = load_data()

    X = df[
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ]

    y = df[TARGET_COLUMN]

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    models = build_models()

    results = []

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
        "pr_auc": "average_precision",
    }

    for model_name, classifier in models.items():

        print(
            f"\n{'-' * 70}"
        )

        print(
            f"Evaluating: {model_name}"
        )

        pipeline = build_pipeline(
            classifier
        )

        scores = cross_validate(
            pipeline,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )

        result = {
            "model": model_name,
        }

        for metric_name in scoring:
            test_scores = scores[
                f"test_{metric_name}"
            ]

            result[
                f"{metric_name}_mean"
            ] = test_scores.mean()

            result[
                f"{metric_name}_std"
            ] = test_scores.std()

            print(
                f"{metric_name.upper():<10}: "
                f"{test_scores.mean():.4f} "
                f"+/- "
                f"{test_scores.std():.4f}"
            )

        results.append(result)

    results_df = pd.DataFrame(
        results
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df.to_csv(
        REPORT_PATH,
        index=False,
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "CROSS-VALIDATION SUMMARY"
    )

    print("=" * 70)

    display_columns = [
        "model",
        "f1_mean",
        "f1_std",
        "roc_auc_mean",
        "roc_auc_std",
        "pr_auc_mean",
        "pr_auc_std",
    ]

    print(
        results_df[
            display_columns
        ].to_string(
            index=False,
            float_format=lambda value: f"{value:.4f}",
        )
    )

    print(
        f"\nResults saved to:\n"
        f"{REPORT_PATH}"
    )

    print(
        "\nCross-validation complete."
    )


if __name__ == "__main__":
    main()
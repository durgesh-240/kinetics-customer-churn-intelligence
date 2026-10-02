from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold,
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
    / "tuning_results.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
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
    """Build preprocessing pipeline."""

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


def build_logistic_pipeline() -> Pipeline:
    """Create Logistic Regression pipeline."""

    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=2000,
                    random_state=42,
                ),
            ),
        ]
    )


def build_gradient_boosting_pipeline() -> Pipeline:
    """Create Gradient Boosting pipeline."""

    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                GradientBoostingClassifier(
                    random_state=42,
                ),
            ),
        ]
    )


def tune_model(
    name: str,
    pipeline: Pipeline,
    parameter_distributions: dict,
    X: pd.DataFrame,
    y: pd.Series,
) -> RandomizedSearchCV:

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=parameter_distributions,
        n_iter=15,
        scoring="f1",
        cv=cv,
        random_state=42,
        n_jobs=-1,
        refit=True,
        verbose=1,
    )

    print(
        f"\n{'=' * 70}"
    )

    print(
        f"TUNING: {name}"
    )

    print(
        f"{'=' * 70}"
    )

    search.fit(
        X,
        y,
    )

    print(
        f"\nBest F1: "
        f"{search.best_score_:.4f}"
    )

    print(
        "\nBest parameters:"
    )

    for parameter, value in (
        search.best_params_.items()
    ):
        print(
            f"  {parameter}: {value}"
        )

    return search


def main() -> None:

    print("=" * 70)
    print("KINETICS - HYPERPARAMETER TUNING")
    print("=" * 70)

    df = load_data()

    X = df[
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ]

    y = df[TARGET_COLUMN]

    logistic_pipeline = (
        build_logistic_pipeline()
    )

    logistic_parameters = {
        "model__C": [
            0.01,
            0.05,
            0.1,
            0.25,
            0.5,
            1.0,
            2.0,
            5.0,
            10.0,
        ],
        "model__class_weight": [
            None,
            "balanced",
        ],
        "model__solver": [
            "liblinear",
            "lbfgs",
        ],
    }

    gradient_pipeline = (
        build_gradient_boosting_pipeline()
    )

    gradient_parameters = {
        "model__n_estimators": [
            100,
            150,
            200,
            250,
            300,
        ],
        "model__learning_rate": [
            0.01,
            0.03,
            0.05,
            0.08,
            0.1,
        ],
        "model__max_depth": [
            2,
            3,
            4,
        ],
        "model__min_samples_leaf": [
            5,
            10,
            15,
            20,
        ],
        "model__subsample": [
            0.7,
            0.8,
            0.9,
            1.0,
        ],
    }

    logistic_search = tune_model(
        name="Logistic Regression",
        pipeline=logistic_pipeline,
        parameter_distributions=logistic_parameters,
        X=X,
        y=y,
    )

    gradient_search = tune_model(
        name="Gradient Boosting",
        pipeline=gradient_pipeline,
        parameter_distributions=gradient_parameters,
        X=X,
        y=y,
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    logistic_model_path = (
        MODEL_DIR
        / "logistic_regression_tuned.joblib"
    )

    gradient_model_path = (
        MODEL_DIR
        / "gradient_boosting_tuned.joblib"
    )

    joblib.dump(
        logistic_search.best_estimator_,
        logistic_model_path,
    )

    joblib.dump(
        gradient_search.best_estimator_,
        gradient_model_path,
    )

    results = pd.DataFrame(
        [
            {
                "model": "Logistic Regression",
                "best_cv_f1": logistic_search.best_score_,
                "best_parameters": str(
                    logistic_search.best_params_
                ),
            },
            {
                "model": "Gradient Boosting",
                "best_cv_f1": gradient_search.best_score_,
                "best_parameters": str(
                    gradient_search.best_params_
                ),
            },
        ]
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results.to_csv(
        REPORT_PATH,
        index=False,
    )

    print(
        f"\nTuning results saved to:\n"
        f"{REPORT_PATH}"
    )

    print(
        "\nTuned models saved:"
    )

    print(
        logistic_model_path
    )

    print(
        gradient_model_path
    )

    print(
        "\nHyperparameter tuning complete."
    )


if __name__ == "__main__":
    main()
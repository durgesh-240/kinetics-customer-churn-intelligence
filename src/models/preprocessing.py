from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FEATURE_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_features.csv"
)

PREPROCESSOR_PATH = (
    PROJECT_ROOT
    / "models"
    / "preprocessor.joblib"
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


def load_feature_data() -> pd.DataFrame:
    """Load the feature-engineered dataset."""

    if not FEATURE_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Feature dataset not found at: {FEATURE_DATA_PATH}\n"
            "Run: python -m src.features.build_features"
        )

    return pd.read_csv(FEATURE_DATA_PATH)


def build_preprocessor() -> ColumnTransformer:
    """
    Build the preprocessing pipeline.

    Numerical features:
        StandardScaler

    Categorical features:
        OneHotEncoder
    """

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

    return preprocessor


def main() -> None:
    print("=" * 70)
    print("KINETICS - PREPROCESSING PIPELINE")
    print("=" * 70)

    df = load_feature_data()

    X = df[
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ]

    y = df[TARGET_COLUMN]

    print(
        f"\nInput features: "
        f"{X.shape[1]}"
    )

    print(
        f"Rows: "
        f"{len(X):,}"
    )

    print(
        f"Target distribution:"
        f"\n  0 (Stayed): {(y == 0).sum():,}"
        f"\n  1 (Churned): {(y == 1).sum():,}"
    )

    preprocessor = build_preprocessor()

    X_transformed = preprocessor.fit_transform(X)

    print(
        f"\nTransformed feature count: "
        f"{X_transformed.shape[1]}"
    )

    print(
        f"Transformed matrix shape: "
        f"{X_transformed.shape}"
    )

    PREPROCESSOR_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        preprocessor,
        PREPROCESSOR_PATH,
    )

    print(
        f"\nPreprocessor saved to:\n"
        f"{PREPROCESSOR_PATH}"
    )

    print("\nPreprocessing pipeline complete.")


if __name__ == "__main__":
    main()
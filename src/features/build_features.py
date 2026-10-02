from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_clean.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_features.csv"
)


SERVICE_COLUMNS = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]


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


def load_clean_data() -> pd.DataFrame:
    """Load the cleaned dataset."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Clean dataset not found at: {INPUT_PATH}\n"
            "Run: python -m src.data.clean"
        )

    return pd.read_csv(INPUT_PATH)


def create_service_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ServiceCount.

    Counts active optional services. A value of 'Yes'
    represents an active service.
    """

    data = df.copy()

    existing_service_columns = [
        column
        for column in SERVICE_COLUMNS
        if column in data.columns
    ]

    data["ServiceCount"] = (
        data[existing_service_columns]
        .eq("Yes")
        .sum(axis=1)
    )

    return data


def create_average_monthly_spend(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create AverageMonthlySpend.

    Uses TotalCharges / tenure.

    For customers with zero tenure, the feature is
    set to MonthlyCharges.
    """

    data = df.copy()

    data["AverageMonthlySpend"] = (
        data["TotalCharges"]
        / data["tenure"].replace(0, pd.NA)
    )

    data["AverageMonthlySpend"] = (
        data["AverageMonthlySpend"]
        .fillna(data["MonthlyCharges"])
    )

    return data


def validate_features(df: pd.DataFrame) -> None:
    """Validate the engineered dataset."""

    required_columns = (
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
        + [TARGET_COLUMN]
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(
                f"  - {column}"
                for column in missing_columns
            )
        )

    if df[required_columns].isnull().any().any():
        missing = (
            df[required_columns]
            .isnull()
            .sum()
        )

        missing = missing[missing > 0]

        raise ValueError(
            "Missing values detected:\n"
            f"{missing}"
        )

    if (df["ServiceCount"] < 0).any():
        raise ValueError(
            "ServiceCount contains negative values."
        )

    if (df["AverageMonthlySpend"] < 0).any():
        raise ValueError(
            "AverageMonthlySpend contains negative values."
        )


def save_features(df: pd.DataFrame) -> None:
    """Save the feature-engineered dataset."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nFeature dataset saved to:\n"
        f"{OUTPUT_PATH}"
    )


def main() -> None:
    print("=" * 70)
    print("KINETICS - FEATURE ENGINEERING")
    print("=" * 70)

    df = load_clean_data()

    print(
        f"\nInput dataset: "
        f"{len(df):,} rows × {len(df.columns)} columns"
    )

    df = create_service_count(df)

    df = create_average_monthly_spend(df)

    validate_features(df)

    print("\nEngineered features:")

    print(
        f"  ServiceCount"
        f"                  min={df['ServiceCount'].min()}"
        f", max={df['ServiceCount'].max()}"
        f", mean={df['ServiceCount'].mean():.2f}"
    )

    print(
        f"  AverageMonthlySpend"
        f"        min=${df['AverageMonthlySpend'].min():.2f}"
        f", max=${df['AverageMonthlySpend'].max():.2f}"
        f", mean=${df['AverageMonthlySpend'].mean():.2f}"
    )

    print(
        f"\nTotal features before target: "
        f"{len(NUMERIC_FEATURES) + len(CATEGORICAL_FEATURES)}"
    )

    print(
        f"Total dataset columns: "
        f"{len(df.columns)}"
    )

    save_features(df)

    print("\nFeature engineering complete.")


if __name__ == "__main__":
    main()
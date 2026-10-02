from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Telco-Customer-Churn.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_clean.csv"
)


def load_raw_data() -> pd.DataFrame:
    """Load the original Telco Customer Churn dataset."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at: {RAW_DATA_PATH}\n"
            "Run: python scripts/download_data.py"
        )

    return pd.read_csv(RAW_DATA_PATH)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the raw churn dataset.

    Operations:
    - Remove customerID from modeling data.
    - Convert TotalCharges to numeric.
    - Remove rows where TotalCharges cannot be interpreted numerically.
    - Convert Churn into binary target.
    """

    data = df.copy()

    # ---------------------------------------------------------
    # 1. Remove identifier
    # ---------------------------------------------------------

    if "customerID" in data.columns:
        data = data.drop(columns=["customerID"])

    # ---------------------------------------------------------
    # 2. Convert TotalCharges to numeric
    # ---------------------------------------------------------

    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"],
        errors="coerce"
    )

    invalid_total_charges = data["TotalCharges"].isna().sum()

    if invalid_total_charges > 0:
        print(
            f"Removing {invalid_total_charges} rows with "
            "invalid TotalCharges values."
        )

        data = data.dropna(subset=["TotalCharges"])

    # ---------------------------------------------------------
    # 3. Convert target to binary
    # ---------------------------------------------------------

    if "Churn" not in data.columns:
        raise ValueError("Target column 'Churn' not found.")

    target_mapping = {
        "No": 0,
        "Yes": 1,
    }

    data["Churn"] = data["Churn"].map(target_mapping)

    if data["Churn"].isna().any():
        raise ValueError(
            "Unexpected values found in Churn column."
        )

    data["Churn"] = data["Churn"].astype(int)

    # ---------------------------------------------------------
    # 4. Remove duplicate rows after transformation
    # ---------------------------------------------------------

    duplicate_count = data.duplicated().sum()

    if duplicate_count > 0:
        print(
            f"Removing {duplicate_count} duplicate rows."
        )

        data = data.drop_duplicates()

    # ---------------------------------------------------------
    # 5. Final validation
    # ---------------------------------------------------------

    if data.isnull().any().any():
        missing_columns = (
            data.isnull()
            .sum()
            .loc[lambda x: x > 0]
        )

        raise ValueError(
            "Missing values remain after cleaning:\n"
            f"{missing_columns}"
        )

    if not set(data["Churn"].unique()).issubset({0, 1}):
        raise ValueError(
            "Churn contains values other than 0 and 1."
        )

    return data


def save_processed_data(df: pd.DataFrame) -> None:
    """Save the cleaned dataset."""

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        f"\nProcessed dataset saved to:\n"
        f"{PROCESSED_DATA_PATH}"
    )


def main() -> None:
    print("=" * 70)
    print("KINETICS - DATA CLEANING")
    print("=" * 70)

    raw_data = load_raw_data()

    print(f"\nRaw rows: {len(raw_data):,}")
    print(f"Raw columns: {len(raw_data.columns):,}")

    cleaned_data = clean_data(raw_data)

    print(f"\nCleaned rows: {len(cleaned_data):,}")
    print(f"Cleaned columns: {len(cleaned_data.columns):,}")

    print("\nTarget distribution:")

    churn_counts = cleaned_data["Churn"].value_counts()

    for value, count in churn_counts.items():
        label = "Churned" if value == 1 else "Stayed"
        percentage = count / len(cleaned_data) * 100

        print(
            f"  {label}: "
            f"{count:,} "
            f"({percentage:.2f}%)"
        )

    save_processed_data(cleaned_data)

    print("\nData cleaning complete.")


if __name__ == "__main__":
    main()
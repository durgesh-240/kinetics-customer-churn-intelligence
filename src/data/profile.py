from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"


def load_data() -> pd.DataFrame:
    """Load the raw Telco Customer Churn dataset."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}\n"
            "Run: python scripts/download_data.py"
        )

    return pd.read_csv(DATA_PATH)


def profile_data(df: pd.DataFrame) -> None:
    """Print a basic data-quality and target-variable profile."""

    print("\n" + "=" * 70)
    print("KINETICS - DATA PROFILE")
    print("=" * 70)

    print("\n[1] Dataset Shape")
    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]:,}")

    print("\n[2] Columns")
    for column in df.columns:
        print(f"  - {column}")

    print("\n[3] Data Types")
    print(df.dtypes.to_string())

    print("\n[4] Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("  No missing values detected.")
    else:
        for column, count in missing.items():
            percentage = count / len(df) * 100
            print(f"  {column}: {count:,} ({percentage:.2f}%)")

    print("\n[5] Duplicate Rows")
    duplicates = df.duplicated().sum()
    print(f"  {duplicates:,}")

    print("\n[6] Target Distribution")

    if "Churn" in df.columns:
        churn_counts = df["Churn"].value_counts(dropna=False)
        churn_percentages = df["Churn"].value_counts(
            normalize=True,
            dropna=False
        ) * 100

        for value in churn_counts.index:
            print(
                f"  {value}: "
                f"{churn_counts[value]:,} "
                f"({churn_percentages[value]:.2f}%)"
            )
    else:
        print("  WARNING: 'Churn' column not found.")

    print("\n[7] Numeric Summary")

    numeric_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    if len(numeric_columns) > 0:
        print(
            df[numeric_columns]
            .describe()
            .transpose()
            .round(2)
            .to_string()
        )
    else:
        print("  No numeric columns found.")

    print("\n[8] Categorical Cardinality")

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:
        print(
            f"  {column}: "
            f"{df[column].nunique(dropna=False)} unique values"
        )

    print("\n" + "=" * 70)
    print("PROFILE COMPLETE")
    print("=" * 70)


def main() -> None:
    df = load_data()
    profile_data(df)


if __name__ == "__main__":
    main()
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "reports"
    / "eda"
)


def load_data() -> pd.DataFrame:
    """Load the cleaned dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found at: {DATA_PATH}\n"
            "Run: python -m src.data.clean"
        )

    return pd.read_csv(DATA_PATH)


def setup_output_directory() -> None:
    """Create the EDA output directory."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def save_plot(filename: str) -> None:
    """Save and close the current matplotlib figure."""

    path = OUTPUT_DIR / filename

    plt.tight_layout()
    plt.savefig(
        path,
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()

    print(f"Saved: {path}")


def plot_churn_distribution(df: pd.DataFrame) -> None:
    """Plot overall churn distribution."""

    plt.figure(figsize=(7, 5))

    sns.countplot(
        data=df,
        x="Churn"
    )

    plt.title("Customer Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Number of Customers")

    plt.xticks(
        [0, 1],
        ["Stayed", "Churned"]
    )

    save_plot("01_churn_distribution.png")


def plot_churn_by_contract(df: pd.DataFrame) -> None:
    """Analyze churn rate by contract type."""

    churn_rate = (
        df.groupby("Contract")["Churn"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=churn_rate.index,
        y=churn_rate.values
    )

    plt.title("Churn Rate by Contract Type")
    plt.xlabel("Contract Type")
    plt.ylabel("Churn Rate (%)")

    save_plot("02_churn_by_contract.png")


def plot_churn_by_internet_service(df: pd.DataFrame) -> None:
    """Analyze churn rate by internet service."""

    churn_rate = (
        df.groupby("InternetService")["Churn"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=churn_rate.index,
        y=churn_rate.values
    )

    plt.title("Churn Rate by Internet Service")
    plt.xlabel("Internet Service")
    plt.ylabel("Churn Rate (%)")

    save_plot("03_churn_by_internet_service.png")


def plot_churn_by_payment_method(df: pd.DataFrame) -> None:
    """Analyze churn rate by payment method."""

    churn_rate = (
        df.groupby("PaymentMethod")["Churn"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    plt.figure(figsize=(10, 5))

    sns.barplot(
        x=churn_rate.index,
        y=churn_rate.values
    )

    plt.title("Churn Rate by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Churn Rate (%)")

    plt.xticks(
        rotation=20,
        ha="right"
    )

    save_plot("04_churn_by_payment_method.png")


def plot_churn_by_tenure(df: pd.DataFrame) -> None:
    """Analyze the relationship between tenure and churn."""

    plt.figure(figsize=(9, 5))

    sns.boxplot(
        data=df,
        x="Churn",
        y="tenure"
    )

    plt.title("Tenure Distribution by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Tenure (Months)")

    plt.xticks(
        [0, 1],
        ["Stayed", "Churned"]
    )

    save_plot("05_tenure_vs_churn.png")


def plot_churn_by_monthly_charges(df: pd.DataFrame) -> None:
    """Analyze monthly charges by churn status."""

    plt.figure(figsize=(9, 5))

    sns.boxplot(
        data=df,
        x="Churn",
        y="MonthlyCharges"
    )

    plt.title("Monthly Charges by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Monthly Charges")

    plt.xticks(
        [0, 1],
        ["Stayed", "Churned"]
    )

    save_plot("06_monthly_charges_vs_churn.png")


def plot_churn_by_total_charges(df: pd.DataFrame) -> None:
    """Analyze total charges by churn status."""

    plt.figure(figsize=(9, 5))

    sns.boxplot(
        data=df,
        x="Churn",
        y="TotalCharges"
    )

    plt.title("Total Charges by Churn")
    plt.xlabel("Churn")
    plt.ylabel("Total Charges")

    plt.xticks(
        [0, 1],
        ["Stayed", "Churned"]
    )

    save_plot("07_total_charges_vs_churn.png")


def plot_tenure_distribution(df: pd.DataFrame) -> None:
    """Plot tenure distribution by churn status."""

    plt.figure(figsize=(10, 6))

    sns.histplot(
        data=df,
        x="tenure",
        hue="Churn",
        bins=30,
        kde=True,
        element="step"
    )

    plt.title("Tenure Distribution by Churn")
    plt.xlabel("Tenure (Months)")
    plt.ylabel("Number of Customers")

    save_plot("08_tenure_distribution.png")


def plot_monthly_charges_distribution(df: pd.DataFrame) -> None:
    """Plot monthly charges distribution by churn status."""

    plt.figure(figsize=(10, 6))

    sns.histplot(
        data=df,
        x="MonthlyCharges",
        hue="Churn",
        bins=30,
        kde=True,
        element="step"
    )

    plt.title("Monthly Charges Distribution by Churn")
    plt.xlabel("Monthly Charges")
    plt.ylabel("Number of Customers")

    save_plot("09_monthly_charges_distribution.png")


def print_key_statistics(df: pd.DataFrame) -> None:
    """Print important churn statistics."""

    print("\n" + "=" * 70)
    print("KINETICS - KEY EDA STATISTICS")
    print("=" * 70)

    overall_churn = df["Churn"].mean() * 100

    print(
        f"\nOverall churn rate: "
        f"{overall_churn:.2f}%"
    )

    print("\nChurn rate by contract:")

    contract_churn = (
        df.groupby("Contract")["Churn"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    for contract, rate in contract_churn.items():
        print(
            f"  {contract}: "
            f"{rate:.2f}%"
        )

    print("\nChurn rate by internet service:")

    internet_churn = (
        df.groupby("InternetService")["Churn"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    for service, rate in internet_churn.items():
        print(
            f"  {service}: "
            f"{rate:.2f}%"
        )

    print("\nChurn rate by payment method:")

    payment_churn = (
        df.groupby("PaymentMethod")["Churn"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    for method, rate in payment_churn.items():
        print(
            f"  {method}: "
            f"{rate:.2f}%"
        )

    print("\nAverage tenure:")

    tenure_stats = (
        df.groupby("Churn")["tenure"]
        .mean()
    )

    print(
        f"  Stayed  : "
        f"{tenure_stats[0]:.2f} months"
    )

    print(
        f"  Churned : "
        f"{tenure_stats[1]:.2f} months"
    )

    print("\nAverage monthly charges:")

    monthly_stats = (
        df.groupby("Churn")["MonthlyCharges"]
        .mean()
    )

    print(
        f"  Stayed  : "
        f"${monthly_stats[0]:.2f}"
    )

    print(
        f"  Churned : "
        f"${monthly_stats[1]:.2f}"
    )


def main() -> None:
    print("=" * 70)
    print("KINETICS - EXPLORATORY DATA ANALYSIS")
    print("=" * 70)

    df = load_data()

    setup_output_directory()

    print(f"\nLoaded {len(df):,} customers.")

    plot_churn_distribution(df)
    plot_churn_by_contract(df)
    plot_churn_by_internet_service(df)
    plot_churn_by_payment_method(df)
    plot_churn_by_tenure(df)
    plot_churn_by_monthly_charges(df)
    plot_churn_by_total_charges(df)
    plot_tenure_distribution(df)
    plot_monthly_charges_distribution(df)

    print_key_statistics(df)

    print("\nEDA complete.")
    print(f"Charts saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
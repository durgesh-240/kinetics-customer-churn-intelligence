from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw/Telco-Customer-Churn.csv")
PROCESSED_PATH = Path("data/processed/telco_clean.csv")


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data.columns = [c.strip() for c in data.columns]
    data["TotalCharges"] = pd.to_numeric(data["TotalCharges"], errors="coerce")
    data["Churn"] = data["Churn"].map({"Yes": 1, "No": 0}).astype("Int64")
    data = data.drop_duplicates(subset=["customerID"]).reset_index(drop=True)
    return data


def main() -> None:
    df = clean(load_raw())
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved {len(df):,} rows to {PROCESSED_PATH}")
    print(df.isna().sum().sort_values(ascending=False).head(10))


if __name__ == "__main__":
    main()

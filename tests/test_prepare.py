import pandas as pd
from src.data.prepare import clean


def test_clean_maps_target_and_total_charges():
    df = pd.DataFrame({
        "customerID": ["A", "B"],
        "TotalCharges": ["100.0", ""],
        "Churn": ["Yes", "No"],
    })
    result = clean(df)
    assert result["Churn"].tolist() == [1, 0]
    assert result["TotalCharges"].isna().sum() == 1

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap

from sklearn.model_selection import train_test_split


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
    / "gradient_boosting_tuned.joblib"
)

REPORT_DIR = PROJECT_ROOT / "reports"
EXPLANATION_DIR = REPORT_DIR / "local_explanations"

EXPLANATION_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = (
    EXPLANATION_DIR
    / "sample_customer_explanation.csv"
)

TARGET = "Churn"
RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    return X, y


def get_transformed_feature_names(preprocessor):
    """
    Return the exact feature names produced by the fitted
    ColumnTransformer.
    """

    names = preprocessor.get_feature_names_out()

    return np.asarray(names)


def aggregate_shap_values(
    shap_values,
    transformed_feature_names,
    original_features,
):
    """
    Aggregate one-hot encoded SHAP values back to the
    original business-level feature.

    Example:

        cat__Contract_Month-to-month
        cat__Contract_One year
        cat__Contract_Two year

    become:

        Contract
    """

    aggregated = {}

    for original_feature in original_features:

        indices = []

        for i, transformed_name in enumerate(
            transformed_feature_names
        ):
            cleaned_name = transformed_name

            if "__" in cleaned_name:
                cleaned_name = cleaned_name.split(
                    "__",
                    1,
                )[1]

            if (
                cleaned_name == original_feature
                or cleaned_name.startswith(
                    original_feature + "_"
                )
            ):
                indices.append(i)

        if indices:
            aggregated[original_feature] = float(
                np.sum(
                    shap_values[indices]
                )
            )

    return pd.Series(
        aggregated,
        dtype=float,
    )


def explain_customer(
    model,
    X_customer,
    background_data,
):
    """
    Generate SHAP values for a single customer.
    """

    preprocessor = model.named_steps["preprocessor"]
    estimator = model.named_steps["model"]

    X_background_transformed = (
        preprocessor.transform(
            background_data
        )
    )

    X_customer_transformed = (
        preprocessor.transform(
            X_customer
        )
    )

    feature_names = get_transformed_feature_names(
        preprocessor
    )

    print("\nTransformed background shape:")
    print(X_background_transformed.shape)

    print("Transformed customer shape:")
    print(X_customer_transformed.shape)

    print("\nTransformed feature count:")
    print(len(feature_names))

    print("\nFirst 10 transformed features:")

    for feature in feature_names[:10]:
        print(f"  {feature}")

    print("\nCreating SHAP explainer...")

    explainer = shap.TreeExplainer(
        estimator
    )

    shap_output = explainer(
        X_customer_transformed
    )

    shap_values = shap_output.values

    print("\nRaw SHAP output shape:")
    print(shap_values.shape)

    print("Raw SHAP output type:")
    print(type(shap_values))

    if shap_values.ndim == 3:
        if shap_values.shape[-1] == 2:
            shap_values = shap_values[:, :, 1]
        else:
            shap_values = shap_values[:, :, 0]

    if shap_values.ndim != 2:
        raise ValueError(
            f"Unexpected SHAP output shape: "
            f"{shap_values.shape}"
        )

    customer_shap_values = shap_values[0]

    print("\nCustomer SHAP vector length:")
    print(len(customer_shap_values))

    print("Transformed feature count:")
    print(len(feature_names))

    if len(customer_shap_values) != len(feature_names):
        raise ValueError(
            "SHAP value count does not match "
            "transformed feature count."
        )

    aggregated = aggregate_shap_values(
        customer_shap_values,
        feature_names,
        X_customer.columns,
    )

    return aggregated


def create_explanation_table(
    shap_series,
    churn_probability,
):
    """
    Create a business-friendly explanation table.
    """

    explanation = pd.DataFrame(
        {
            "feature": shap_series.index,
            "shap_value": shap_series.values,
        }
    )

    explanation["impact"] = np.where(
        explanation["shap_value"] > 0,
        "Increases churn risk",
        "Decreases churn risk",
    )

    explanation["absolute_impact"] = (
        explanation["shap_value"].abs()
    )

    explanation["churn_probability"] = (
        churn_probability
    )

    explanation = explanation.sort_values(
        by="absolute_impact",
        ascending=False,
    )

    return explanation


def main():
    print("=" * 70)
    print("KINETICS - LOCAL MODEL EXPLAINABILITY")
    print("=" * 70)

    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print(f"\nTest samples: {len(X_test)}")

    model = joblib.load(MODEL_PATH)

    print("\nLoaded model:")
    print(MODEL_PATH)

    # Use the first test customer as a reproducible example.
    customer_index = X_test.index[0]

    X_customer = X_test.loc[
        [customer_index]
    ]

    y_actual = y_test.loc[
        customer_index
    ]

    churn_probability = model.predict_proba(
        X_customer
    )[0, 1]

    prediction = int(
        churn_probability >= 0.5
    )

    print("\n" + "=" * 70)
    print("CUSTOMER")
    print("=" * 70)

    print(f"Actual churn:      {y_actual}")
    print(f"Predicted churn:   {prediction}")
    print(
        f"Churn probability: {churn_probability:.4f}"
    )

    print("\nCustomer attributes:")

    print(
        X_customer.T.to_string(
            header=False
        )
    )

    background_data = X_train.sample(
        n=min(500, len(X_train)),
        random_state=RANDOM_STATE,
    )

    shap_series = explain_customer(
        model,
        X_customer,
        background_data,
    )

    explanation = create_explanation_table(
        shap_series,
        churn_probability,
    )

    print("\n" + "=" * 70)
    print("TOP CHURN DRIVERS")
    print("=" * 70)

    if explanation.empty:
        print(
            "No SHAP features were generated."
        )
    else:
        print(
            explanation.head(10).to_string(
                index=False,
                float_format=lambda x: f"{x:.6f}",
            )
        )

    explanation.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\nExplanation saved to:")
    print(OUTPUT_PATH)

    print("\n" + "=" * 70)
    print("LOCAL EXPLAINABILITY COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
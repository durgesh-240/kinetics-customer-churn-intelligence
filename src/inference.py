from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "gradient_boosting_tuned.joblib"
)

GLOBAL_IMPORTANCE_PATH = (
    PROJECT_ROOT
    / "reports"
    / "feature_importance"
    / "permutation_importance.csv"
)


class KineticsInference:
    """
    Central inference service for KINETICS.

    Responsible for:
    - Loading the trained model
    - Generating churn probability
    - Assigning risk level
    - Generating local SHAP explanations
    - Loading global feature importance
    """

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

        self.global_importance = (
            pd.read_csv(GLOBAL_IMPORTANCE_PATH)
            if GLOBAL_IMPORTANCE_PATH.exists()
            else pd.DataFrame()
        )

        self.preprocessor = (
            self.model.named_steps["preprocessor"]
        )

        self.estimator = (
            self.model.named_steps["model"]
        )

    def predict_customer(self, customer_data: dict) -> dict:
        """
        Predict churn risk for one customer.
        """

        X = pd.DataFrame([customer_data])

        probability = float(
            self.model.predict_proba(X)[0, 1]
        )

        prediction = int(
            probability >= 0.5
        )

        risk_level = self._get_risk_level(
            probability
        )

        local_explanation = (
            self._get_local_explanation(X)
        )

        global_drivers = (
            self._get_global_drivers()
        )

        return {
            "churn_probability": round(
                probability,
                4,
            ),
            "prediction": prediction,
            "risk_level": risk_level,
            "local_explanation": local_explanation,
            "global_drivers": global_drivers,
        }

    @staticmethod
    def _get_risk_level(probability: float) -> str:
        """
        Convert churn probability into a
        business-readable risk category.
        """

        if probability >= 0.70:
            return "HIGH"

        if probability >= 0.40:
            return "MEDIUM"

        return "LOW"

    def _get_global_drivers(self, limit: int = 10):
        """
        Return globally important features.
        """

        if self.global_importance.empty:
            return []

        top_features = (
            self.global_importance
            .head(limit)
        )

        return [
            {
                "feature": row["feature"],
                "importance": round(
                    float(
                        row["importance_mean"]
                    ),
                    6,
                ),
            }
            for _, row in top_features.iterrows()
        ]

    def _get_local_explanation(
        self,
        X: pd.DataFrame,
        limit: int = 8,
    ):
        """
        Generate local SHAP explanations.
        """

        X_transformed = (
            self.preprocessor.transform(X)
        )

        feature_names = (
            self.preprocessor
            .get_feature_names_out()
        )

        explainer = shap.TreeExplainer(
            self.estimator
        )

        shap_output = explainer(
            X_transformed
        )

        shap_values = shap_output.values

        if shap_values.ndim == 3:
            if shap_values.shape[-1] == 2:
                shap_values = (
                    shap_values[:, :, 1]
                )
            else:
                shap_values = (
                    shap_values[:, :, 0]
                )

        customer_values = shap_values[0]

        aggregated = {}

        for i, transformed_name in enumerate(
            feature_names
        ):
            clean_name = transformed_name

            if "__" in clean_name:
                clean_name = clean_name.split(
                    "__",
                    1,
                )[1]

            original_feature = (
                clean_name.split("_", 1)[0]
            )

            # Handle engineered features and
            # numerical features without underscores.
            for feature in X.columns:
                if (
                    clean_name == feature
                    or clean_name.startswith(
                        feature + "_"
                    )
                ):
                    original_feature = feature
                    break

            if original_feature not in aggregated:
                aggregated[
                    original_feature
                ] = 0.0

            aggregated[
                original_feature
            ] += float(
                customer_values[i]
            )

        explanation = []

        for feature, value in aggregated.items():
            explanation.append(
                {
                    "feature": feature,
                    "shap_value": round(
                        value,
                        6,
                    ),
                    "impact": (
                        "Increases churn risk"
                        if value > 0
                        else "Decreases churn risk"
                    ),
                    "absolute_impact": round(
                        abs(value),
                        6,
                    ),
                }
            )

        explanation.sort(
            key=lambda x: x["absolute_impact"],
            reverse=True,
        )

        return explanation[:limit]


inference_service = KineticsInference()


def predict_customer(customer_data: dict) -> dict:
    """
    Public inference function.

    FastAPI and other application layers
    should use this function rather than
    loading the model directly.
    """

    return inference_service.predict_customer(
        customer_data
    )


if __name__ == "__main__":

    sample_customer = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 5,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Credit card (automatic)",
        "MonthlyCharges": 44.05,
        "TotalCharges": 202.15,
        "ServiceCount": 0,
        "AverageMonthlySpend": 40.43,
    }

    result = predict_customer(
        sample_customer
    )

    print("=" * 70)
    print("KINETICS - INFERENCE TEST")
    print("=" * 70)

    print(
        f"\nChurn probability: "
        f"{result['churn_probability']:.2%}"
    )

    print(
        f"Prediction: "
        f"{'CHURN' if result['prediction'] else 'STAY'}"
    )

    print(
        f"Risk level: "
        f"{result['risk_level']}"
    )

    print("\nLocal explanation:")

    for item in result[
        "local_explanation"
    ]:
        print(
            f"  {item['feature']}: "
            f"{item['shap_value']:+.4f} "
            f"-> {item['impact']}"
        )

    print("\nGlobal drivers:")

    for item in result[
        "global_drivers"
    ]:
        print(
            f"  {item['feature']}: "
            f"{item['importance']:.4f}"
        )

    print("\nInference test complete.")
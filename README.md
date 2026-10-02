# Kinetics

## Customer Behavior & Churn Intelligence Platform

Kinetics is an end-to-end machine learning and analytics project that studies customer behavior, estimates churn risk, explains individual predictions, and exposes the resulting model through a production-style API and full-stack web application.

### Project goal

The project is deliberately built as more than a classification notebook:

**Data → Preparation → EDA → Feature Engineering → ML → Evaluation → Explainability → API → Web App → Retention Insights**

### Planned stack

- Python, Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn, SHAP
- FastAPI + Pydantic
- PostgreSQL / Supabase
- React + TypeScript + Vite + Tailwind CSS
- Docker + pytest

### Dataset

The initial case study uses IBM's public Telco Customer Churn sample dataset. IBM describes it as fictional telecommunications customer data, with 7,043 customers and a churn label indicating whether a customer left. The original IBM repository is archived, so the project keeps the raw-data download reproducible rather than treating the dataset as a live source.

Source: https://github.com/IBM/telco-customer-churn-on-icp4d

### Important modeling constraint

This dataset is a cross-sectional snapshot. It does not contain monthly customer snapshots suitable for true temporal forecasting. Therefore Kinetics will frame the first model as **churn-risk classification from observed customer attributes**, not as a causal claim or guaranteed future forecast.

### Repository structure

```text
Kinetics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── explainability/
├── models/
├── reports/
├── backend/
├── frontend/
├── tests/
├── scripts/
├── requirements.txt
└── README.md
```

### First milestone

1. Download and verify the raw dataset.
2. Profile the data and document data quality issues.
3. Build a leakage-safe preprocessing pipeline.
4. Establish a Logistic Regression baseline.
5. Evaluate with precision, recall, F1, ROC-AUC and PR-AUC.
6. Save the preprocessing/model artifact for later API integration.

### Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py
python -m src.models.train_baseline
```

The frontend and API will be added after the data and model pipeline is validated.

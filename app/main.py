from fastapi import FastAPI
import joblib
import pandas as pd
import logging

app = FastAPI()

# 🔴 Logging fix (important)
logging.basicConfig(
    filename="predictions.log",   # root এ save হবে
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    force=True
)

# Load artifacts
model = joblib.load("artifacts/model.pkl")
columns = joblib.load("artifacts/columns.pkl")

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
def predict(data: dict):
    
    # Convert input to dataframe
    df = pd.DataFrame([data])

    # Fix TotalCharges
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Fill missing values
    df = df.fillna(0)

    # Feature engineering
    if "tenure" in df.columns and "MonthlyCharges" in df.columns:
        df["avg_monthly_value"] = df["MonthlyCharges"] / (df["tenure"] + 1)

    # Encoding
    df = pd.get_dummies(df, drop_first=True)

    # Align columns
    df = df.reindex(columns=columns, fill_value=0)

    # Prediction
    pred = int(model.predict(df)[0])
    result = "Churn" if pred == 1 else "No Churn"

    # ✅ Logging
    logging.info(f"Input: {data} | Prediction: {result}")

    return {"prediction": result}
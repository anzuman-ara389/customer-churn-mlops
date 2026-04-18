from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging

app = FastAPI()

class CustomerInput(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

logging.basicConfig(
    filename="predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    force=True
)

model = joblib.load("artifacts/model.pkl")
columns = joblib.load("artifacts/columns.pkl")

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
def predict(data: CustomerInput):
    df = pd.DataFrame([data.model_dump()])

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    df = df.fillna(0)

    if "tenure" in df.columns and "MonthlyCharges" in df.columns:
        df["avg_monthly_value"] = df["MonthlyCharges"] / (df["tenure"] + 1)

    df = pd.get_dummies(df, drop_first=True)
    df = df.reindex(columns=columns, fill_value=0)

    pred = int(model.predict(df)[0])
    result = "Churn" if pred == 1 else "No Churn"

    logging.info(f"Input: {data.model_dump()} | Prediction: {result}")

    return {"prediction": result}
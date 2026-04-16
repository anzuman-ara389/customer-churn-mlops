import os
import json
from datetime import datetime
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

ARTIFACT_DIR = "artifacts"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

df = pd.read_csv("data/processed_data.csv")

X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

metrics = {
    "timestamp": datetime.now().isoformat(),
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, zero_division=0),
    "recall": recall_score(y_test, y_pred, zero_division=0),
    "f1_score": f1_score(y_test, y_pred, zero_division=0)
}

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

joblib.dump(model, f"{ARTIFACT_DIR}/model_{timestamp}.pkl")
joblib.dump(list(X.columns), f"{ARTIFACT_DIR}/columns_{timestamp}.pkl")

with open(f"{ARTIFACT_DIR}/metrics_{timestamp}.json", "w") as f:
    json.dump(metrics, f, indent=2)

joblib.dump(model, f"{ARTIFACT_DIR}/model_latest.pkl")
joblib.dump(list(X.columns), f"{ARTIFACT_DIR}/columns_latest.pkl")

with open(f"{ARTIFACT_DIR}/metrics_latest.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("Training complete. Model and metrics saved.")
print(metrics)
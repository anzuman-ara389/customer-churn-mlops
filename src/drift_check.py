import os
import json
import sqlite3
from datetime import datetime
import pandas as pd

DB_PATH = "data/database.db"
ARTIFACT_DIR = "artifacts"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def load_tables():
    conn = sqlite3.connect(DB_PATH)
    historical = pd.read_sql("SELECT * FROM historical_data", conn)
    new_data = pd.read_sql("SELECT * FROM new_data", conn)
    conn.close()
    return historical, new_data

def compute_drift_report(historical, new_data):
    report = {
        "timestamp": datetime.now().isoformat(),
        "drift_detected": False,
        "checks": {}
    }

    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]

    for col in numeric_cols:
        if col in historical.columns and col in new_data.columns:
            hist_mean = pd.to_numeric(historical[col], errors="coerce").mean()
            new_mean = pd.to_numeric(new_data[col], errors="coerce").mean()

            if pd.isna(hist_mean) or pd.isna(new_mean):
                continue

            diff_ratio = abs(new_mean - hist_mean) / (abs(hist_mean) + 1e-6)

            report["checks"][col] = {
                "historical_mean": float(hist_mean),
                "new_data_mean": float(new_mean),
                "relative_difference": float(diff_ratio)
            }

            if diff_ratio > 0.20:
                report["drift_detected"] = True

    return report

if __name__ == "__main__":
    historical, new_data = load_tables()
    report = compute_drift_report(historical, new_data)

    with open(os.path.join(ARTIFACT_DIR, "drift_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    print("Drift report saved.")
    print(json.dumps(report, indent=2))
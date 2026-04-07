import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

INPUT_PATH = "data/processed_data.csv"
MODEL_PATH = "artifacts/model.pkl"
METRICS_PATH = "artifacts/metrics.txt"
COLUMNS_PATH = "artifacts/columns.pkl"


def train():
    df = pd.read_csv(INPUT_PATH)

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    preds = model.predict(X)
    acc = accuracy_score(y, preds)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(list(X.columns), COLUMNS_PATH)

    with open(METRICS_PATH, "w") as f:
        f.write(f"Accuracy: {acc}")

    print("Training done")
    print("Accuracy:", acc)


if __name__ == "__main__":
    train()
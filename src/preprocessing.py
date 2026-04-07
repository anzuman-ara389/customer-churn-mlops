import pandas as pd

INPUT_PATH = "data/historical_data.csv"
OUTPUT_PATH = "data/processed_data.csv"


def preprocess():
    df = pd.read_csv(INPUT_PATH)

    if "customerID" in df.columns:
        df = df.drop("customerID", axis=1)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.fillna(0)

    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    if "tenure" in df.columns and "MonthlyCharges" in df.columns:
        df["avg_monthly_value"] = df["MonthlyCharges"] / (df["tenure"] + 1)

    df = pd.get_dummies(df, drop_first=True)

    df.to_csv(OUTPUT_PATH, index=False)
    print("Preprocessing done.")


if __name__ == "__main__":
    preprocess()
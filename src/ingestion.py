import pandas as pd
import os
from datetime import datetime

DATA_PATH = "data/historical_data.csv"
NEW_DATA_PATH = "data/new_data.csv"
LOG_PATH = "artifacts/ingestion_log.txt"


def ingest_new_data():
    # simulate new data (sample from historical)
    df = pd.read_csv(DATA_PATH)

    new_data = df.sample(10)

    # save new data
    new_data.to_csv(NEW_DATA_PATH, index=False)

    # append to historical
    updated_df = pd.concat([df, new_data], ignore_index=True)
    updated_df.to_csv(DATA_PATH, index=False)

    # log
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now()} - New data ingested: {len(new_data)} rows\n")

    print("New data ingested successfully!")


if __name__ == "__main__":
    ingest_new_data()
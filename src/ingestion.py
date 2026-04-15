import pandas as pd
import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/database.db")

historical = pd.read_sql("SELECT * FROM historical_data", conn)
new_data = pd.read_sql("SELECT * FROM new_data", conn)

updated = pd.concat([historical, new_data], ignore_index=True)

updated.to_sql("historical_data", conn, if_exists="replace", index=False)

with open("artifacts/ingestion_log.txt", "a") as f:
    f.write(f"Ingestion run at {datetime.now()}\n")

conn.close()

print("Ingestion completed.")
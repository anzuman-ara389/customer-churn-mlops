import os
import pandas as pd
import sqlite3

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/database.db")

historical = pd.read_csv("data/historical_data.csv")
new_data = pd.read_csv("data/new_data.csv")

historical.to_sql("historical_data", conn, if_exists="replace", index=False)
new_data.to_sql("new_data", conn, if_exists="replace", index=False)

conn.close()

print("Database initialized successfully.")
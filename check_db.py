import sqlite3

conn = sqlite3.connect("data/database.db")
cur = conn.cursor()

tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables:", tables)

historical_rows = cur.execute("SELECT COUNT(*) FROM historical_data").fetchone()[0]
new_rows = cur.execute("SELECT COUNT(*) FROM new_data").fetchone()[0]

print("Historical rows:", historical_rows)
print("New rows:", new_rows)

conn.close()

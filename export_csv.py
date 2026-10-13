import sqlite3
import pandas as pd

conn = sqlite3.connect("patients.db")
df = pd.read_sql_query(
    "SELECT * FROM patients ORDER BY PatientID",
    conn
)
conn.close()

df.to_csv("patients.csv", index=False, encoding="utf-8-sig")

print("Export completed. Number of patients:", len(df))
import pandas as pd
import sqlite3

# load dataset
data = pd.read_csv("data/jobs_cleaned.csv")

# connect to database
conn = sqlite3.connect("database/jobs.db")

# write table
data.to_sql("jobs", conn, if_exists="replace", index=False)

print("Database created and data inserted.")

conn.close()

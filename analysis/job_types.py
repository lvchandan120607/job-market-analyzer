import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("database/jobs.db")

query = """
SELECT job_type, COUNT(*) AS count
FROM jobs
GROUP BY job_type
ORDER BY count DESC
"""

df = pd.read_sql_query(query, conn)
conn.close()

plt.figure(figsize=(8,8))
plt.pie(df["count"], labels=df["job_type"], autopct="%1.1f%%")

plt.title("Job Type Distribution")

plt.savefig("charts/job_types.png")

print("Chart saved: charts/job_types.png")

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("database/jobs.db")

query = """
SELECT company_name, COUNT(*) AS count
FROM jobs
GROUP BY company_name
ORDER BY count DESC
LIMIT 10
"""

df = pd.read_sql_query(query, conn)
conn.close()

plt.figure(figsize=(10,6))
plt.bar(df["company_name"], df["count"])
plt.xticks(rotation=45, ha="right")
plt.title("Top Companies Hiring Data Roles")
plt.xlabel("Company")
plt.ylabel("Number of Listings")

plt.tight_layout()
plt.savefig("charts/top_companies.png")

print("Chart saved: charts/top_companies.png")

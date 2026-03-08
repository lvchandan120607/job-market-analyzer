import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# connect to database
conn = sqlite3.connect("database/jobs.db")

query = """
SELECT title, COUNT(*) AS count
FROM jobs
GROUP BY title
ORDER BY count DESC
LIMIT 10
"""

df = pd.read_sql_query(query, conn)

conn.close()

# create bar chart
plt.figure(figsize=(10,6))
plt.bar(df["title"], df["count"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Job Titles")
plt.xlabel("Job Title")
plt.ylabel("Number of Listings")

# save chart
plt.tight_layout()
plt.savefig("charts/top_job_titles.png")

print("Chart saved to charts/top_job_titles.png")

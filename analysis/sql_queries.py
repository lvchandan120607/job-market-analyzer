import sqlite3
import pandas as pd

conn = sqlite3.connect("database/jobs.db")

query = """
SELECT title, COUNT(*) AS count
FROM jobs
GROUP BY title
ORDER BY count DESC
LIMIT 10
"""

df = pd.read_sql_query(query, conn)

print("\nTop Job Titles:\n")
print(df)

conn.close()

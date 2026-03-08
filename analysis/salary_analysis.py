import pandas as pd
import matplotlib.pyplot as plt
import re

# load dataset
data = pd.read_csv("data/jobs.csv")

# function to extract numbers from salary text
def extract_salary(s):
    numbers = re.findall(r"\d+", str(s))
    if len(numbers) >= 2:
        return (int(numbers[0]) + int(numbers[1])) / 2
    elif len(numbers) == 1:
        return int(numbers[0])
    else:
        return None

# create numeric salary column
data["salary_numeric"] = data["salary"].apply(extract_salary)

# remove rows without salary
data = data.dropna(subset=["salary_numeric"])

# plot histogram
plt.figure(figsize=(10,6))
plt.hist(data["salary_numeric"], bins=20)

plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of Jobs")

plt.tight_layout()
plt.savefig("charts/salary_distribution.png")

print("Chart saved: charts/salary_distribution.png")

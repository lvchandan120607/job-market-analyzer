import pandas as pd

# load dataset
data = pd.read_csv("data/jobs.csv")

# show first rows
print("\nFirst 5 rows:\n")
print(data.head())

# show dataset information
print("\nDataset Info:\n")
print(data.info())

# show basic statistics
print("\nStatistics:\n")
print(data.describe())

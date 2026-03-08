kimport pandas as pd

df = pd.read_csv("data/jobs.csv")

# Standardize job types
def clean_job_type(x):
    x = str(x).lower()

    if "full" in x:
        return "Full-time"
    if "part" in x:
        return "Part-time"
    if "contract" in x:
        return "Contract"
    if "intern" in x:
        return "Internship"
    if "remote" in x:
        return "Remote"

    return "Other"

df["job_type"] = df["job_type"].apply(clean_job_type)

df.to_csv("data/jobs_cleaned.csv", index=False)

print("Clean dataset saved")

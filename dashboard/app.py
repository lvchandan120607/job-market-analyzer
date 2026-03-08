import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page config
st.set_page_config(page_title="Job Market Dashboard", layout="wide")

st.title("Job Market Analysis Dashboard")

# Database connection
conn = sqlite3.connect("database/jobs.db")
data = pd.read_sql_query("SELECT * FROM jobs", conn)

# -----------------------------
# KPI METRICS
# -----------------------------
total_jobs = len(data)
unique_companies = data["company_name"].nunique()
remote_jobs = data["job_type"].str.contains("remote", case=False, na=False).sum()

salary_df = data.copy()
salary_df["salary"] = salary_df["salary"].str.replace("£", "", regex=False)
salary_df["salary"] = salary_df["salary"].str.extract(r'(\d+)')
salary_df["salary"] = pd.to_numeric(salary_df["salary"], errors="coerce")

avg_salary = int(salary_df["salary"].mean()) if salary_df["salary"].notnull().any() else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", total_jobs)
col2.metric("Companies Hiring", unique_companies)
col3.metric("Remote Jobs", remote_jobs)
col4.metric("Avg Salary (£)", avg_salary)

st.markdown("---")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

job_type = st.sidebar.selectbox(
    "Job Type",
    ["All"] + sorted(data["job_type"].dropna().unique())
)

company = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(data["company_name"].dropna().unique())
)

filtered_data = data.copy()

if job_type != "All":
    filtered_data = filtered_data[filtered_data["job_type"] == job_type]

if company != "All":
    filtered_data = filtered_data[filtered_data["company_name"] == company]

# -----------------------------
# SALARY DISTRIBUTION
# -----------------------------
st.subheader("Salary Distribution")

salary_data = filtered_data.copy()
salary_data["salary"] = salary_data["salary"].str.replace("£", "", regex=False)
salary_data["salary"] = salary_data["salary"].str.extract(r'(\d+)')
salary_data["salary"] = pd.to_numeric(salary_data["salary"], errors="coerce")

fig_salary = px.histogram(
    salary_data,
    x="salary",
    nbins=20,
    title="Salary Distribution"
)

st.plotly_chart(fig_salary, use_container_width=True)

# -----------------------------
# DATASET PREVIEW
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_data.head())

# -----------------------------
# TOP JOB TITLES + COMPANIES
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Job Titles")

    titles = (
        filtered_data["title"]
        .value_counts()
        .reset_index()
    )

    titles.columns = ["title", "count"]

    fig_titles = px.bar(
        titles.head(10),
        x="title",
        y="count",
        title="Top Job Titles"
    )

    st.plotly_chart(fig_titles, use_container_width=True)

with col2:
    st.subheader("Top Companies Hiring")

    companies = (
        filtered_data["company_name"]
        .value_counts()
        .reset_index()
    )

    companies.columns = ["company", "count"]

    fig_companies = px.bar(
        companies.head(10),
        x="company",
        y="count",
        title="Top Hiring Companies"
    )

    st.plotly_chart(fig_companies, use_container_width=True)

# -----------------------------
# JOB TYPE DISTRIBUTION
# -----------------------------
st.subheader("Job Type Distribution")

job_types = (
    filtered_data["job_type"]
    .value_counts()
    .head(6)
    .reset_index()
)

job_types.columns = ["job_type", "count"]

fig_types = px.bar(
    job_types,
    x="job_type",
    y="count",
    title="Job Type Distribution"
)

st.plotly_chart(fig_types, use_container_width=True)

# -----------------------------
# SQL ANALYTICS PANEL
# -----------------------------
st.subheader("SQL Analytics")

query = st.text_area(
    "Run a SQL query on the jobs database",
    "SELECT title, company_name FROM jobs WHERE job_type='Remote' LIMIT 20"
)

if st.button("Run Query"):
    try:
        conn2 = sqlite3.connect("database/jobs.db")
        result = pd.read_sql_query(query, conn2)
        st.dataframe(result)
        conn2.close()
    except Exception as e:
        st.error(f"Query error: {e}")

conn.close()

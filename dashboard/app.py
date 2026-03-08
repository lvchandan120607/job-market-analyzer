import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Job Market Analyzer", layout="wide")

st.title("Job Market Analysis Dashboard")

# -----------------------------
# DATA SOURCE (UPLOAD OR DATABASE)
# -----------------------------

st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("Using uploaded dataset")
else:
    conn = sqlite3.connect("database/jobs.db")
    data = pd.read_sql_query("SELECT * FROM jobs", conn)
    st.info("Using default dataset")

# -----------------------------
# DATA PREPARATION
# -----------------------------

if "title" in data.columns:
    data = data.dropna(subset=["title"])

salary_df = data.copy()

if "salary" in salary_df.columns:
    salary_df["salary"] = salary_df["salary"].astype(str)
    salary_df["salary"] = salary_df["salary"].str.replace("£", "", regex=False)
    salary_df["salary"] = salary_df["salary"].str.extract(r'(\d+)')
    salary_df["salary"] = pd.to_numeric(salary_df["salary"], errors="coerce")

# -----------------------------
# KPI METRICS
# -----------------------------

total_jobs = len(data)
unique_companies = data["company_name"].nunique()

remote_jobs = data["job_type"].str.contains(
    "remote",
    case=False,
    na=False
).sum()

avg_salary = int(
    salary_df["salary"].mean()
) if salary_df["salary"].notnull().any() else 0

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
    filtered_data = filtered_data[
        filtered_data["job_type"] == job_type
    ]

if company != "All":
    filtered_data = filtered_data[
        filtered_data["company_name"] == company
    ]

# -----------------------------
# TABS
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Job Analysis",
    "Salary Insights",
    "SQL Analytics"
])

# -----------------------------
# TAB 1 : OVERVIEW
# -----------------------------

with tab1:

    st.header("Market Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Jobs", total_jobs)
    col2.metric("Companies Hiring", unique_companies)
    col3.metric("Remote Jobs", remote_jobs)
    col4.metric("Average Salary", avg_salary)

    st.subheader("Dataset Preview")
    st.dataframe(filtered_data.head())

# -----------------------------
# TAB 2 : JOB ANALYSIS
# -----------------------------

with tab2:

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
        color="count",
        title="Most In-Demand Job Titles"
    )

    st.plotly_chart(fig_titles, use_container_width=True)

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
        color="count",
        title="Top Hiring Companies"
    )

    st.plotly_chart(fig_companies, use_container_width=True)

# -----------------------------
# TAB 3 : SALARY INSIGHTS
# -----------------------------

with tab3:

    st.subheader("Salary Distribution")

    fig_salary = px.histogram(
        salary_df,
        x="salary",
        nbins=25,
        color_discrete_sequence=["#3366cc"]
    )

    st.plotly_chart(fig_salary, use_container_width=True)

# -----------------------------
# TAB 4 : SQL ANALYTICS
# -----------------------------

with tab4:

    st.subheader("Run SQL Queries")

    query = st.text_area(
        "Run SQL query on the jobs database",
        "SELECT * FROM jobs LIMIT 10"
    )

    if st.button("Run Query"):

        try:
            conn2 = sqlite3.connect("database/jobs.db")

            result = pd.read_sql_query(query, conn2)

            st.dataframe(result)

            conn2.close()

        except Exception as e:
            st.error(f"Query error: {e}")

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Job Market Analyzer", layout="wide")

st.title("Job Market Analysis Dashboard")

# -----------------------------
# DATA SOURCE
# -----------------------------
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("Using uploaded dataset")
else:
    conn = sqlite3.connect("database/jobs.db")
    data = pd.read_sql_query("SELECT * FROM jobs", conn)
    st.info("Using default dataset")

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
data.columns = data.columns.str.lower().str.strip()

# -----------------------------
# COLUMN DETECTION
# -----------------------------
title_col = None
company_col = None
jobtype_col = None
salary_col = None

for col in data.columns:
    if "title" in col:
        title_col = col
    if "company" in col:
        company_col = col
    if "type" in col or "location" in col:
        jobtype_col = col
    if "salary" in col:
        salary_col = col

# -----------------------------
# DATA PREP
# -----------------------------
if title_col:
    data = data.dropna(subset=[title_col])

salary_df = data.copy()

if salary_col:
    salary_df[salary_col] = salary_df[salary_col].astype(str)
    salary_df[salary_col] = salary_df[salary_col].str.replace("£", "", regex=False)
    salary_df[salary_col] = salary_df[salary_col].str.extract(r'(\d+)')
    salary_df[salary_col] = pd.to_numeric(salary_df[salary_col], errors="coerce")

# -----------------------------
# KPIs
# -----------------------------
total_jobs = len(data)

unique_companies = (
    data[company_col].nunique() if company_col else 0
)

remote_jobs = (
    data[jobtype_col]
    .str.contains("remote", case=False, na=False)
    .sum() if jobtype_col else 0
)

avg_salary = (
    int(salary_df[salary_col].mean())
    if salary_col and salary_df[salary_col].notnull().any()
    else 0
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

filtered_data = data.copy()

if jobtype_col:
    jobtype_options = ["All"] + sorted(data[jobtype_col].dropna().unique())
    selected_jobtype = st.sidebar.selectbox("Job Type", jobtype_options)

    if selected_jobtype != "All":
        filtered_data = filtered_data[
            filtered_data[jobtype_col] == selected_jobtype
        ]

if company_col:
    company_options = ["All"] + sorted(data[company_col].dropna().unique())
    selected_company = st.sidebar.selectbox("Company", company_options)

    if selected_company != "All":
        filtered_data = filtered_data[
            filtered_data[company_col] == selected_company
        ]

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Job Analysis", "Salary Insights", "SQL Analytics"]
)

# -----------------------------
# TAB 1
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
# TAB 2
# -----------------------------
with tab2:

    if title_col:

        titles = (
            filtered_data[title_col]
            .value_counts()
            .reset_index()
        )

        titles.columns = ["title", "count"]

        fig_titles = px.bar(
            titles.head(10),
            x="title",
            y="count",
            title="Most In-Demand Job Titles",
            color="count"
        )

        st.plotly_chart(fig_titles, use_container_width=True)

    if company_col:

        companies = (
            filtered_data[company_col]
            .value_counts()
            .reset_index()
        )

        companies.columns = ["company", "count"]

        fig_companies = px.bar(
            companies.head(10),
            x="company",
            y="count",
            title="Top Hiring Companies",
            color="count"
        )

        st.plotly_chart(fig_companies, use_container_width=True)

# -----------------------------
# TAB 3
# -----------------------------
with tab3:

    if salary_col:

        st.subheader("Salary Distribution")

        fig_salary = px.histogram(
            salary_df,
            x=salary_col,
            nbins=25,
            title="Salary Distribution"
        )

        st.plotly_chart(fig_salary, use_container_width=True)

# -----------------------------
# TAB 4
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

import streamlit as st
import pandas as pd
from data_manager import apply_filters, load_initial_data, init_data
from utils import load_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

h1 {
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Data Explorer")

# ---------------- DATA ----------------
df= init_data()
df = apply_filters()

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", int(df.isna().sum().sum()))

# ---------------- OUTLIER DETECTION ----------------
if "Lead Time" in df.columns:
    q1 = df["Lead Time"].quantile(0.25)
    q3 = df["Lead Time"].quantile(0.75)
    iqr = q3 - q1

    outliers = df[
        (df["Lead Time"] < q1 - 1.5 * iqr) |
        (df["Lead Time"] > q3 + 1.5 * iqr)
    ]

    col4.metric("Outliers", outliers.shape[0])
else:
    col4.metric("Outliers", "N/A")

st.markdown("---")

# ---------------- SEARCH ----------------
search = st.text_input("🔎 Search data")

if search:
    filtered_df = df[
        df.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(),
            axis=1
        )
    ]
else:
    filtered_df = df

# ---------------- DATA QUALITY FLAGS ----------------
st.subheader("⚠️ Data Quality Check")

issues = []

if "Lead Time" in df.columns:
    if (df["Lead Time"] < 0).sum() > 0:
        issues.append("Negative Lead Time values found")

    if (df["Lead Time"] > 1000).sum() > 0:
        issues.append("Extreme Lead Time values (>1000 days) found")

if df.isna().sum().sum() > 0:
    issues.append("Missing values present in dataset")

if issues:
    for issue in issues:
        st.error("🚨 " + issue)
else:
    st.success("✅ No major data issues detected")

# ---------------- PREVIEW ----------------
st.subheader("📊 Data Preview")

rows = st.slider("Rows to display", 5, 100, 20)

st.dataframe(filtered_df.head(rows), use_container_width=True)

# ---------------- OUTLIER VIEW ----------------
if "Lead Time" in df.columns and not outliers.empty:
    with st.expander("🚨 View Outlier Records (Anomalies)"):
        st.dataframe(outliers, use_container_width=True)

# ---------------- FULL VIEW ----------------
with st.expander("🔽 View Full Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# ---------------- DOWNLOAD ----------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
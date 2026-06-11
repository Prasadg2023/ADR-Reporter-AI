import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_reports
from utils import generate_report_pdf
import os

st.set_page_config(page_title="Owner Dashboard", page_icon="📊", layout="wide")

st.title("📊 Owner Dashboard")

# --- FETCH DATA ---
@st.cache_data(ttl=60)
def load_data():
    reports = get_all_reports()
    if not reports:
        return pd.DataFrame()
    df = pd.DataFrame(reports)
    # Convert dates to datetime objects for easy filtering
    if 'submission_timestamp' in df.columns:
        df['submission_timestamp'] = pd.to_datetime(df['submission_timestamp'])
    return df

df = load_data()

if df.empty:
    st.info("No reports found in the database. Please submit a report first.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Reports")

# Date Filter
min_date = df['submission_timestamp'].min().date() if not df.empty else None
max_date = df['submission_timestamp'].max().date() if not df.empty else None
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# Category Filter
categories = ["All"] + list(df['final_drug_category'].dropna().unique())
selected_category = st.sidebar.selectbox("Drug Category", categories)

# Gender Filter
genders = ["All"] + list(df['gender'].dropna().unique())
selected_gender = st.sidebar.selectbox("Gender", genders)

# Apply Filters
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['submission_timestamp'].dt.date >= start_date) & 
        (filtered_df['submission_timestamp'].dt.date <= end_date)
    ]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['final_drug_category'] == selected_category]
    
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

# --- METRICS ---
st.markdown("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Reports", len(df))
col2.metric("Filtered Reports", len(filtered_df))
col3.metric("Top Category", filtered_df['final_drug_category'].mode()[0] if not filtered_df.empty else "N/A")

# --- CHARTS ---
st.markdown("### Analytics")
c1, c2 = st.columns(2)

with c1:
    if not filtered_df.empty:
        cat_counts = filtered_df['final_drug_category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig1 = px.pie(cat_counts, names='Category', values='Count', title="Drug Category Distribution")
        st.plotly_chart(fig1, use_container_width=True)

with c2:
    if not filtered_df.empty:
        gender_counts = filtered_df['gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig2 = px.bar(gender_counts, x='Gender', y='Count', title="Gender Split")
        st.plotly_chart(fig2, use_container_width=True)

# Monthly Trend
if not filtered_df.empty:
    trend_df = filtered_df.copy()
    trend_df['MonthYear'] = trend_df['submission_timestamp'].dt.to_period('M').astype(str)
    trend_counts = trend_df.groupby('MonthYear').size().reset_index(name='Count')
    fig3 = px.line(trend_counts, x='MonthYear', y='Count', markers=True, title="Monthly Trend of Reports")
    st.plotly_chart(fig3, use_container_width=True)

# --- DATA TABLE & EXPORTS ---
st.markdown("### Detailed Reports")

# Display the table
st.dataframe(filtered_df.drop(columns=['report_id'], errors='ignore'))

# Export CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name='adr_reports.csv',
    mime='text/csv',
)

# Export PDF for a single report
st.markdown("### Export Individual Report (PDF)")
if not filtered_df.empty:
    report_to_export = st.selectbox("Select Report to Export as PDF (by ID)", filtered_df['report_id'])
    
    if st.button("Generate PDF"):
        # Get specific report data
        report_data = filtered_df[filtered_df['report_id'] == report_to_export].iloc[0].to_dict()
        try:
            pdf_path = generate_report_pdf(report_data)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label=f"📥 Download Report {report_to_export} PDF",
                    data=pdf_file,
                    file_name=f"ADR_Report_{report_to_export}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")

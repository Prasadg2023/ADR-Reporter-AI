import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_reports
from utils import generate_report_pdf
import os
import base64

st.set_page_config(page_title="Owner Dashboard", page_icon="📊", layout="wide")

# --- BASE64 IMAGE LOADER ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                data = image_file.read()
                return base64.b64encode(data).decode()
    except Exception:
        pass
    return ""

bg_base64 = get_base64_image("assets/adr_config_background.png")

# Premium glassmorphism styles matching the dark clinical theme
css = f"""
<style>
/* Glassmorphism theme with blurred background image */
.stApp::before {{
    content: "";
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    filter: blur(8px) brightness(0.6);
    z-index: -1;
}}

.stApp {{
    background: transparent !important;
    font-family: 'Inter', 'Outfit', 'Segoe UI', sans-serif;
}}

/* Custom glassmorphism card for components */
.glass-card {{
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}}

h1, h2, h3 {{
    color: #00f2fe !important;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
    font-weight: 700 !important;
}}

p, li, label, span, .stMarkdown p {{
    color: #e2e8f0 !important;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(10, 15, 30, 0.9) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("📊 Owner Dashboard")

def style_plotly_fig(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family="'Inter', sans-serif"),
        title_font=dict(color='#00f2fe', size=16),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.05)',
        zerolinecolor='rgba(255,255,255,0.1)',
        tickfont=dict(color='#cbd5e1')
    )
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.05)',
        zerolinecolor='rgba(255,255,255,0.1)',
        tickfont=dict(color='#cbd5e1')
    )
    return fig


# --- FETCH DATA ---
@st.cache_data(ttl=60)
def load_data():
    reports = get_all_reports()
    if not reports:
        return pd.DataFrame()
    df = pd.DataFrame(reports)
    # Convert dates to datetime objects for easy filtering
    if 'submission_timestamp' in df.columns:
        df['submission_timestamp'] = pd.to_datetime(df['submission_timestamp'], format='mixed', errors='coerce')
    
    # Sort by report_id in ascending order
    if 'report_id' in df.columns:
        df = df.sort_values(by='report_id', ascending=True)
    
    # Standardize and clean category names for display/filtering
    if 'final_drug_category' in df.columns:
        category_map = {
            "nsaid": "NSAIDs",
            "nsaid / analgesic": "NSAIDs",
            "nsaid/analgesic": "NSAIDs",
            "nsaids": "NSAIDs",
            "antibiotic": "Antibiotics",
            "antibiotics": "Antibiotics",
            "antiallergic / antihistamine": "Antihistamines",
            "antiallergic/antihistamine": "Antihistamines",
            "antihistamine": "Antihistamines",
            "antihistamines": "Antihistamines",
            "antidiabetic": "Antidiabetics",
            "antidiabetics": "Antidiabetics",
            "antihypertensive": "Antihypertensives",
            "antihypertensives": "Antihypertensives",
            "antipyretic": "Antipyretics",
            "antipyretics": "Antipyretics",
            "beta-blocker": "Beta-blockers",
            "beta-blockers": "Beta-blockers",
            "betabloker": "Beta-blockers",
            "betablocker": "Beta-blockers",
            "calcium channel blocker": "Calcium Channel Blockers",
            "calcium channel blockers": "Calcium Channel Blockers",
            "ace inhibitor": "ACE Inhibitors",
            "ace inhibitors": "ACE Inhibitors",
            "angiotensin receptor blocker (arbs)": "Angiotensin Receptor Blockers (ARBs)",
            "angiotensin receptor blockers": "Angiotensin Receptor Blockers (ARBs)",
            "arb": "Angiotensin Receptor Blockers (ARBs)",
            "arbs": "Angiotensin Receptor Blockers (ARBs)",
            "diuretic": "Diuretics",
            "diuretics": "Diuretics",
            "statin": "Statins / Lipid-lowering Drugs",
            "statins": "Statins / Lipid-lowering Drugs",
            "statin / lipid-lowering drugs": "Statins / Lipid-lowering Drugs",
            "statin/lipid-lowering drugs": "Statins / Lipid-lowering Drugs",
            "statins / lipid-lowering drugs": "Statins / Lipid-lowering Drugs",
            "statins/lipid-lowering drugs": "Statins / Lipid-lowering Drugs",
            "benzodiazepine": "Benzodiazepines",
            "benzodiazepines": "Benzodiazepines",
            "other": "Others",
            "others": "Others"
        }
        df['final_drug_category'] = df['final_drug_category'].apply(
            lambda x: category_map.get(str(x).lower().strip(), str(x)) if pd.notna(x) else "Others (Low Confidence)"
        )
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
        fig1 = px.pie(
            cat_counts, 
            names='Category', 
            values='Count', 
            title="Drug Category Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        style_plotly_fig(fig1)
        st.plotly_chart(fig1, use_container_width=True)

with c2:
    if not filtered_df.empty:
        gender_counts = filtered_df['gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig2 = px.bar(
            gender_counts, 
            x='Gender', 
            y='Count', 
            title="Gender Split",
            color='Gender',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        style_plotly_fig(fig2)
        fig2.update_yaxes(dtick=1)
        st.plotly_chart(fig2, use_container_width=True)

# Monthly Trend
if not filtered_df.empty:
    # 1. Clean and standardize the date column by creating a copy of the dataframe
    trend_df = filtered_df.copy()
    
    # 2. Convert mixed-format dates with proper error handling (coerce invalid to NaT)
    trend_df['ParsedDate'] = pd.to_datetime(trend_df['submission_timestamp'], format='mixed', errors='coerce')
    
    # 3. Remove invalid dates (NaT)
    trend_df = trend_df.dropna(subset=['ParsedDate'])
    
    if not trend_df.empty:
        # Group records by Month-Year chronologically
        trend_df['YearMonthKey'] = trend_df['ParsedDate'].dt.to_period('M')
        
        # Determine chronological bounds to ensure the x-axis displays all months in the range
        min_period = trend_df['YearMonthKey'].min()
        max_period = trend_df['YearMonthKey'].max()
        all_months = pd.period_range(start=min_period, end=max_period, freq='M')
        
        # 4. Group by month and reindex to include intermediate months with zero counts
        trend_counts = trend_df.groupby('YearMonthKey').size()
        trend_counts = trend_counts.reindex(all_months, fill_value=0).reset_index()
        trend_counts.columns = ['YearMonthKey', 'Count']
        
        # Convert Period to string representation (YYYY-MM) for plotting
        trend_counts['MonthYear'] = trend_counts['YearMonthKey'].astype(str)
        
        # 5. Create a Plotly area chart showing the monthly trend of reports
        fig3 = px.area(
            trend_counts, 
            x='MonthYear', 
            y='Count', 
            markers=True, 
            title="Monthly Trend of Reports",
            labels={'MonthYear': 'Month-Year', 'Count': 'Number of Reports'}
        )
        
        # 6. Apply styled visual elements matching the glassmorphic dark theme
        fig3.update_traces(
            line=dict(color='#00f2fe', width=3), 
            fillcolor='rgba(0, 242, 254, 0.15)',
            marker=dict(size=10, color='#7f00ff', symbol='circle', line=dict(color='#ffffff', width=2))
        )
        
        # Ensure x-axis is categorical to display all labels clearly and chronologically
        fig3.update_xaxes(type='category')
        
        # Force integer-only steps on the Y-axis since report count is discrete
        fig3.update_yaxes(dtick=1)
        
        # Apply unified transparent chart styling helper
        style_plotly_fig(fig3)
        
        # Display with st.plotly_chart
        st.plotly_chart(fig3, use_container_width=True)

# --- DATA TABLE & EXPORTS ---
st.markdown("### Detailed Reports")

# Display the table with report_id visible and index hidden
st.dataframe(filtered_df, hide_index=True)

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
    
    # Get specific report data
    report_data = filtered_df[filtered_df['report_id'] == report_to_export].iloc[0].to_dict()
    try:
        pdf_path = generate_report_pdf(report_data)
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        st.download_button(
            label=f"📥 Download Report {report_to_export} PDF",
            data=pdf_bytes,
            file_name=f"ADR_Report_{report_to_export}.pdf",
            mime="application/pdf",
            key=f"download_pdf_{report_to_export}"
        )
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")

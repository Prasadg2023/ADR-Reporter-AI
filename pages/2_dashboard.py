import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_reports, get_report_pdf, delete_report
from utils import generate_report_pdf, render_common_sidebar
from translations import TRANSLATIONS
import os
import base64

if "language" not in st.session_state or not st.session_state.language:
    st.session_state.language = "English"

lang = st.session_state.language

st.set_page_config(page_title=TRANSLATIONS[lang]["dash_title"], page_icon="📊", layout="wide")

# Render common sidebar
render_common_sidebar("dashboard")

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

st.title(TRANSLATIONS[lang]["dash_title"])

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
    st.info(TRANSLATIONS[lang]["dash_error_no_reports"])
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header(TRANSLATIONS[lang]["dash_filter_header"])

# Date Filter
min_date = df['submission_timestamp'].min().date() if not df.empty else None
max_date = df['submission_timestamp'].max().date() if not df.empty else None
date_range = st.sidebar.date_input(TRANSLATIONS[lang]["dash_filter_date"], [min_date, max_date])

# Category Filter
categories = [TRANSLATIONS[lang]["dash_filter_all"]] + list(df['final_drug_category'].dropna().unique())
selected_category = st.sidebar.selectbox(TRANSLATIONS[lang]["dash_filter_category"], categories)

# Gender Filter
genders = [TRANSLATIONS[lang]["dash_filter_all"]] + list(df['gender'].dropna().unique())
selected_gender = st.sidebar.selectbox(TRANSLATIONS[lang]["dash_filter_gender"], genders)

# Apply Filters
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['submission_timestamp'].dt.date >= start_date) & 
        (filtered_df['submission_timestamp'].dt.date <= end_date)
    ]

if selected_category != TRANSLATIONS[lang]["dash_filter_all"]:
    filtered_df = filtered_df[filtered_df['final_drug_category'] == selected_category]
    
if selected_gender != TRANSLATIONS[lang]["dash_filter_all"]:
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

# --- METRICS ---
st.markdown(TRANSLATIONS[lang]["dash_metrics_header"])
col1, col2, col3 = st.columns(3)
col1.metric(TRANSLATIONS[lang]["dash_metric_total"], len(df))
col2.metric(TRANSLATIONS[lang]["dash_metric_filtered"], len(filtered_df))
col3.metric(TRANSLATIONS[lang]["dash_metric_top_category"], filtered_df['final_drug_category'].mode()[0] if not filtered_df.empty else "N/A")

# --- CHARTS ---
st.markdown(TRANSLATIONS[lang]["dash_analytics_header"])
c1, c2 = st.columns(2)

with c1:
    if not filtered_df.empty:
        cat_counts = filtered_df['final_drug_category'].value_counts().reset_index()
        cat_counts.columns = [TRANSLATIONS[lang]['dash_chart_pie_cat'], TRANSLATIONS[lang]['dash_chart_pie_count']]
        fig1 = px.pie(
            cat_counts, 
            names=TRANSLATIONS[lang]['dash_chart_pie_cat'], 
            values=TRANSLATIONS[lang]['dash_chart_pie_count'], 
            title=TRANSLATIONS[lang]["dash_chart_pie_title"],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        style_plotly_fig(fig1)
        st.plotly_chart(fig1, use_container_width=True)

with c2:
    if not filtered_df.empty:
        gender_counts = filtered_df['gender'].value_counts().reset_index()
        gender_counts.columns = [TRANSLATIONS[lang]['dash_chart_bar_gender'], TRANSLATIONS[lang]['dash_chart_bar_count']]
        fig2 = px.bar(
            gender_counts, 
            x=TRANSLATIONS[lang]['dash_chart_bar_gender'], 
            y=TRANSLATIONS[lang]['dash_chart_bar_count'], 
            title=TRANSLATIONS[lang]["dash_chart_bar_title"],
            color=TRANSLATIONS[lang]['dash_chart_bar_gender'],
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
            title=TRANSLATIONS[lang]["dash_chart_trend_title"],
            labels={'MonthYear': TRANSLATIONS[lang]['dash_chart_trend_x'], 'Count': TRANSLATIONS[lang]['dash_chart_trend_y']}
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
st.markdown(TRANSLATIONS[lang]["dash_detailed_header"])

# Rename columns for localized display
rename_dict = {}
for col in filtered_df.columns:
    translation_key = f"col_{col}"
    if translation_key in TRANSLATIONS[lang]:
        rename_dict[col] = TRANSLATIONS[lang][translation_key]
display_df = filtered_df.rename(columns=rename_dict)

# Display the table with report_id visible and index hidden
st.dataframe(display_df, hide_index=True)

# Export CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=TRANSLATIONS[lang]["dash_btn_download_csv"],
    data=csv,
    file_name='adr_reports.csv',
    mime='text/csv',
)

# Export PDF for a single report
st.markdown(TRANSLATIONS[lang]["dash_export_header"])
if not filtered_df.empty:
    report_to_export = st.selectbox(TRANSLATIONS[lang]["dash_export_select"], filtered_df['report_id'])
    
    try:
        pdf_bytes = get_report_pdf(report_to_export)
        
        if pdf_bytes:
            # Download Button
            st.download_button(
                label=TRANSLATIONS[lang]["dash_btn_download_pdf"].format(id=report_to_export),
                data=pdf_bytes,
                file_name=f"ADR_Report_{report_to_export}.pdf",
                mime="application/pdf",
                key=f"download_pdf_{report_to_export}"
            )
            
            # View PDF Inline Preview
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
            with st.expander(TRANSLATIONS[lang]["dash_view_pdf_expander"]):
                st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.error(TRANSLATIONS[lang]["dash_error_pdf_failed"])
    except Exception as e:
        st.error(TRANSLATIONS[lang]["dash_error_pdf_gen_failed"].format(error=e))

# --- ADMINISTRATOR PANEL ---
st.markdown(TRANSLATIONS[lang]["dash_admin_header"])
with st.expander(TRANSLATIONS[lang]["dash_admin_expander"]):
    # Check for admin credentials (default to "admin")
    ADMIN_PASSWORD = "admin"
    if hasattr(st, "secrets") and "admin" in st.secrets:
        ADMIN_PASSWORD = st.secrets["admin"].get("password", ADMIN_PASSWORD)
        
    admin_password = st.text_input(TRANSLATIONS[lang]["dash_admin_password_label"], type="password", key="admin_pwd")
    
    if admin_password == ADMIN_PASSWORD:
        st.success(TRANSLATIONS[lang]["dash_admin_auth_success"])
        
        report_ids = df['report_id'].tolist() if not df.empty else []
        if report_ids:
            report_to_delete = st.selectbox(TRANSLATIONS[lang]["dash_admin_select_delete"], report_ids, key="delete_report_id")
            
            # Checkbox to prevent accidental deletions
            confirm = st.checkbox(TRANSLATIONS[lang]["dash_admin_confirm_checkbox"].format(id=report_to_delete), key="confirm_delete")
            
            if st.button(TRANSLATIONS[lang]["dash_admin_btn_delete"], type="primary", use_container_width=True):
                if confirm:
                    if delete_report(report_to_delete):
                        st.success(TRANSLATIONS[lang]["dash_admin_delete_success"].format(id=report_to_delete))
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(TRANSLATIONS[lang]["dash_admin_delete_failed"])
                else:
                    st.warning(TRANSLATIONS[lang]["dash_admin_confirm_warning"])
        else:
            st.info(TRANSLATIONS[lang]["dash_admin_no_reports"])
    elif admin_password != "":
        st.error(TRANSLATIONS[lang]["dash_admin_auth_failed"])

import streamlit as st
from database import init_db

# Initialize database on app startup
try:
    init_db()
except Exception as e:
    st.error(f"Failed to initialize database: {e}")

st.set_page_config(
    page_title="ADR Reporter AI",
    page_icon="💊",
    layout="centered"
)

st.title("💊 ADR Reporter AI Hub")

st.markdown("""
Welcome to the **Adverse Drug Reaction (ADR) Reporter AI** system.

Please use the sidebar on the left to navigate:
- **📝 Patient Reporter:** A conversational interface for patients to report adverse drug reactions step-by-step.
- **📊 Owner Dashboard:** A comprehensive dashboard for administrators to analyze and export the collected reports.
""")

st.info("Database initialized successfully. If you haven't yet, ensure your MySQL server (e.g. XAMPP) is running.")

import streamlit as st
import base64
import os
from database import init_db
from translations import APP_TEXTS, NAV_TEXTS

# Initialize database on app startup
try:
    init_db()
except Exception as e:
    st.error(f"Failed to initialize database: {e}")

# Initialize session state language before set_page_config
if "language" not in st.session_state:
    st.session_state.language = "English"

lang = st.session_state.language

st.set_page_config(
    page_title=APP_TEXTS[lang]["page_title"],
    page_icon="💊",
    layout="centered"
)

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

# Load background image
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

/* Custom glassmorphism card for welcome message and instructions */
.glass-card {{
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 30px;
    margin-top: 20px;
    margin-bottom: 25px;
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
}}

/* Style headers and main texts for clinical neon glowing theme */
h1, h2, h3 {{
    color: #00f2fe !important;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
    font-weight: 700 !important;
}}

p, li, label, span, .stMarkdown p {{
    color: #e2e8f0 !important;
    font-size: 1.05rem !important;
    line-height: 1.6 !important;
}}

/* Make sidebar match the theme */
[data-testid="stSidebar"] {{
    background-color: rgba(10, 15, 30, 0.9) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}}

/* Info alert box custom styling */
.stAlert {{
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    border-radius: 12px !important;
}}

/* Hide default Streamlit sidebar page links */
[data-testid="stSidebarNav"] {{
    display: none !important;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- GLOBAL SIDEBAR NAVIGATION & LANGUAGE SELECTOR ---
nav_data = NAV_TEXTS.get(lang, NAV_TEXTS["English"])
st.sidebar.markdown(f"### {nav_data['nav_title']}")

# Language selectbox
languages = ["English", "Hindi", "Marathi"]
lang_display = {
    "English": "English",
    "Hindi": "हिंदी (Hindi)",
    "Marathi": "मराठी (Marathi)"
}
curr_idx = languages.index(lang) if lang in languages else 0
selected_lang = st.sidebar.selectbox(
    nav_data["select_lang"],
    options=languages,
    format_func=lambda x: lang_display[x],
    index=curr_idx,
    key="global_language_selector"
)

if selected_lang != lang:
    st.session_state.language = selected_lang
    st.rerun()

# Sidebar Navigation buttons
if st.sidebar.button(nav_data["home"], use_container_width=True):
    st.switch_page("app.py")
if st.sidebar.button(nav_data["patient_assessment"], use_container_width=True):
    st.switch_page("pages/1_patient_reporter.py")
if st.sidebar.button(nav_data["dashboard"], use_container_width=True):
    st.switch_page("pages/2_dashboard.py")

st.title(APP_TEXTS[lang]["title"])

st.markdown(f"""
<div class="glass-card">
    <h3>{APP_TEXTS[lang]["welcome_hdr"]}</h3>
    <p>{APP_TEXTS[lang]["welcome_desc"]}</p>
    <hr style="border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 20px 0;">
    <p>{APP_TEXTS[lang]["sidebar_prompt"]}</p>
    <ul style="padding-left: 20px; margin-bottom: 10px;">
        <li style="margin-bottom: 10px;">
            {APP_TEXTS[lang]["li_reporter"]}
        </li>
        <li style="margin-bottom: 10px;">
            {APP_TEXTS[lang]["li_dashboard"]}
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.info(APP_TEXTS[lang]["db_success"])


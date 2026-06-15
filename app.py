import streamlit as st
import base64
import os
from database import init_db
from utils import render_common_sidebar
from translations import TRANSLATIONS

# Ensure language is initialized in session state
if "language" not in st.session_state or not st.session_state.language:
    st.session_state.language = "English"

# Render the sidebar navigation
render_common_sidebar("home")

lang = st.session_state.language

st.set_page_config(
    page_title=TRANSLATIONS[lang]["app_title"],
    page_icon="💊",
    layout="centered"
)

# Initialize database on app startup
try:
    init_db()
    db_initialized = True
except Exception as e:
    db_initialized = False
    st.error(TRANSLATIONS[lang]["app_db_error"].format(error=e))

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
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title(TRANSLATIONS[lang]["app_title"])

st.markdown(f"""
<div class="glass-card">
    <h3>{TRANSLATIONS[lang]["app_welcome_heading"]}</h3>
    <p>{TRANSLATIONS[lang]["app_welcome_subtext"]}</p>
    <hr style="border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 20px 0;">
    <p>{TRANSLATIONS[lang]["app_welcome_instruction"]}</p>
    <ul style="padding-left: 20px; margin-bottom: 10px;">
        <li style="margin-bottom: 10px;">
            {TRANSLATIONS[lang]["app_desc_reporter"]}
        </li>
        <li style="margin-bottom: 10px;">
            {TRANSLATIONS[lang]["app_desc_dashboard"]}
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

if db_initialized:
    st.info(TRANSLATIONS[lang]["app_db_success"])


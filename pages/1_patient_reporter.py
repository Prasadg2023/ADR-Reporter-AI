import streamlit as st
import json
import time
import pandas as pd
import requests
import urllib.parse
import base64
import os
import io
try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

try:
    import speech_recognition as sr
    HAS_SPEECH_RECOGNITION = True
except ImportError:
    HAS_SPEECH_RECOGNITION = False

from database import insert_report
from utils import detect_drug_category
from translations import QUESTIONS, REPORTER_UI_TEXTS as UI_TEXTS, LANG_CODES, NAV_TEXTS

# --- SESSION STATE INITIALIZATION ---
if "flow_state" not in st.session_state:
    st.session_state.flow_state = "language_selection" # language_selection, chatting, summary, completed
if "language" not in st.session_state:
    st.session_state.language = "English"

lang = st.session_state.language

@st.cache_data(show_spinner=False)
def get_question_audio(text, lang_name):
    if not HAS_GTTS:
        return None
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Marathi": "mr"
    }
    lang_code = lang_map.get(lang_name, "en")
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

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

st.set_page_config(page_title=UI_TEXTS[lang]["welcome_title"], page_icon="🗣️", layout="centered")

# --- CUSTOM GLASSMORPHISM STYLES & BACKGROUND ---
bg_base64 = get_base64_image("assets/pharma_background.png")

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
    filter: blur(10px) brightness(0.65);
    z-index: -1;
}}

.stApp {{
    background: transparent !important;
}}

/* Custom glassmorphism card for instructions and widgets */
.glass-card {{
    background: rgba(17, 25, 40, 0.7);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.125);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}}

/* Custom styling for chat bubbles */
[data-testid="stChatMessage"] {{
    background: rgba(17, 25, 40, 0.75) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    padding: 15px !important;
    margin-bottom: 12px !important;
}}

/* Style headers and main texts for dark background visibility */
h1, h2, h3, p, li, label, span, .stMarkdown p {{
    color: #ffffff !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.6);
}}

/* Make sidebar match the theme */
[data-testid="stSidebar"] {{
    background-color: rgba(10, 15, 30, 0.9) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}}

/* Table styling for glass look */
.stTable, div[data-testid="stTable"] table {{
    background: rgba(10, 15, 30, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px;
    overflow: hidden;
    color: white !important;
}}

/* Streamlit chat input glass styling */
[data-testid="stChatInput"] textarea {{
    background: rgba(17, 25, 40, 0.85) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}}

/* Primary Buttons styling */
.stButton button {{
    background: linear-gradient(135deg, #1b3a4b, #219ebc) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 15px rgba(33, 158, 188, 0.3) !important;
    transition: all 0.3s ease !important;
    font-weight: bold !important;
}}

.stButton button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(33, 158, 188, 0.5) !important;
}}

/* Hide default Streamlit sidebar page links */
[data-testid="stSidebarNav"] {{
    display: none !important;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "answers_original" not in st.session_state:
    st.session_state.answers_original = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "auto_category" not in st.session_state:
    st.session_state.auto_category = "Others"

# --- PROGRESS PERSISTENCE SETUP ---
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adr_reports_progress.json")

def save_progress():
    progress_data = {
        "language": st.session_state.language,
        "current_q_index": st.session_state.current_q_index,
        "answers": st.session_state.answers,
        "answers_original": st.session_state.answers_original,
        "chat_history": st.session_state.chat_history,
        "auto_category": st.session_state.auto_category
    }
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

# Check and prompt to resume incomplete assessment if found
if st.session_state.flow_state == "language_selection" and os.path.exists(PROGRESS_FILE):
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown(UI_TEXTS[lang]["resume_title"])
    st.markdown(UI_TEXTS[lang]["resume_msg"], unsafe_allow_html=True)
    
    col_resume, col_new = st.columns(2)
    with col_resume:
        if st.button(UI_TEXTS[lang]["btn_resume_yes"], use_container_width=True, type="primary"):
            try:
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    progress_data = json.load(f)
                st.session_state.language = progress_data.get("language")
                lang = st.session_state.language
                st.session_state.current_q_index = progress_data.get("current_q_index", 0)
                st.session_state.answers = progress_data.get("answers", {})
                st.session_state.answers_original = progress_data.get("answers_original", {})
                st.session_state.auto_category = progress_data.get("auto_category", "Others")
                st.session_state.flow_state = "chatting"
                rebuild_chat_history()
                st.rerun()
            except Exception as e:
                st.error(UI_TEXTS[lang]["resume_err"].format(e=e))
                
    with col_new:
        if st.button(UI_TEXTS[lang]["btn_resume_no"], use_container_width=True):
            try:
                os.remove(PROGRESS_FILE)
            except Exception:
                pass
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- HELPER FUNCTIONS ---
def add_msg(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def rebuild_chat_history():
    st.session_state.chat_history = []
    lang_name = st.session_state.language
    if not lang_name:
        return
    st.session_state.chat_history.append({"role": "assistant", "content": UI_TEXTS[lang_name]["welcome_msg"]})
    st.session_state.chat_history.append({"role": "assistant", "content": QUESTIONS[0]["text"][lang_name]})
    
    for i in range(st.session_state.current_q_index):
        q = QUESTIONS[i]
        if q["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
            continue
        if q["key"] == "physician_contact" and st.session_state.answers.get("physician_name") in ["None", "Unknown"]:
            continue
            
        orig = st.session_state.answers_original.get(q["key"])
        trans = st.session_state.answers.get(q["key"])
        if orig is None:
            continue
            
        st.session_state.chat_history.append({"role": "user", "content": orig})
        
        label_text = q["label"].get(lang_name, q["label"]["English"])
        if trans != orig and trans.lower() != orig.lower():
            display_val = f"{orig} (English: {trans})"
        else:
            display_val = orig
        conf_msg = f"**{i + 1}. {label_text}**\n{UI_TEXTS[lang_name]['you_said']}: {display_val}\n{UI_TEXTS[lang_name]['recorded']}"
        st.session_state.chat_history.append({"role": "assistant", "content": conf_msg})
        
        if q["key"] == "drug_name":
            detected = st.session_state.auto_category
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": UI_TEXTS[lang_name]["detected_category"].format(detected=detected)
            })
            
        next_i = i + 1
        if next_i < len(QUESTIONS) and QUESTIONS[next_i]["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
            next_i += 1
        if next_i < len(QUESTIONS) and QUESTIONS[next_i]["key"] == "physician_contact" and st.session_state.answers.get("physician_name") in ["None", "Unknown"]:
            next_i += 1
            
        if next_i < len(QUESTIONS) and next_i <= st.session_state.current_q_index:
            st.session_state.chat_history.append({"role": "assistant", "content": QUESTIONS[next_i]["text"][lang_name]})

def translate_to_english(text):
    if not text:
        return ""
    try:
        text.encode('ascii')
        return text
    except UnicodeEncodeError:
        pass
    
    try:
        q = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={q}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            res = r.json()
            parts = [item[0] for item in res[0] if item[0]]
            return "".join(parts).strip()
    except Exception:
        pass
    return text

def normalize_devanagari_numbers(text):
    devanagari_to_english = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    for d, e in devanagari_to_english.items():
        text = text.replace(d, e)
    return text

def normalize_email(text):
    text_lower = text.lower().strip()
    text_lower = text_lower.replace(" at the rate ", "@")
    text_lower = text_lower.replace(" at the rateof ", "@")
    text_lower = text_lower.replace(" at the rate of ", "@")
    text_lower = text_lower.replace(" at rate ", "@")
    text_lower = text_lower.replace(" at ", "@")
    text_lower = text_lower.replace(" dot ", ".")
    text_lower = text_lower.replace(" point ", ".")
    text_lower = text_lower.replace(" ", "")
    if text_lower.endswith("."):
        text_lower = text_lower[:-1]
    return text_lower

def normalize_mobile(text):
    text_clean = text.replace(" ", "").strip()
    text_clean = "".join([c for c in text_clean if c.isdigit() or c == '+'])
    return text_clean

TRANSLITERATED_MAPPING = {
    # Symptoms / Reactions
    "dokedukhi": "headache",
    "doke dukhi": "headache",
    "doke dukhne": "headache",
    "dokedukhane": "headache",
    "taap": "fever",
    "tap": "fever",
    "khokla": "cough",
    "khokala": "cough",
    "sardi": "cold",
    "shardi": "cold",
    "pitt": "acidity",
    "pitta": "acidity",
    "ulteea": "vomiting",
    "ultya": "vomiting",
    "ulti": "vomiting",
    "ultia": "vomiting",
    "ulta": "vomiting",
    "chakkar": "dizziness",
    "chakar": "dizziness",
    "angduki": "body pain",
    "ang dukhi": "body pain",
    "khaj": "itching",
    "khand": "itching",
    "purad": "skin rash",
    "puraad": "skin rash",
    "thandi": "shivering",
    "potduki": "stomach ache",
    "pot dukhi": "stomach ache",
    "potat dukhi": "stomach ache",
    "chatidukhi": "chest pain",
    "chaati dukhne": "chest pain",
    "ghasa dukhne": "sore throat",
    "gala kharab": "sore throat",
    "shwas ghenyala tras": "shortness of breath",
    "ashaktpana": "weakness",
    
    # Common Whatsapp chat connecting words (Marathi / Hindi)
    "ahe": "have / is",
    "aahe": "have / is",
    "hota": "was",
    "hoti": "was",
    "hote": "was",
    "mhanun": "so",
    "sobat": "with",
    "natar": "after",
    "nantar": "after",
    "purvi": "before",
    "keli": "did",
    "kela": "did",
    "band": "stopped",
    "bandh": "stopped",
    "chalu": "ongoing",
    "nahi": "not",
    "nahis": "not",
    "pan": "but",
    "tras": "trouble",
    "bharpur": "high",
    "khup": "very",
    "dava": "medicine",
    "goli": "tablet",
    "aushadh": "medicine",
    "aushadhi": "medicine",
    "ghetli": "took",
    "ghetla": "took",
    "mhanje": "means",
    "bhiti": "fear"
}

def translate_transliterated_marathi_hindi(text):
    if not text:
        return ""
    text_lower = text.lower().strip()
    
    sorted_keys = sorted(TRANSLITERATED_MAPPING.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in text_lower:
            val = TRANSLITERATED_MAPPING[key]
            text_lower = text_lower.replace(key, val)
            
    return text_lower

def map_negative_or_skip(val):
    val_lower = val.strip().lower()
    skips = [
        "skip", "skp", "स्किप", "छोड़ें", "छोड़े", "वगळा", "नका",
        "not sure", "i don't know", "dont know", "not available", "unknown",
        "पता नहीं", "मालूम नहीं", "निश्चित नहीं", "माहित नाही", "नक्की नाही", "माहिती नाही"
    ]
    no_terms = ["no", "none", "नहीं", "नही", "नाही", "नको"]
    still_taking_terms = ["still taking", "अभी भी ले रहे हैं", "अजूनही घेत आहे"]
    still_ongoing_terms = ["still ongoing", "ongoing", "अभी भी जारी है", "अजूनही सुरू आहे"]
    
    if any(term in val_lower for term in skips):
        return "Unknown"
    if any(term in val_lower for term in no_terms):
        return "None"
    if any(term in val_lower for term in still_taking_terms):
        return "still taking"
    if any(term in val_lower for term in still_ongoing_terms):
        return "still ongoing"
    
    return val

def map_gender(val_translated, val_original):
    val_l = val_original.lower().strip()
    val_t_l = val_translated.lower().strip()
    
    males = ["male", "m", "पुरुष", "नर"]
    females = ["female", "f", "महिला", "स्त्री", "मादा"]
    others = ["other", "o", "अन्य", "इतर", "तीसरा", "तिसरा"]
    
    if any(term == val_l or term == val_t_l for term in males):
        return "Male"
    if any(term == val_l or term == val_t_l for term in females):
        return "Female"
    if any(term == val_l or term == val_t_l for term in others):
        return "Other"
    
    return val_translated.title()

# --- PYTHON SPEECH RECOGNITION TRANSCRIBER ---
def transcribe_audio(audio_file, language_code):
    if not HAS_SPEECH_RECOGNITION:
        err_msg = {
            "en-US": "Error: Speech recognition library is not available on this server.",
            "hi-IN": "त्रुटि: स्पीच रिकग्निशन लाइब्रेरी इस सर्वर पर उपलब्ध नहीं है।",
            "mr-IN": "त्रुटी: स्पीच रिकग्निशन लायब्ररी या सर्व्हरवर उपलब्ध नाही."
        }
        return err_msg.get(language_code, err_msg["en-US"])
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language=language_code)
            return text.strip()
    except sr.UnknownValueError:
        err_msg = {
            "en-US": "Error: Could not understand audio.",
            "hi-IN": "त्रुटि: आवाज समझ में नहीं आया।",
            "mr-IN": "त्रुटी: आवाज समजला नाही."
        }
        return err_msg.get(language_code, err_msg["en-US"])
    except sr.RequestError as e:
        err_msg = {
            "en-US": f"Error: Request failed; {e}",
            "hi-IN": f"त्रुटि: अनुरोध विफल रहा; {e}",
            "mr-IN": f"त्रुटी: विनंती अयशस्वी झाली; {e}"
        }
        return err_msg.get(language_code, err_msg["en-US"])
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI RENDER ---
lang = st.session_state.language if st.session_state.language else "English"

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
    rebuild_chat_history()
    st.rerun()

# Sidebar Navigation buttons
if st.sidebar.button(nav_data["home"], use_container_width=True):
    st.switch_page("app.py")
if st.sidebar.button(nav_data["patient_assessment"], use_container_width=True):
    st.switch_page("pages/1_patient_reporter.py")
if st.sidebar.button(nav_data["dashboard"], use_container_width=True):
    st.switch_page("pages/2_dashboard.py")

# Sidebar options for quitting assessment and navigation
if st.session_state.flow_state in ["chatting", "summary"]:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {UI_TEXTS[lang]['options_hdr']}")
    if st.session_state.flow_state == "chatting" and st.session_state.current_q_index > 0:
        if st.sidebar.button(UI_TEXTS[lang]["btn_prev"], use_container_width=True, key="btn_prev_sidebar"):
            st.session_state.current_q_index -= 1
            while st.session_state.current_q_index > 0:
                prev_q = QUESTIONS[st.session_state.current_q_index]
                if prev_q["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
                    st.session_state.current_q_index -= 1
                elif prev_q["key"] == "physician_contact" and st.session_state.answers.get("physician_name") in ["None", "Unknown"]:
                    st.session_state.current_q_index -= 1
                else:
                    break
            rebuild_chat_history()
            save_progress()
            st.rerun()
    if st.sidebar.button(UI_TEXTS[lang]["btn_quit"], use_container_width=True, key="btn_quit_sidebar"):
        st.session_state.confirm_quit = True
        st.rerun()

# Confirm Quit Assessment Dialog
if st.session_state.get("confirm_quit", False):
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown(UI_TEXTS[lang]["quit_confirm_title"])
    st.markdown(UI_TEXTS[lang]["quit_confirm_msg"], unsafe_allow_html=True)
    
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button(UI_TEXTS[lang]["btn_quit_yes"], use_container_width=True, type="primary"):
            save_progress()
            st.session_state.clear()
            st.rerun()
    with col_no:
        if st.button(UI_TEXTS[lang]["btn_quit_no"], use_container_width=True):
            st.session_state.confirm_quit = False
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Display Pharmacist Avatar photo and title layout
st.markdown('<div class="glass-card" style="padding: 15px; margin-bottom: 25px;">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("assets/pharmacist_avatar.png"):
        st.image("assets/pharmacist_avatar.png", use_container_width=True)
with col2:
    st.title(UI_TEXTS[lang]["welcome_title"])
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.flow_state == "language_selection":
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown(UI_TEXTS[lang]["lang_selection_title"])
    st.markdown(UI_TEXTS[lang]["lang_selection_msg"], unsafe_allow_html=True)
    
    cols = st.columns(3)
    if cols[0].button("English", use_container_width=True, key="btn_lang_en"):
        st.session_state.language = "English"
    if cols[1].button("Hindi / हिंदी", use_container_width=True, key="btn_lang_hi"):
        st.session_state.language = "Hindi"
    if cols[2].button("Marathi / मराठी", use_container_width=True, key="btn_lang_mr"):
        st.session_state.language = "Marathi"
        
    if st.session_state.language:
        lang = st.session_state.language
        # Start Chat
        st.session_state.flow_state = "chatting"
        rebuild_chat_history()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.flow_state == "chatting":
    
    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Input Processing
    q_index = st.session_state.current_q_index
    
    # Speak the current question aloud
    if q_index < len(QUESTIONS):
        current_q = QUESTIONS[q_index]
        # Skip voice output if the question is auto-skipped
        if not (current_q["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)"):
            question_text = current_q["text"][lang]
            audio_bytes = get_question_audio(question_text, lang)
            if audio_bytes:
                if "last_played_q_index" not in st.session_state or st.session_state.last_played_q_index != q_index:
                    autoplay = True
                    st.session_state.last_played_q_index = q_index
                else:
                    autoplay = False
                st.audio(audio_bytes, format="audio/mp3", autoplay=autoplay)
                
    user_input = None
    
    if q_index < len(QUESTIONS):
        current_q = QUESTIONS[q_index]
        
        # Fallback check: skip manual category question if category detection succeeded
        if current_q["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
            st.session_state.answers["drug_category_manual"] = "Unknown"
            st.session_state.answers_original["drug_category_manual"] = "Unknown"
            st.session_state.current_q_index += 1
            st.rerun()
            
        label_text = current_q["label"].get(lang, current_q["label"]["English"])
        lang_code = LANG_CODES.get(lang, "en-US")
        
        # Display current answer if already answered (when patient went back)
        is_answered = current_q["key"] in st.session_state.answers
        if is_answered:
            current_ans = st.session_state.answers_original.get(current_q["key"], "")
            st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(UI_TEXTS[lang]["inline_current_response"].format(label_text=label_text, current_ans=current_ans))
            
            edited_val = st.text_input(
                UI_TEXTS[lang]["inline_edit_label"],
                value=current_ans,
                key=f"inline_edit_{q_index}"
            )
            
            col_save, col_next = st.columns(2)
            with col_save:
                if st.button(UI_TEXTS[lang]["btn_save_changes"], use_container_width=True, type="primary", key=f"btn_save_inline_{q_index}"):
                    user_input = edited_val
            with col_next:
                if st.button(UI_TEXTS[lang]["btn_next_question"], use_container_width=True, key=f"btn_next_inline_{q_index}"):
                    if current_q["key"] == "physician_name" and st.session_state.answers.get("physician_name") in ["None", "Unknown"]:
                        st.session_state.current_q_index += 2
                    else:
                        st.session_state.current_q_index += 1
                    save_progress()
                    rebuild_chat_history()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Main Page 'Previous Question' button for easy navigation
        if q_index > 0:
            if st.button(UI_TEXTS[lang]["btn_prev"], key=f"btn_prev_main_{q_index}", use_container_width=True):
                st.session_state.current_q_index -= 1
                while st.session_state.current_q_index > 0:
                    prev_q = QUESTIONS[st.session_state.current_q_index]
                    if prev_q["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
                        st.session_state.current_q_index -= 1
                    elif prev_q["key"] == "physician_contact" and st.session_state.answers.get("physician_name") in ["None", "Unknown"]:
                        st.session_state.current_q_index -= 1
                    else:
                        break
                rebuild_chat_history()
                save_progress()
                st.rerun()

        # Render voice input and chat input
        if HAS_SPEECH_RECOGNITION:
            rec_title = UI_TEXTS[lang]["voice_record_title"].format(label_text=label_text)
            if is_answered:
                rec_title = UI_TEXTS[lang]["voice_record_replace"]
            st.markdown(f"#### {rec_title}")
            audio_file = st.audio_input(UI_TEXTS[lang]["audio_input_label"], key=f"audio_input_{q_index}")
        else:
            st.info(UI_TEXTS[lang]["voice_disabled_info"])
            audio_file = None
        
        placeholder = UI_TEXTS[lang]["input_placeholder"].format(label=label_text)
        chat_val = st.chat_input(placeholder)
        
        # Process voice recording input
        if audio_file:
            with st.spinner(UI_TEXTS[lang]["voice_spinner"]):
                speech_text = transcribe_audio(audio_file, lang_code)
                if speech_text.startswith("Error:") or speech_text.startswith("त्रुटि:") or speech_text.startswith("त्रुटी:"):
                    st.error(speech_text)
                else:
                    user_input = speech_text
                    
        # Process keyboard text input
        if chat_val:
            user_input = chat_val
        
        if user_input:
            # Process and record answer
            val_original = user_input.strip()
            val_normalized = normalize_devanagari_numbers(val_original)
            
            # Normalize email and mobile formats if spoken
            if current_q["key"] == "patient_email":
                val_normalized = normalize_email(val_normalized)
                val_original = val_normalized
            elif current_q["key"] == "patient_mobile":
                val_normalized = normalize_mobile(val_normalized)
                val_original = val_normalized
                
            # Translate transliterated Marathi/Hindi symptoms (like "dokedukhi") to English
            val_normalized = translate_transliterated_marathi_hindi(val_normalized)
            
            val_translated = translate_to_english(val_normalized)
            
            # Map skip / no values
            val_mapped = map_negative_or_skip(val_original)
            if val_mapped in ["Unknown", "None"]:
                val_translated = val_mapped
            
            # Specific mappings per key
            if current_q["key"] == "gender":
                val_translated = map_gender(val_translated, val_original)
            
            # Special check for physician contact logic
            if current_q["key"] == "physician_name" and val_translated in ["None", "Unknown"]:
                st.session_state.answers["physician_name"] = "None"
                st.session_state.answers["physician_contact"] = "N/A"
                st.session_state.answers_original["physician_name"] = val_original
                st.session_state.answers_original["physician_contact"] = "N/A"
                st.session_state.current_q_index += 2 # Skip next question
            else:
                st.session_state.answers[current_q["key"]] = val_translated
                st.session_state.answers_original[current_q["key"]] = val_original
                st.session_state.current_q_index += 1
            
            # Auto-detect drug logic (Question 7: drug_name)
            if current_q["key"] == "drug_name":
                detected = detect_drug_category(val_translated)
                st.session_state.auto_category = detected
                
            # Next Question or Summary
            next_q_index = st.session_state.current_q_index
            if next_q_index < len(QUESTIONS):
                next_q = QUESTIONS[next_q_index]
                # CATEGORY DETECTION RULE:
                if next_q["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
                    st.session_state.answers["drug_category_manual"] = "Unknown"
                    st.session_state.answers_original["drug_category_manual"] = "Unknown"
                    st.session_state.current_q_index += 1
                    next_q_index = st.session_state.current_q_index
                    
            if next_q_index >= len(QUESTIONS):
                st.session_state.flow_state = "summary"
            
            rebuild_chat_history()
            save_progress()
            st.rerun()
            
elif st.session_state.flow_state == "summary":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.success(UI_TEXTS[lang]["summary_success"])
    
    # Finalize Category
    manual_cat = st.session_state.answers.get("drug_category_manual", "Unknown")
    final_cat = st.session_state.auto_category if manual_cat == "Unknown" else manual_cat
    st.session_state.answers["final_drug_category"] = final_cat

    # Display Table showing original answer and translation
    summary_data = []
    for q in QUESTIONS:
        key = q["key"]
        label = q["label"].get(lang, q["label"]["English"])
        orig = st.session_state.answers_original.get(key, "")
        trans = st.session_state.answers.get(key, "")
        summary_data.append({
            UI_TEXTS[lang]["field_col"]: label,
            UI_TEXTS[lang]["answer_col"]: orig,
            UI_TEXTS[lang]["english_col"]: trans
        })
    
    # Add final_drug_category
    cat_label = {
        "English": "Final Drug Category",
        "Hindi": "अंतिम दवा श्रेणी",
        "Marathi": "अंतिम औषध वर्ग"
    }.get(lang, "Final Drug Category")
    summary_data.append({
        UI_TEXTS[lang]["field_col"]: cat_label,
        UI_TEXTS[lang]["answer_col"]: st.session_state.answers["final_drug_category"],
        UI_TEXTS[lang]["english_col"]: st.session_state.answers["final_drug_category"]
    })
    
    df = pd.DataFrame(summary_data)
    df.index = range(1, len(df) + 1)
    st.table(df)
    
    # Summary editing expander
    with st.expander(UI_TEXTS[lang]["edit_expander"]):
        edit_options = [q["label"].get(lang, q["label"]["English"]) for q in QUESTIONS]
        selected_edit_label = st.selectbox(UI_TEXTS[lang]["edit_select_field"], edit_options, key="select_edit_field")
        
        # Find corresponding question key
        selected_q = next(q for q in QUESTIONS if q["label"].get(lang, q["label"]["English"]) == selected_edit_label)
        key = selected_q["key"]
        
        current_val_orig = st.session_state.answers_original.get(key, "")
        new_val_orig = st.text_input(UI_TEXTS[lang]["edit_new_response"].format(selected_edit_label=selected_edit_label), value=current_val_orig, key=f"edit_input_{key}")
        
        if st.button(UI_TEXTS[lang]["btn_save_changes"], use_container_width=True, key=f"save_edit_{key}"):
            st.session_state.answers_original[key] = new_val_orig
            
            # Translate to English
            val_normalized = normalize_devanagari_numbers(new_val_orig)
            if key == "patient_email":
                val_normalized = normalize_email(val_normalized)
            elif key == "patient_mobile":
                val_normalized = normalize_mobile(val_normalized)
            val_normalized = translate_transliterated_marathi_hindi(val_normalized)
            val_translated = translate_to_english(val_normalized)
            
            # Map skip / no values
            val_mapped = map_negative_or_skip(new_val_orig)
            if val_mapped in ["Unknown", "None"]:
                val_translated = val_mapped
                
            if key == "gender":
                val_translated = map_gender(val_translated, new_val_orig)
                
            st.session_state.answers[key] = val_translated
            
            # Auto-detect category if drug name changed
            if key == "drug_name":
                st.session_state.auto_category = detect_drug_category(val_translated)
                
            # Re-finalize drug category in case it changed
            manual_cat = st.session_state.answers.get("drug_category_manual", "Unknown")
            final_cat = st.session_state.auto_category if manual_cat == "Unknown" else manual_cat
            st.session_state.answers["final_drug_category"] = final_cat
            
            save_progress()
            st.success(UI_TEXTS[lang]["edit_success"].format(selected_edit_label=selected_edit_label))
            st.rerun()
            
    col_sub, col_rest = st.columns(2)
    with col_sub:
        if st.button(UI_TEXTS[lang]["btn_submit"], type="primary", use_container_width=True):
            # Save to DB
            success = insert_report(st.session_state.answers)
            if success:
                # Delete progress file on successful final submission
                if os.path.exists(PROGRESS_FILE):
                    try:
                        os.remove(PROGRESS_FILE)
                    except Exception:
                        pass
                st.session_state.flow_state = "completed"
                st.rerun()
            else:
                st.error(UI_TEXTS[lang]["db_save_err"])
    with col_rest:
        if st.button(UI_TEXTS[lang]["btn_restart"], use_container_width=True):
            # Delete progress file
            if os.path.exists(PROGRESS_FILE):
                try:
                    os.remove(PROGRESS_FILE)
                except Exception:
                    pass
            st.session_state.clear()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.flow_state == "completed":
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.balloons()
    st.image("assets/pharmacist_avatar.png", width=120)
    st.success(UI_TEXTS[lang]["report_success"])
    if st.button(UI_TEXTS[lang]["btn_new"], use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

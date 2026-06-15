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

@st.cache_data(show_spinner=False)
def get_question_audio(text, lang):
    if not HAS_GTTS:
        return None
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Marathi": "mr"
    }
    lang_code = lang_map.get(lang, "en")
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

st.set_page_config(page_title="Patient Reporter", page_icon="🗣️", layout="centered")

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

</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- DATA STRUCTURES (Multilingual) ---
QUESTIONS = [
    {
        "key": "patient_name",
        "label": {"English": "Patient Name", "Hindi": "मरीज का नाम", "Marathi": "रुग्णाचे नाव"},
        "text": {
            "English": "Please tell me the patient's full name.",
            "Hindi": "कृपया मरीज का पूरा नाम बताएं।",
            "Marathi": "कृपया रुग्णाचे पूर्ण नाव सांगा."
        }
    },
    {
        "key": "patient_email",
        "label": {"English": "Email Address", "Hindi": "ईमेल पता", "Marathi": "ईमेल पत्ता"},
        "text": {
            "English": "What is the patient's email address? (Type 'skip' if not available)",
            "Hindi": "मरीज का ईमेल पता क्या है? (यदि उपलब्ध न हो तो 'skip' लिखें)",
            "Marathi": "रुग्णाचा ईमेल पत्ता काय आहे? (उपलब्ध नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "patient_mobile",
        "label": {"English": "Mobile Number", "Hindi": "मोबाइल नंबर", "Marathi": "मोबाईल नंबर"},
        "text": {
            "English": "What is the patient's mobile number? (Type 'skip' if not available)",
            "Hindi": "मरीज का मोबाइल नंबर क्या है? (यदि उपलब्ध न हो तो 'skip' लिखें)",
            "Marathi": "रुग्णाचा मोबाईल नंबर काय आहे? (उपलब्ध नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "age",
        "label": {"English": "Age", "Hindi": "उम्र", "Marathi": "वय"},
        "text": {
            "English": "How old is the patient?",
            "Hindi": "मरीज की उम्र कितनी है?",
            "Marathi": "रुग्णाचे वय किती आहे?"
        }
    },
    {
        "key": "gender",
        "label": {"English": "Gender", "Hindi": "लिंग", "Marathi": "लिंग"},
        "text": {
            "English": "What is the patient's gender? (Male / Female / Other)",
            "Hindi": "मरीज का लिंग क्या है? (पुरुष / महिला / अन्य)",
            "Marathi": "रुग्णाचे लिंग काय आहे? (पुरुष / महिला / इतर)"
        }
    },
    {
        "key": "weight_kg",
        "label": {"English": "Weight (kg)", "Hindi": "वजन (किग्रा)", "Marathi": "वजन (किग्रॅ)"},
        "text": {
            "English": "What is the patient's weight in kilograms? (Type 'skip' if not available)",
            "Hindi": "मरीज का वजन किलोग्राम में कितना है? (यदि उपलब्ध न हो तो 'skip' लिखें)",
            "Marathi": "रुग्णाचे वजन किलोग्राममध्ये किती आहे? (उपलब्ध नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "drug_name",
        "label": {"English": "Drug Name", "Hindi": "दवा का नाम", "Marathi": "औषधाचे नाव"},
        "text": {
            "English": "Which drug or medicine caused the reaction? Please type the name.",
            "Hindi": "किस दवा के कारण रिएक्शन हुआ? कृपया नाम लिखें।",
            "Marathi": "कोणत्या औषधामुळे ही रिएक्शन झाली? कृपया नाव लिहा."
        }
    },
    {
        "key": "indication",
        "label": {"English": "Reason for Medicine", "Hindi": "दवा लेने का कारण", "Marathi": "औषध घेण्याचे कारण"},
        "text": {
            "English": "What was this medicine being used to treat? (What was the reason or indication for taking it?)",
            "Hindi": "इस दवा का उपयोग किस बीमारी के इलाज के लिए किया जा रहा था? (इसे लेने का कारण क्या था?)",
            "Marathi": "हे औषध कोणत्या आजाराच्या उपचारासाठी वापरले जात होते? (ते घेण्याचे कारण काय होते?)"
        }
    },
    {
        "key": "medicine_start_date",
        "label": {"English": "Medicine Start Date", "Hindi": "दवा शुरू करने की तिथि", "Marathi": "औषध सुरू केल्याची तारीख"},
        "text": {
            "English": "When did the patient start taking this medicine? (e.g. DD/MM/YYYY)",
            "Hindi": "मरीज ने यह दवा लेना कब शुरू किया था? (जैसे DD/MM/YYYY)",
            "Marathi": "रुग्णाने हे औषध घेणे कधी सुरू केले? (उदा. DD/MM/YYYY)"
        }
    },
    {
        "key": "medicine_stop_date",
        "label": {"English": "Medicine Stop Date", "Hindi": "दवा बंद करने की तिथि", "Marathi": "औषध बंद केल्याची तारीख"},
        "text": {
            "English": "When did the patient stop taking this medicine? (Type 'still taking' if applicable)",
            "Hindi": "मरीज ने यह दवा लेना कब बंद किया? (यदि अभी भी ले रहे हैं तो 'still taking' लिखें)",
            "Marathi": "रुग्णाने हे औषध घेणे कधी बंद केले? (अजूनही घेत असल्यास 'still taking' लिहा)"
        }
    },
    {
        "key": "reaction_start_date",
        "label": {"English": "Reaction Start Date", "Hindi": "रिएक्शन शुरू होने की तिथि", "Marathi": "रिएक्शन सुरू झाल्याची तारीख"},
        "text": {
            "English": "When did the reaction or side effect start?",
            "Hindi": "रिएक्शन या दुष्प्रभाव कब शुरू हुआ था?",
            "Marathi": "रिएक्शन किंवा दुष्परिणाम कधी सुरू झाला?"
        }
    },
    {
        "key": "reaction_end_date",
        "label": {"English": "Reaction End Date", "Hindi": "रिएक्शन समाप्त होने की तिथि", "Marathi": "रिएक्शन संपल्याची तारीख"},
        "text": {
            "English": "When did the reaction stop or resolve? (Type 'still ongoing' if applicable)",
            "Hindi": "रिएक्शन कब बंद या ठीक हुआ? (यदि अभी भी जारी है तो 'still ongoing' लिखें)",
            "Marathi": "रिएक्शन कधी थांबली किंवा बरी झाली? (अजूनही सुरू असल्यास 'still ongoing' लिहा)"
        }
    },
    {
        "key": "reaction_description",
        "label": {"English": "Reaction Description", "Hindi": "रिएक्शन का विवरण", "Marathi": "रिएक्शनचे वर्णन"},
        "text": {
            "English": "Please describe the reaction or side effect in your own words. What exactly happened?",
            "Hindi": "कृपया अपने शब्दों में रिएक्शन या दुष्प्रभाव का वर्णन करें। वास्तव में क्या हुआ था?",
            "Marathi": "कृपया तुमच्या शब्दांत रिएक्शन किंवा दुष्परिणामाचे वर्णन करा. नक्की काय घडले?"
        }
    },
    {
        "key": "drug_category_manual",
        "label": {"English": "Drug Category", "Hindi": "दवा की श्रेणी", "Marathi": "औषधाचा वर्ग"},
        "text": {
            "English": "Do you know the category of this medicine? (e.g., Antibiotic, NSAID, Antiallergic. Type 'skip' to use auto-detected)",
            "Hindi": "क्या आप इस दवा की श्रेणी जानते हैं? (जैसे: एंटीबायोटिक, दर्दनिवारक, एलर्जी की दवा। स्वतः पहचान के लिए 'skip' लिखें)",
            "Marathi": "तुम्हाला या औषधाचा वर्ग माहिती आहे का? (उदा. अँटीबायोटिक, पेनकिलर, अँटी-अॅलर्जिक. ऑटो-डिटेक्ट वापरण्यासाठी 'skip' लिहा)"
        }
    },
    {
        "key": "route_of_administration",
        "label": {"English": "Route", "Hindi": "दवा लेने का मार्ग", "Marathi": "औषध घेण्याचा मार्ग"},
        "text": {
            "English": "How was this medicine taken? (e.g., by mouth, injection, skin patch)",
            "Hindi": "यह दवा कैसे ली गई थी? (जैसे: मुंह से, इंजेक्शन, त्वचा पैच द्वारा)",
            "Marathi": "हे औषध कसे घेतले गेले? (उदा. तोंडाद्वारे, इंजेक्शन, त्वचेवरील पॅच)"
        }
    },
    {
        "key": "strength",
        "label": {"English": "Strength", "Hindi": "दवा की क्षमता (डोज)", "Marathi": "औषधाची क्षमता (डोस)"},
        "text": {
            "English": "What was the strength or dose of the medicine? (e.g., 500mg, 10mg. Type 'skip' if not known)",
            "Hindi": "दवा की खुराक या क्षमता क्या थी? (जैसे: 500mg, 10mg। न पता होने पर 'skip' लिखें)",
            "Marathi": "औषधाचा डोस किंवा क्षमता काय होती? (उदा. 500mg, 10mg. माहिती नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "frequency",
        "label": {"English": "Frequency", "Hindi": "दवा लेने की आवृत्ति", "Marathi": "औषध घेण्याची वारंवारता"},
        "text": {
            "English": "How often was the medicine taken? (e.g., once a day, twice a day. Type 'skip' if not known)",
            "Hindi": "दवा कितनी बार ली जाती थी? (जैसे: दिन में एक बार, दिन में दो बार। न पता होने पर 'skip' लिखें)",
            "Marathi": "औषध किती वेळा घेतले जात होते? (उदा. दिवसातून एकदा, दिवसातून दोनदा. माहिती नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "batch_number",
        "label": {"English": "Batch Number", "Hindi": "बैच संख्या", "Marathi": "बॅच नंबर"},
        "text": {
            "English": "Do you have the batch number of the medicine? (Type 'skip' if not available)",
            "Hindi": "क्या आपके पास दवा का बैच नंबर है? (उपलब्ध न होने पर 'skip' लिखें)",
            "Marathi": "तुमच्याकडे औषधाचा बॅच नंबर आहे का? (उपलब्ध नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "expiry_date",
        "label": {"English": "Expiry Date", "Hindi": "एक्सपायरी डेट", "Marathi": "एक्सपायरी तारीख"},
        "text": {
            "English": "What is the expiry date on the medicine package? (Type 'skip' if not available)",
            "Hindi": "दवा के पैकेट पर एक्सपायरी डेट क्या है? (उपलब्ध न होने पर 'skip' लिखें)",
            "Marathi": "औषधाच्या पॅकेटवर कालबाह्यता तारीख (एक्सपायरी डेट) काय आहे? (उपलब्ध नसल्यास 'skip' लिहा)"
        }
    },
    {
        "key": "action_taken",
        "label": {"English": "Action Taken", "Hindi": "की गई कार्रवाई", "Marathi": "केलेली कारवाई"},
        "text": {
            "English": "What action was taken after the reaction? (e.g., medicine stopped, dose reduced, no action)",
            "Hindi": "रिएक्शन के बाद क्या कार्रवाई की गई? (जैसे: दवा बंद कर दी गई, खुराक कम कर दी गई, कोई कार्रवाई नहीं की गई)",
            "Marathi": "रिएक्शननंतर काय उपाययोजना केली गेली? (उदा. औषध बंद केले, डोस कमी केला, कोणतीही कारवाई केली नाही)"
        }
    },
    {
        "key": "physician_name",
        "label": {"English": "Physician Name", "Hindi": "चिकित्सक का नाम", "Marathi": "डॉक्टरांचे नाव"},
        "text": {
            "English": "Is there any doctor or physician associated with this treatment? (Type 'no' or 'not sure' if skip)",
            "Hindi": "क्या इस इलाज से जुड़ा कोई डॉक्टर या चिकित्सक है? (छोड़ने के लिए 'no' या 'not sure' लिखें)",
            "Marathi": "या उपचाराशी संबंधित कोणताही डॉक्टर किंवा चिकित्सक आहे का? (वगळण्यासाठी 'no' किंवा 'not sure' लिहा)"
        }
    },
    {
        "key": "physician_contact",
        "label": {"English": "Physician Contact", "Hindi": "चिकित्सक का संपर्क", "Marathi": "डॉक्टरांचा संपर्क"},
        "text": {
            "English": "What is the contact number or email of the physician? (Type 'skip' if not available)",
            "Hindi": "चिकित्सक का संपर्क नंबर या ईमेल क्या है? (उपलब्ध न होने पर 'skip' लिखें)",
            "Marathi": "डॉक्टरांचा संपर्क क्रमांक किंवा ईमेल काय आहे? (उपलब्ध नसल्यास 'skip' लिहा)"
        }
    }
]

UI_TEXTS = {
    "English": {
        "welcome_title": "🗣️ Patient Reporter AI",
        "tip_voice": "🎙️ *Tip: Record your voice using the widget below, or type your answer in the chat input.*",
        "welcome_msg": "Hello! I am ADR Reporter AI. I will help you report an adverse drug reaction (a side effect from a medicine). I will ask you 22 simple questions. You can speak or type. Let us begin.",
        "input_placeholder": "Your answer to: {label}...",
        "recorded": "✅ Recorded",
        "detected_category": "💡 Detected category: **{detected}**",
        "summary_success": "You have answered all questions. Please review your report below.",
        "field_col": "Field",
        "answer_col": "Your Answer",
        "english_col": "English Translation",
        "btn_submit": "Submit Report",
        "btn_restart": "Restart/Edit (Clears all data)",
        "report_success": "Report Submitted Successfully! Thank you.",
        "btn_new": "Start New Report",
        "you_said": "You said"
    },
    "Hindi": {
        "welcome_title": "🗣️ पेशेंट रिपोर्टर AI (मरीज रिपोर्टर)",
        "tip_voice": "🎙️ *सुझाव: नीचे दिए गए वॉयस रिकॉर्डर का उपयोग करें, या चैट इनपुट में अपना उत्तर टाइप करें।*",
        "welcome_msg": "नमस्ते! मैं ADR रिपोर्टर AI हूँ। मैं दवा के प्रतिकूल प्रभाव (साइड इफेक्ट) की रिपोर्ट करने में आपकी मदद करूँगा। मैं आपसे 22 आसान सवाल पूछूँगा। आप बोलकर या टाइप करके उत्तर दे सकते हैं। चलिए शुरू करते हैं।",
        "input_placeholder": "{label} के लिए आपका उत्तर...",
        "recorded": "✅ दर्ज किया गया",
        "detected_category": "💡 खोजी गई श्रेणी: **{detected}**",
        "summary_success": "आपने सभी सवालों के जवाब दे दिए हैं। कृपया नीचे दी गई अपनी रिपोर्ट की समीक्षा करें।",
        "field_col": "विवरण",
        "answer_col": "आपका उत्तर",
        "english_col": "अंग्रेजी अनुवाद",
        "btn_submit": "रिपोर्ट सबमिट करें",
        "btn_restart": "पुनः आरंभ करें/संपादित करें (सभी डेटा हटा दिया जाएगा)",
        "report_success": "रिपोर्ट सफलतापूर्वक सबमिट की गई! धन्यवाद।",
        "btn_new": "नई रिपोर्ट शुरू करें",
        "you_said": "आपने कहा"
    },
    "Marathi": {
        "welcome_title": "🗣️ पेशंट रिपोर्टर AI (रुग्ण रिपोर्टर)",
        "tip_voice": "🎙️ *टीप: खालील व्हॉइस रेकॉर्डर वापरा किंवा चॅट इनपुटमध्ये तुमचे उत्तर टाईप करा.*",
        "welcome_msg": "नमस्कार! मी ADR रिपोर्टर AI आहे. औषधामुळे झालेल्या दुष्परिणामाची (रिएक्शन) नोंद करण्यास मी तुम्हाला मदत करेन. मी तुम्हाला २२ सोपे प्रश्न विचारीन. तुम्ही बोलून किंवा टाईप करून उत्तर देऊ शकता. चला तर मग सुरू करूया.",
        "input_placeholder": "{label} साठी आपले उत्तर...",
        "recorded": "✅ नोंदवले गेले",
        "detected_category": "💡 शोधलेला औषध वर्ग: **{detected}**",
        "summary_success": "तुम्ही सर्व प्रश्नांची उत्तरे दिली आहेत. कृपया खालील आपल्या अहवालाचे पुनरावलोकन करा.",
        "field_col": "तपशील",
        "answer_col": "तुमचे उत्तर",
        "english_col": "इंग्रजी अनुवाद",
        "btn_submit": "अहवाल सबमिट करा",
        "btn_restart": "पुन्हा सुरू करा/दुरुस्त करा (सर्व डेटा नष्ट होईल)",
        "report_success": "अहवाल यशस्वीरीत्या सादर केला गेला! धन्यवाद.",
        "btn_new": "नवीन अहवाल सुरू करा",
        "you_said": "तुम्ही म्हणालात"
    }
}

LANG_CODES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN"
}

# --- SESSION STATE INITIALIZATION ---
if "flow_state" not in st.session_state:
    st.session_state.flow_state = "language_selection" # language_selection, chatting, summary, completed
if "language" not in st.session_state:
    st.session_state.language = None
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
    st.markdown("### 🔄 Resume Previous Assessment?")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>We found an incomplete assessment from your last visit. Would you like to resume from where you left off?</p>", unsafe_allow_html=True)
    
    col_resume, col_new = st.columns(2)
    with col_resume:
        if st.button("Yes, Resume Assessment", use_container_width=True, type="primary"):
            try:
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    progress_data = json.load(f)
                st.session_state.language = progress_data.get("language")
                st.session_state.current_q_index = progress_data.get("current_q_index", 0)
                st.session_state.answers = progress_data.get("answers", {})
                st.session_state.answers_original = progress_data.get("answers_original", {})
                st.session_state.auto_category = progress_data.get("auto_category", "Others")
                st.session_state.flow_state = "chatting"
                rebuild_chat_history()
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load progress: {e}")
                
    with col_new:
        if st.button("No, Start New Assessment", use_container_width=True):
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
    lang = st.session_state.language
    if not lang:
        return
    st.session_state.chat_history.append({"role": "assistant", "content": UI_TEXTS[lang]["welcome_msg"]})
    st.session_state.chat_history.append({"role": "assistant", "content": QUESTIONS[0]["text"][lang]})
    
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
        
        label_text = q["label"].get(lang, q["label"]["English"])
        if trans != orig and trans.lower() != orig.lower():
            display_val = f"{orig} (English: {trans})"
        else:
            display_val = orig
        conf_msg = f"**{i + 1}. {label_text}**\n{UI_TEXTS[lang]['you_said']}: {display_val}\n{UI_TEXTS[lang]['recorded']}"
        st.session_state.chat_history.append({"role": "assistant", "content": conf_msg})
        
        if q["key"] == "drug_name":
            detected = st.session_state.auto_category
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": UI_TEXTS[lang]["detected_category"].format(detected=detected)
            })
            
        next_i = i + 1
        if next_i < len(QUESTIONS) and QUESTIONS[next_i]["key"] == "drug_category_manual" and st.session_state.auto_category != "Others (Low Confidence)":
            next_i += 1
        if next_i < len(QUESTIONS) and QUESTIONS[next_i]["key"] == "physician_contact" and st.session_state.answers.get("physician_name") in ["None", "Unknown"]:
            next_i += 1
            
        if next_i < len(QUESTIONS) and next_i <= st.session_state.current_q_index:
            st.session_state.chat_history.append({"role": "assistant", "content": QUESTIONS[next_i]["text"][lang]})

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
        return "Error: Speech recognition library is not available on this server."
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language=language_code)
            return text.strip()
    except sr.UnknownValueError:
        return "Error: Could not understand audio / आवाज समझ में नहीं आया।"
    except sr.RequestError as e:
        return f"Error: Request failed; {e}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI RENDER ---
lang = st.session_state.language if st.session_state.language else "English"

# Sidebar options for quitting assessment and navigation
if st.session_state.flow_state in ["chatting", "summary"]:
    st.sidebar.header("Options")
    if st.session_state.flow_state == "chatting" and st.session_state.current_q_index > 0:
        if st.sidebar.button("⬅️ Previous Question", use_container_width=True):
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
    if st.sidebar.button("🚪 Quit Assessment", use_container_width=True):
        st.session_state.confirm_quit = True
        st.rerun()

# Confirm Quit Assessment Dialog
if st.session_state.get("confirm_quit", False):
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("### ⚠️ Confirm Quit Assessment")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>Are you sure you want to quit? Your current progress will be saved so you can resume later.</p>", unsafe_allow_html=True)
    
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Yes, Quit & Save", use_container_width=True, type="primary"):
            save_progress()
            st.session_state.clear()
            st.rerun()
    with col_no:
        if st.button("No, Continue Assessment", use_container_width=True):
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
    st.markdown("### Which language would you prefer? / आप कौन सी भाषा पसंद करेंगे? / तुम्हाला कोणती भाषा आवडेल?")
    st.markdown("<p style='font-size:14px; opacity:0.8;'>Please select a language to start the conversation with the assistant.</p>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    if cols[0].button("English", use_container_width=True):
        st.session_state.language = "English"
    if cols[1].button("Hindi / हिंदी", use_container_width=True):
        st.session_state.language = "Hindi"
    if cols[2].button("Marathi / मराठी", use_container_width=True):
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
            st.markdown(f"📝 **Current response for {label_text}:** *{current_ans}*")
            
            edited_val = st.text_input(
                "Edit response manually:",
                value=current_ans,
                key=f"inline_edit_{q_index}"
            )
            
            col_save, col_next = st.columns(2)
            with col_save:
                if st.button("💾 Save Changes", use_container_width=True, type="primary", key=f"btn_save_inline_{q_index}"):
                    user_input = edited_val
            with col_next:
                if st.button("➡️ Next Question", use_container_width=True, key=f"btn_next_inline_{q_index}"):
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
            if st.button("⬅️ Previous Question", key=f"btn_prev_main_{q_index}", use_container_width=True):
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
            rec_title = f"🎙️ Record answer for: *{label_text}*"
            if is_answered:
                rec_title = f"🎙️ Speak again / Re-record to replace answer:"
            st.markdown(f"#### {rec_title}")
            audio_file = st.audio_input("Record voice / आवाज रेकॉर्ड करा", key=f"audio_input_{q_index}")
        else:
            st.info("🎙️ Voice input is temporarily disabled (missing dependency). Please type your response below.")
            audio_file = None
        
        placeholder = UI_TEXTS[lang]["input_placeholder"].format(label=label_text)
        chat_val = st.chat_input(placeholder)
        
        # Process voice recording input
        if audio_file:
            with st.spinner("🎙️ Transcribing voice... / आवाज का अनुवाद हो रहा है..."):
                speech_text = transcribe_audio(audio_file, lang_code)
                if speech_text.startswith("Error:"):
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
    with st.expander("✏️ Edit any response"):
        edit_options = [q["label"].get(lang, q["label"]["English"]) for q in QUESTIONS]
        selected_edit_label = st.selectbox("Select field to edit:", edit_options, key="select_edit_field")
        
        # Find corresponding question key
        selected_q = next(q for q in QUESTIONS if q["label"].get(lang, q["label"]["English"]) == selected_edit_label)
        key = selected_q["key"]
        
        current_val_orig = st.session_state.answers_original.get(key, "")
        new_val_orig = st.text_input(f"New response for '{selected_edit_label}':", value=current_val_orig, key=f"edit_input_{key}")
        
        if st.button("💾 Save Changes", use_container_width=True, key=f"save_edit_{key}"):
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
            st.success(f"Updated '{selected_edit_label}' successfully!")
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
                st.error("Failed to save report. Please check database connection.")
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

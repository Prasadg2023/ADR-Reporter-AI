# Centralized Translations for ADR Reporter AI
# Supporting English, Hindi, and Marathi languages.

LANG_CODES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN"
}

LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr"
}

NAV_TEXTS = {
    "English": {
        "nav_title": "Navigation",
        "home": "🏠 Home",
        "patient_assessment": "📝 Patient Assessment",
        "dashboard": "📊 Dashboard",
        "select_lang": "Language / भाषा / भाषा"
    },
    "Hindi": {
        "nav_title": "नेविगेशन",
        "home": "🏠 मुख्य पृष्ठ",
        "patient_assessment": "📝 मरीज मूल्यांकन",
        "dashboard": "📊 डैशबोर्ड",
        "select_lang": "Language / भाषा / भाषा"
    },
    "Marathi": {
        "nav_title": "नेव्हिगेशन",
        "home": "🏠 मुख्यपृष्ठ",
        "patient_assessment": "📝 रुग्ण मूल्यांकन",
        "dashboard": "📊 डॅशबोर्ड",
        "select_lang": "Language / भाषा / भाषा"
    }
}

APP_TEXTS = {
    "English": {
        "page_title": "ADR Reporter AI Configuration",
        "title": "💊 ADR Reporter AI Configuration",
        "welcome_hdr": "Welcome to the Adverse Drug Reaction (ADR) Reporter AI System",
        "welcome_desc": "This intelligent assistant automates and manages patient report ingestion and clinical analysis.",
        "sidebar_prompt": "Please use the sidebar on the left to navigate between modules:",
        "li_reporter": "<strong>📝 Patient Reporter:</strong> A conversational multilingual interface for patients to report adverse drug events step-by-step.",
        "li_dashboard": "<strong>📊 Owner Dashboard:</strong> A comprehensive analytical dashboard for administrators to inspect, filter, and export collected ADR records.",
        "db_success": "Database initialized successfully. Ensure your MySQL server (e.g. XAMPP) is running.",
        "db_failed": "Failed to initialize database: {e}"
    },
    "Hindi": {
        "page_title": "ADR रिपोर्टर AI कॉन्फ़िगरेशन",
        "title": "💊 ADR रिपोर्टर AI कॉन्फ़िगरेशन",
        "welcome_hdr": "प्रतिकूल दवा प्रतिक्रिया (ADR) रिपोर्टर AI सिस्टम में आपका स्वागत है",
        "welcome_desc": "यह बुद्धिमान सहायक मरीज की रिपोर्ट दर्ज करने और नैदानिक विश्लेषण को स्वचालित और प्रबंधित करता है।",
        "sidebar_prompt": "मॉड्यूल्स के बीच नेविगेट करने के लिए कृपया बाईं ओर स्थित साइडबार का उपयोग करें:",
        "li_reporter": "<strong>📝 मरीज रिपोर्टर:</strong> मरीजों के लिए प्रतिकूल दवा घटनाओं की कदम-दर-कदम रिपोर्ट करने के लिए एक संवादात्मक बहुभाषी इंटरफ़ेस।",
        "li_dashboard": "<strong>📊 ओनर डैशबोर्ड:</strong> प्रशासकों के लिए एकत्रित ADR रिकॉर्ड का निरीक्षण, फ़िल्टर और निर्यात करने के लिए एक व्यापक विश्लेषणात्मक डैशबोर्ड।",
        "db_success": "डेटाबेस सफलतापूर्वक प्रारंभ हो गया। सुनिश्चित करें कि आपका MySQL सर्वर (जैसे XAMPP) चल रहा है।",
        "db_failed": "डेटाबेस प्रारंभ करने में विफल: {e}"
    },
    "Marathi": {
        "page_title": "ADR रिपोर्टर AI कॉन्फिगरेशन",
        "title": "💊 ADR रिपोर्टर AI कॉन्फिगरेशन",
        "welcome_hdr": "औषधांच्या प्रतिकूल परिणाम (ADR) रिपोर्टर AI सिस्टममध्ये आपले स्वागत आहे",
        "welcome_desc": "हे बुद्धिमान सहाय्यक रुग्णांचे अहवाल नोंदवणे आणि क्लिनिकल विश्लेषणाचे काम स्वयंचलित आणि व्यवस्थापित करते.",
        "sidebar_prompt": "मॉड्यूल्समध्ये नेव्हिगेट करण्यासाठी कृपया डावीकडील साइडबार वापरा:",
        "li_reporter": "<strong>📝 रुग्ण रिपोर्टर:</strong> रुग्णांसाठी टप्प्याटप्प्याने औषधांच्या दुष्परिणामांची नोंद करण्यासाठी एक संवादात्मक बहुभाषिक इंटरफेस.",
        "li_dashboard": "<strong>📊 ओनर डॅशबोर्ड:</strong> प्रशासकांसाठी गोळा केलेले ADR रेकॉर्ड्स तपासण्यासाठी, फिल्टर करण्यासाठी आणि एक्सपोर्ट करण्यासाठी एक सर्वसमावेशक विश्लेषणात्मक डॅशबोर्ड.",
        "db_success": "डेटाबेस यशस्वीरीत्या सुरू झाला. आपला MySQL सर्व्हर (उदा. XAMPP) सुरू असल्याची खात्री करा.",
        "db_failed": "डेटाबेस सुरू करण्यात अयशस्वी: {e}"
    }
}

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

REPORTER_UI_TEXTS = {
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
        "you_said": "You said",
        
        "options_hdr": "Options",
        "btn_prev": "⬅️ Previous Question",
        "btn_quit": "🚪 Quit Assessment",
        "quit_confirm_title": "### ⚠️ Confirm Quit Assessment",
        "quit_confirm_msg": "<p style='font-size:14px; opacity:0.8;'>Are you sure you want to quit? Your current progress will be saved so you can resume later.</p>",
        "btn_quit_yes": "Yes, Quit & Save",
        "btn_quit_no": "No, Continue Assessment",
        
        "resume_title": "### 🔄 Resume Previous Assessment?",
        "resume_msg": "<p style='font-size:14px; opacity:0.8;'>We found an incomplete assessment from your last visit. Would you like to resume from where you left off?</p>",
        "btn_resume_yes": "Yes, Resume Assessment",
        "btn_resume_no": "No, Start New Assessment",
        "resume_err": "Failed to load progress: {e}",
        
        "lang_selection_title": "### Which language would you prefer? / आप कौन सी भाषा पसंद करेंगे? / तुम्हाला कोणती भाषा आवडेल?",
        "lang_selection_msg": "<p style='font-size:14px; opacity:0.8;'>Please select a language to start the conversation with the assistant.</p>",
        
        "inline_current_response": "📝 **Current response for {label_text}:** *{current_ans}*",
        "inline_edit_label": "Edit response manually:",
        "btn_save_changes": "💾 Save Changes",
        "btn_next_question": "➡️ Next Question",
        
        "voice_record_title": "🎙️ Record answer for: *{label_text}*",
        "voice_record_replace": "🎙️ Speak again / Re-record to replace answer:",
        "audio_input_label": "Record voice / आवाज रेकॉर्ड करा",
        "voice_disabled_info": "🎙️ Voice input is temporarily disabled (missing dependency). Please type your response below.",
        "voice_spinner": "🎙️ Transcribing voice...",
        
        "edit_expander": "✏️ Edit any response",
        "edit_select_field": "Select field to edit:",
        "edit_new_response": "New response for '{selected_edit_label}':",
        "edit_success": "Updated '{selected_edit_label}' successfully!",
        "db_save_err": "Failed to save report. Please check database connection."
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
        "you_said": "आपने कहा",
        
        "options_hdr": "विकल्प",
        "btn_prev": "⬅️ पिछला प्रश्न",
        "btn_quit": "🚪 मूल्यांकन समाप्त करें",
        "quit_confirm_title": "### ⚠️ मूल्यांकन समाप्त करने की पुष्टि करें",
        "quit_confirm_msg": "<p style='font-size:14px; opacity:0.8;'>क्या आप वाकई बाहर निकलना चाहते हैं? आपकी वर्तमान प्रगति को सहेज लिया जाएगा ताकि आप बाद में फिर से शुरू कर सकें।</p>",
        "btn_quit_yes": "हाँ, समाप्त करें और सहेजें",
        "btn_quit_no": "नहीं, मूल्यांकन जारी रखें",
        
        "resume_title": "### 🔄 पिछला मूल्यांकन फिर से शुरू करें?",
        "resume_msg": "<p style='font-size:14px; opacity:0.8;'>हमें आपकी पिछली यात्रा से एक अधूरा मूल्यांकन मिला है। क्या आप वहीं से शुरू करना चाहेंगे जहाँ आपने छोड़ा था?</p>",
        "btn_resume_yes": "हाँ, मूल्यांकन फिर से शुरू करें",
        "btn_resume_no": "नहीं, नया मूल्यांकन शुरू करें",
        "resume_err": "प्रगति लोड करने में विफल: {e}",
        
        "lang_selection_title": "### Which language would you prefer? / आप कौन सी भाषा पसंद करेंगे? / तुम्हाला कोणती भाषा आवडेल?",
        "lang_selection_msg": "<p style='font-size:14px; opacity:0.8;'>कृपया सहायक के साथ बातचीत शुरू करने के लिए एक भाषा चुनें।</p>",
        
        "inline_current_response": "📝 **{label_text} के लिए वर्तमान उत्तर:** *{current_ans}*",
        "inline_edit_label": "मैन्युअल रूप से उत्तर संपादित करें:",
        "btn_save_changes": "💾 परिवर्तन सहेजें",
        "btn_next_question": "➡️ अगला प्रश्न",
        
        "voice_record_title": "🎙️ *{label_text}* के लिए उत्तर रिकॉर्ड करें",
        "voice_record_replace": "🎙️ फिर से बोलें / उत्तर बदलने के लिए फिर से रिकॉर्ड करें:",
        "audio_input_label": "आवाज रिकॉर्ड करें",
        "voice_disabled_info": "🎙️ वॉयस इनपुट अस्थायी रूप से अक्षम है (लापता निर्भरता)। कृपया नीचे अपना उत्तर टाइप करें।",
        "voice_spinner": "🎙️ आवाज का अनुवाद हो रहा है...",
        
        "edit_expander": "✏️ किसी भी उत्तर को संपादित करें",
        "edit_select_field": "संपादित करने के लिए फ़ील्ड चुनें:",
        "edit_new_response": "'{selected_edit_label}' के लिए नया उत्तर:",
        "edit_success": "'{selected_edit_label}' को सफलतापूर्वक अपडेट किया गया!",
        "db_save_err": "रिपोर्ट सहेजने में विफल। कृपया डेटाबेस कनेक्शन की जाँच करें।"
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
        "you_said": "तुम्ही म्हणालात",
        
        "options_hdr": "पर्याय",
        "btn_prev": "➡️ मागील प्रश्न",
        "btn_quit": "🚪 मूल्यांकन बंद करा",
        "quit_confirm_title": "### ⚠️ मूल्यांकन बंद करण्याची खात्री करा",
        "quit_confirm_msg": "<p style='font-size:14px; opacity:0.8;'>तुम्हाला नक्की बंद करायचे आहे का? तुमची सध्याची प्रगती सेव्ह केली जाईल जेणेकरून तुम्ही नंतर पुन्हा सुरू करू शकाल.</p>",
        "btn_quit_yes": "होय, बंद करा आणि सेव्ह करा",
        "btn_quit_no": "नाही, मूल्यांकन सुरू ठेवा",
        
        "resume_title": "### 🔄 मागील मूल्यांकन पुन्हा सुरू करायचे?",
        "resume_msg": "<p style='font-size:14px; opacity:0.8;'>आम्हाला तुमच्या मागील भेटीतील एक अपूर्ण मूल्यांकन आढळले आहे. तुम्ही जेथून सोडले होते तेथूनच पुन्हा सुरू करू इच्छिता का?</p>",
        "btn_resume_yes": "होय, मूल्यांकन पुन्हा सुरू करा",
        "btn_resume_no": "नाही, नवीन मूल्यांकन सुरू करा",
        "resume_err": "प्रगती लोड करण्यात अयशस्वी: {e}",
        
        "lang_selection_title": "### Which language would you prefer? / आप कौन सी भाषा पसंद करेंगे? / तुम्हाला कोणती भाषा आवडेल?",
        "lang_selection_msg": "<p style='font-size:14px; opacity:0.8;'>कृपया असिस्टंटसोबत संभाषण सुरू करण्यासाठी भाषा निवडा.</p>",
        
        "inline_current_response": "📝 **{label_text} साठी सध्याचा प्रतिसाद:** *{current_ans}*",
        "inline_edit_label": "प्रतिसाद मॅन्युअली संपादित करा:",
        "btn_save_changes": "💾 बदल सेव्ह करा",
        "btn_next_question": "➡️ पुढील प्रश्न",
        
        "voice_record_title": "🎙️ *{label_text}* साठी प्रतिसाद रेकॉर्ड करा",
        "voice_record_replace": "🎙️ पुन्हा बोला / प्रतिसाद बदलण्यासाठी पुन्हा रेकॉर्ड करा:",
        "audio_input_label": "आवाज रेकॉर्ड करा",
        "voice_disabled_info": "🎙️ व्हॉइस इनपुट तात्पुरते बंद आहे (लापता अवलंबित्व). कृपया खाली तुमचा प्रतिसाद टाईप करा.",
        "voice_spinner": "🎙️ आवाजाचे लिप्यंतरण होत आहे...",
        
        "edit_expander": "✏️ कोणताही प्रतिसाद संपादित करा",
        "edit_select_field": "संपादित करण्यासाठी फील्ड निवडा:",
        "edit_new_response": "'{selected_edit_label}' साठी नवीन प्रतिसाद:",
        "edit_success": "'{selected_edit_label}' यशस्वीरीत्या अपडेट केले!",
        "db_save_err": "अहवाल जतन करण्यात अयशस्वी. कृपया डेटाबेस कनेक्शन तपासा."
    }
}

DASHBOARD_TEXTS = {
    "English": {
        "page_title": "Owner Dashboard",
        "title": "📊 Owner Dashboard",
        "load_err": "No reports found in the database. Please submit a report first.",
        "filter_hdr": "Filter Reports",
        "filter_date": "Date Range",
        "filter_category": "Drug Category",
        "filter_gender": "Gender",
        "metrics_hdr": "Key Metrics",
        "metric_total": "Total Reports",
        "metric_filtered": "Filtered Reports",
        "metric_top": "Top Category",
        "analytics_hdr": "Analytics",
        "chart_cat_dist": "Drug Category Distribution",
        "chart_gender_split": "Gender Split",
        "chart_monthly_trend": "Monthly Trend of Reports",
        "chart_xaxis_trend": "Month-Year",
        "chart_yaxis_trend": "Number of Reports",
        "detailed_hdr": "Detailed Reports",
        "btn_download_csv": "📥 Download Filtered Data as CSV",
        "pdf_section_hdr": "Export / View Individual Report (PDF)",
        "pdf_select_report": "Select Report to Export/View as PDF (by ID)",
        "btn_download_pdf": "📥 Download Report {report_to_export} PDF",
        "expander_view_pdf": "👁️ View PDF in Dashboard",
        "pdf_fetch_err": "Failed to retrieve PDF data.",
        "pdf_gen_err": "Failed to generate or retrieve PDF: {e}",
        "admin_hdr": "### 🗑️ Administrator Panel",
        "admin_expander": "Access Administrator Actions",
        "admin_password_label": "Enter Administrator Password",
        "admin_success": "Authorized Access",
        "admin_error": "Incorrect Password. Access Denied.",
        "admin_select_delete": "Select Report ID to Delete",
        "admin_confirm_delete": "Confirm permanent deletion of Report ID {report_to_delete}",
        "admin_btn_delete": "❌ Permanently Delete Report",
        "admin_delete_success": "Report ID {report_to_delete} deleted successfully!",
        "admin_delete_failed": "Failed to delete report from the database.",
        "admin_delete_warn": "Please check the confirmation box to proceed.",
        "admin_no_reports": "No reports available to delete."
    },
    "Hindi": {
        "page_title": "ओनर डैशबोर्ड",
        "title": "📊 ओनर डैशबोर्ड",
        "load_err": "डेटाबेस में कोई रिपोर्ट नहीं मिली। कृपया पहले एक रिपोर्ट सबमिट करें।",
        "filter_hdr": "रिपोर्ट फ़िल्टर करें",
        "filter_date": "तिथि सीमा",
        "filter_category": "दवा की श्रेणी",
        "filter_gender": "लिंग",
        "metrics_hdr": "प्रमुख मेट्रिक्स",
        "metric_total": "कुल रिपोर्ट",
        "metric_filtered": "फ़िल्टर की गई रिपोर्ट",
        "metric_top": "शीर्ष श्रेणी",
        "analytics_hdr": "विश्लेषण",
        "chart_cat_dist": "दवा श्रेणी वितरण",
        "chart_gender_split": "लिंग विभाजन",
        "chart_monthly_trend": "रिपोर्ट का मासिक रुझान",
        "chart_xaxis_trend": "माह-वर्ष",
        "chart_yaxis_trend": "रिपोर्ट की संख्या",
        "detailed_hdr": "विस्तृत रिपोर्ट",
        "btn_download_csv": "📥 फ़िल्टर किया गया डेटा CSV के रूप में डाउनलोड करें",
        "pdf_section_hdr": "व्यक्तिगत रिपोर्ट निर्यात / देखें (PDF)",
        "pdf_select_report": "निर्यात/PDF के रूप में देखने के लिए रिपोर्ट चुनें (ID द्वारा)",
        "btn_download_pdf": "📥 रिपोर्ट {report_to_export} PDF डाउनलोड करें",
        "expander_view_pdf": "👁️ डैशबोर्ड में PDF देखें",
        "pdf_fetch_err": "PDF डेटा पुनर्प्राप्त करने में विफल।",
        "pdf_gen_err": "PDF उत्पन्न करने या प्राप्त करने में विफल: {e}",
        "admin_hdr": "### 🗑️ प्रशासक पैनल",
        "admin_expander": "प्रशासक क्रियाओं तक पहुँचें",
        "admin_password_label": "प्रशासक पासवर्ड दर्ज करें",
        "admin_success": "अधिकृत पहुँच",
        "admin_error": "गलत पासवर्ड। पहुँच अस्वीकृत।",
        "admin_select_delete": "हटाने के लिए रिपोर्ट ID चुनें",
        "admin_confirm_delete": "रिपोर्ट ID {report_to_delete} को स्थायी रूप से हटाने की पुष्टि करें",
        "admin_btn_delete": "❌ रिपोर्ट को स्थायी रूप से हटाएं",
        "admin_delete_success": "रिपोर्ट ID {report_to_delete} सफलतापूर्वक हटा दी गई!",
        "admin_delete_failed": "डेटाबेस से रिपोर्ट हटाने में विफल।",
        "admin_delete_warn": "आगे बढ़ने के लिए कृपया पुष्टि बॉक्स को चेक करें।",
        "admin_no_reports": "हटाने के लिए कोई रिपोर्ट उपलब्ध नहीं है।"
    },
    "Marathi": {
        "page_title": "ओनर डॅशबोर्ड",
        "title": "📊 ओनर डॅशबोर्ड",
        "load_err": "डेटाबेसमध्ये कोणतेही अहवाल आढळले नाहीत. कृपया आधी एक अहवाल सबमिट करा.",
        "filter_hdr": "अहवाल फिल्टर करा",
        "filter_date": "तारीख मर्यादा",
        "filter_category": "औषधाचा वर्ग",
        "filter_gender": "लिंग",
        "metrics_hdr": "महत्त्वाचे मेट्रिक्स",
        "metric_total": "एकूण अहवाल",
        "metric_filtered": "फिल्टर केलेले अहवाल",
        "metric_top": "प्रमुख वर्ग",
        "analytics_hdr": "विश्लेषण",
        "chart_cat_dist": "औषध वर्ग वितरण",
        "chart_gender_split": "लिंग विभागणी",
        "chart_monthly_trend": "अहवालांचा मासिक ट्रेंड",
        "chart_xaxis_trend": "महिना-वर्ष",
        "chart_yaxis_trend": "अहवालांची संख्या",
        "detailed_hdr": "सविस्तर अहवाल",
        "btn_download_csv": "📥 फिल्टर केलेला डेटा CSV स्वरूपात डाउनलोड करा",
        "pdf_section_hdr": "वैयक्तिक अहवाल एक्सपोर्ट करा / पहा (PDF)",
        "pdf_select_report": "एक्सपोर्ट करण्यासाठी/PDF म्हणून पाहण्यासाठी अहवाल निवडा (ID द्वारे)",
        "btn_download_pdf": "📥 अहवाल {report_to_export} PDF डाउनलोड करा",
        "expander_view_pdf": "👁️ डॅशबोर्डमध्ये PDF पहा",
        "pdf_fetch_err": "PDF डेटा मिळवण्यात अपयश.",
        "pdf_gen_err": "PDF तयार करण्यात किंवा मिळवण्यात अयशस्वी: {e}",
        "admin_hdr": "### 🗑️ प्रशासक पॅनेल",
        "admin_expander": "प्रशासक क्रियांमध्ये प्रवेश करा",
        "admin_password_label": "प्रशासक पासवर्ड प्रविष्ट करा",
        "admin_success": "अधिकृत प्रवेश",
        "admin_error": "चुकीचा पासवर्ड. प्रवेश नाकारला.",
        "admin_select_delete": "नष्ट करण्यासाठी अहवाल ID निवडा",
        "admin_confirm_delete": "अहवाल ID {report_to_delete} कायमचे नष्ट करण्याची पुष्टी करा",
        "admin_btn_delete": "❌ अहवाल कायमचा नष्ट करा",
        "admin_delete_success": "अहवाल ID {report_to_delete} यशस्वीरीत्या नष्ट केला गेला!",
        "admin_delete_failed": "डेटाबेसमधून अहवाल नष्ट करण्यात अयशस्वी.",
        "admin_delete_warn": "कृपया पुढे जाण्यासाठी पुष्टीकरण बॉक्स तपासा.",
        "admin_no_reports": "नष्ट करण्यासाठी कोणताही अहवाल उपलब्ध नाही."
    }
}

COLUMNS_MAPPING = {
    "English": {
        "report_id": "Report ID",
        "submission_timestamp": "Submission Date",
        "final_drug_category": "Therapeutic Category",
        "patient_name": "Patient Name",
        "patient_email": "Email Address",
        "patient_mobile": "Mobile Number",
        "age": "Age",
        "gender": "Gender",
        "weight_kg": "Weight (kg)",
        "drug_name": "Drug Name",
        "indication": "Reason for Medicine",
        "medicine_start_date": "Medicine Start Date",
        "medicine_stop_date": "Medicine Stop Date",
        "reaction_start_date": "Reaction Start Date",
        "reaction_end_date": "Reaction End Date",
        "reaction_description": "Reaction Description",
        "drug_category_manual": "Drug Category (Manual)",
        "route_of_administration": "Route of Administration",
        "strength": "Strength",
        "frequency": "Frequency",
        "batch_number": "Batch Number",
        "expiry_date": "Expiry Date",
        "action_taken": "Action Taken",
        "physician_name": "Physician Name",
        "physician_contact": "Physician Contact"
    },
    "Hindi": {
        "report_id": "रिपोर्ट आईडी",
        "submission_timestamp": "जमा करने की तिथि",
        "final_drug_category": "दवा की श्रेणी",
        "patient_name": "मरीज का नाम",
        "patient_email": "ईमेल पता",
        "patient_mobile": "मोबाइल नंबर",
        "age": "उम्र",
        "gender": "लिंग",
        "weight_kg": "वजन (किग्रा)",
        "drug_name": "दवा का नाम",
        "indication": "दवा लेने का कारण",
        "medicine_start_date": "दवा शुरू करने की तिथि",
        "medicine_stop_date": "दवा बंद करने की तिथि",
        "reaction_start_date": "रिएक्शन शुरू होने की तिथि",
        "reaction_end_date": "रिएक्शन समाप्त होने की तिथि",
        "reaction_description": "रिएक्शन का विवरण",
        "drug_category_manual": "दवा की श्रेणी (मैन्युअल)",
        "route_of_administration": "दवा लेने का मार्ग",
        "strength": "दवा की क्षमता",
        "frequency": "दवा लेने की आवृत्ति",
        "batch_number": "बैच संख्या",
        "expiry_date": "एक्सपायरी डेट",
        "action_taken": "की गई कार्रवाई",
        "physician_name": "चिकित्सक का नाम",
        "physician_contact": "चिकित्सक का संपर्क"
    },
    "Marathi": {
        "report_id": "अहवाल आयडी",
        "submission_timestamp": "सादर केल्याची तारीख",
        "final_drug_category": "औषधाचा वर्ग",
        "patient_name": "रुग्णाचे नाव",
        "patient_email": "ईमेल पत्ता",
        "patient_mobile": "मोबाईल नंबर",
        "age": "वय",
        "gender": "लिंग",
        "weight_kg": "वजन (किग्रॅ)",
        "drug_name": "औषधाचे नाव",
        "indication": "औषध घेण्याचे कारण",
        "medicine_start_date": "औषध सुरू केल्याची तारीख",
        "medicine_stop_date": "औषध बंद केल्याची तारीख",
        "reaction_start_date": "रिएक्शन सुरू झाल्याची तारीख",
        "reaction_end_date": "रिएक्शन संपल्याची तारीख",
        "reaction_description": "रिएक्शनचे वर्णन",
        "drug_category_manual": "औषधाचा वर्ग (मॅन्युअल)",
        "route_of_administration": "औषध घेण्याचा मार्ग",
        "strength": "औषधाची क्षमता",
        "frequency": "औषध घेण्याची वारंवारता",
        "batch_number": "बॅच नंबर",
        "expiry_date": "एक्सपायरी तारीख",
        "action_taken": "केलेली कारवाई",
        "physician_name": "डॉक्टरांचे नाव",
        "physician_contact": "डॉक्टरांचा संपर्क"
    }
}

PDF_TEXTS = {
    "English": {
        "title": "ADVERSE DRUG REACTION REPORT",
        "sec_patient": "1. PATIENT INFORMATION",
        "sec_drug": "2. SUSPECTED DRUG(S) INFORMATION",
        "sec_reaction": "3. ADVERSE DRUG REACTION DETAILS",
        "sec_physician": "4. ASSOCIATED PHYSICIAN DETAILS",
        "sig_reporter": "Reporter / Patient Signature",
        "sig_pharmacist": "Reviewing Pharmacist Signature",
        
        "label_report_id": "Report ID",
        "label_submission_date": "Submission Date",
        "label_patient_name": "Patient Name",
        "label_age_gender": "Age / Gender",
        "label_weight": "Weight",
        "label_mobile": "Mobile Number",
        "label_email": "Email Address",
        "label_drug_name": "Drug Name",
        "label_category": "Therapeutic Category",
        "label_strength": "Strength / Dose",
        "label_frequency": "Frequency",
        "label_route": "Route of Admin",
        "label_indication": "Indication",
        "label_batch": "Batch Number",
        "label_expiry": "Expiry Date",
        "label_started": "Date Started",
        "label_stopped": "Date Stopped",
        "label_reaction_started": "Reaction Started",
        "label_reaction_ended": "Reaction Ended",
        "label_action_taken": "Action Taken",
        "label_description_hdr": "Adverse Drug Reaction Description:",
        "label_physician_name": "Physician Name",
        "label_physician_contact": "Physician Contact"
    },
    "Hindi": {
        "title": "प्रतिकूल दवा प्रतिक्रिया रिपोर्ट (ADR REPORT)",
        "sec_patient": "1. मरीज की जानकारी (PATIENT INFORMATION)",
        "sec_drug": "2. संदेहास्पद दवा की जानकारी (SUSPECTED DRUG INFORMATION)",
        "sec_reaction": "3. प्रतिकूल दवा प्रतिक्रिया विवरण (ADR DETAILS)",
        "sec_physician": "4. संबंधित चिकित्सक का विवरण (PHYSICIAN DETAILS)",
        "sig_reporter": "रिपोर्टर / मरीज के हस्ताक्षर",
        "sig_pharmacist": "समीक्षा करने वाले फार्मासिस्ट के हस्ताक्षर",
        
        "label_report_id": "रिपोर्ट आईडी",
        "label_submission_date": "जमा करने की तिथि",
        "label_patient_name": "मरीज का नाम",
        "label_age_gender": "उम्र / लिंग",
        "label_weight": "वजन",
        "label_mobile": "मोबाइल नंबर",
        "label_email": "ईमेल पता",
        "label_drug_name": "दवा का नाम",
        "label_category": "दवा की श्रेणी",
        "label_strength": "क्षमता (डोज)",
        "label_frequency": "आवृत्ति",
        "label_route": "लेने का मार्ग",
        "label_indication": "दवा का कारण",
        "label_batch": "बैच संख्या",
        "label_expiry": "एक्सपायरी डेट",
        "label_started": "शुरू करने की तिथि",
        "label_stopped": "बंद करने की तिथि",
        "label_reaction_started": "रिएक्शन शुरू तिथि",
        "label_reaction_ended": "रिएक्शन समाप्त तिथि",
        "label_action_taken": "की गई कार्रवाई",
        "label_description_hdr": "प्रतिकूल प्रतिक्रिया का विवरण:",
        "label_physician_name": "चिकित्सक का नाम",
        "label_physician_contact": "चिकित्सक का संपर्क"
    },
    "Marathi": {
        "title": "प्रतिकूल औषध प्रतिक्रिया अहवाल (ADR REPORT)",
        "sec_patient": "1. रुग्णाची माहिती (PATIENT INFORMATION)",
        "sec_drug": "2. संशयित औषधांची माहिती (SUSPECTED DRUG INFORMATION)",
        "sec_reaction": "3. प्रतिकूल औषध प्रतिक्रिया तपशील (ADR DETAILS)",
        "sec_physician": "4. संबंधित डॉक्टरांचा तपशील (PHYSICIAN DETAILS)",
        "sig_reporter": "रिपोर्टर / रुग्णाची सही",
        "sig_pharmacist": "तपासणी करणाऱ्या फार्मासिस्टची सही",
        
        "label_report_id": "अहवाल आयडी",
        "label_submission_date": "सादर केल्याची तारीख",
        "label_patient_name": "रुग्णाचे नाव",
        "label_age_gender": "वय / लिंग",
        "label_weight": "वजन",
        "label_mobile": "मोबाईल नंबर",
        "label_email": "ईमेल पत्ता",
        "label_drug_name": "औषधाचे नाव",
        "label_category": "औषधाचा वर्ग",
        "label_strength": "क्षमता (डोस)",
        "label_frequency": "वारंवारता",
        "label_route": "घेण्याचा मार्ग",
        "label_indication": "घेण्याचे कारण",
        "label_batch": "बॅच नंबर",
        "label_expiry": "एक्सपायरी तारीख",
        "label_started": "सुरू केल्याची तारीख",
        "label_stopped": "बंद केल्याची तारीख",
        "label_reaction_started": "रिएक्शन सुरू तारीख",
        "label_reaction_ended": "रिएक्शन संपलेली तारीख",
        "label_action_taken": "केलेली कारवाई",
        "label_description_hdr": "प्रतिकूल प्रतिसादाचे वर्णन:",
        "label_physician_name": "डॉक्टरांचे नाव",
        "label_physician_contact": "डॉक्टरांचा संपर्क"
    }
}

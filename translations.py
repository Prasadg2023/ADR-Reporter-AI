import streamlit as st

LANGUAGES = ["English", "Hindi", "Marathi"]

LANG_CODES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN"
}

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
        "you_said": "You said",

        # Navigation and buttons
        "btn_prev": "⬅️ Previous Question",
        "btn_quit": "🚪 Quit Assessment",
        "confirm_quit_title": "⚠️ Confirm Quit Assessment",
        "confirm_quit_desc": "Are you sure you want to quit? Your current progress will be saved so you can resume later.",
        "btn_quit_yes": "Yes, Quit & Save",
        "btn_quit_no": "No, Continue Assessment",
        "resume_title": "🔄 Resume Previous Assessment?",
        "resume_desc": "We found an incomplete assessment from your last visit. Would you like to resume from where you left off?",
        "btn_resume_yes": "Yes, Resume Assessment",
        "btn_resume_no": "No, Start New Assessment",
        "current_response": "📝 **Current response for {label}:** *{ans}*",
        "edit_response_manually": "Edit response manually:",
        "btn_save_changes": "💾 Save Changes",
        "btn_next_question": "➡️ Next Question",
        "record_answer_for": "🎙️ Record answer for: *{label}*",
        "speak_again_to_replace": "🎙️ Speak again / Re-record to replace answer:",
        "audio_input_label": "Record voice / आवाज रेकॉर्ड करा / आवाज रिकॉर्ड करें",
        "voice_input_disabled": "🎙️ Voice input is temporarily disabled (missing dependency). Please type your response below.",
        "transcribing_voice": "🎙️ Transcribing voice...",
        "edit_any_response": "✏️ Edit any response",
        "select_field_to_edit": "Select field to edit:",
        "new_response_for": "New response for '{label}':",
        "updated_successfully": "Updated '{label}' successfully!",
        "db_save_failed": "Failed to save report. Please check database connection.",
        
        # Sidebar language header
        "sidebar_lang_header": "🌐 Language Selection",
        "sidebar_options_header": "Options",

        # app.py landing page
        "app_title": "💊 ADR Reporter AI Configuration",
        "app_welcome_header": "Welcome to the Adverse Drug Reaction (ADR) Reporter AI System",
        "app_welcome_desc": "This intelligent assistant automates and manages patient report ingestion and clinical analysis.",
        "app_sidebar_desc": "Please use the sidebar on the left to navigate between modules:",
        "app_patient_reporter_bullet": "<strong>📝 Patient Reporter:</strong> A conversational multilingual interface for patients to report adverse drug events step-by-step.",
        "app_dashboard_bullet": "<strong>📊 Owner Dashboard:</strong> A comprehensive analytical dashboard for administrators to inspect, filter, and export collected ADR records.",
        "app_db_success": "Database initialized successfully. Ensure your MySQL server (e.g. XAMPP) is running.",

        # dashboard.py translations
        "dash_title": "📊 Owner Dashboard",
        "dash_no_reports": "No reports found in the database. Please submit a report first.",
        "dash_filter_reports": "Filter Reports",
        "dash_date_range": "Date Range",
        "dash_drug_category": "Drug Category",
        "dash_gender": "Gender",
        "dash_key_metrics": "Key Metrics",
        "dash_total_reports": "Total Reports",
        "dash_filtered_reports": "Filtered Reports",
        "dash_top_category": "Top Category",
        "dash_analytics": "Analytics",
        "dash_dist_title": "Drug Category Distribution",
        "dash_gender_split": "Gender Split",
        "dash_monthly_trend": "Monthly Trend of Reports",
        "dash_month_year": "Month-Year",
        "dash_num_reports": "Number of Reports",
        "dash_detailed_reports": "Detailed Reports",
        "dash_download_csv": "📥 Download Filtered Data as CSV",
        "dash_export_view_pdf": "Export / View Individual Report (PDF)",
        "dash_select_report_by_id": "Select Report to Export/View as PDF (by ID)",
        "dash_download_pdf": "📥 Download Report {id} PDF",
        "dash_view_pdf_inline": "👁️ View PDF in Dashboard",
        "dash_pdf_failed": "Failed to retrieve PDF data.",
        "dash_pdf_gen_error": "Failed to generate or retrieve PDF: {err}",
        "dash_admin_panel": "🗑️ Administrator Panel",
        "dash_admin_actions": "Access Administrator Actions",
        "dash_admin_pwd_label": "Enter Administrator Password",
        "dash_auth_success": "Authorized Access",
        "dash_select_delete_id": "Select Report ID to Delete",
        "dash_confirm_delete": "Confirm permanent deletion of Report ID {id}",
        "dash_btn_delete": "❌ Permanently Delete Report",
        "dash_delete_success": "Report ID {id} deleted successfully!",
        "dash_delete_failed": "Failed to delete report from the database.",
        "dash_check_confirm": "Please check the confirmation box to proceed.",
        "dash_no_delete_avail": "No reports available to delete.",
        "dash_incorrect_pwd": "Incorrect Password. Access Denied.",
        "dash_all": "All"
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

        # Navigation and buttons
        "btn_prev": "⬅️ पिछला प्रश्न",
        "btn_quit": "🚪 मूल्यांकन समाप्त करें",
        "confirm_quit_title": "⚠️ मूल्यांकन बंद करने की पुष्टि करें",
        "confirm_quit_desc": "क्या आप वाकई बाहर निकलना चाहते हैं? आपकी वर्तमान प्रगति को सहेज लिया जाएगा ताकि आप बाद में फिर से शुरू कर सकें।",
        "btn_quit_yes": "हाँ, बाहर निकलें और सहेजें",
        "btn_quit_no": "नहीं, मूल्यांकन जारी रखें",
        "resume_title": "🔄 पिछला मूल्यांकन फिर से शुरू करें?",
        "resume_desc": "हमें आपकी पिछली यात्रा से एक अधूरा मूल्यांकन मिला है। क्या आप वहीं से शुरू करना चाहेंगे जहाँ आपने छोड़ा था?",
        "btn_resume_yes": "हाँ, मूल्यांकन फिर से शुरू करें",
        "btn_resume_no": "नहीं, नया मूल्यांकन शुरू करें",
        "current_response": "📝 **{label} के लिए वर्तमान उत्तर:** *{ans}*",
        "edit_response_manually": "उत्तर को मैन्युअल रूप से संपादित करें:",
        "btn_save_changes": "💾 बदलाव सहेजें",
        "btn_next_question": "➡️ अगला प्रश्न",
        "record_answer_for": "🎙️ {label} के लिए उत्तर रिकॉर्ड करें:",
        "speak_again_to_replace": "🎙️ उत्तर बदलने के लिए फिर से बोलें / फिर से रिकॉर्ड करें:",
        "audio_input_label": "आवाज रिकॉर्ड करें",
        "voice_input_disabled": "🎙️ वॉयस इनपुट अस्थायी रूप से अक्षम है (लापता निर्भरता)। कृपया नीचे अपना उत्तर टाइप करें।",
        "transcribing_voice": "🎙️ आवाज का अनुवाद हो रहा है...",
        "edit_any_response": "✏️ किसी भी उत्तर को संपादित करें",
        "select_field_to_edit": "संपादित करने के लिए फ़ील्ड चुनें:",
        "new_response_for": "'{label}' के लिए नया उत्तर:",
        "updated_successfully": "'{label}' सफलतापूर्वक अपडेट किया गया!",
        "db_save_failed": "रिपोर्ट सहेजने में विफल। कृपया डेटाबेस कनेक्शन की जांच करें।",
        
        # Sidebar language header
        "sidebar_lang_header": "🌐 भाषा चयन",
        "sidebar_options_header": "विकल्प",

        # app.py landing page
        "app_title": "💊 ADR रिपोर्टर AI कॉन्फ़िगरेशन",
        "app_welcome_header": "प्रतिकूल दवा प्रतिक्रिया (ADR) रिपोर्टर AI सिस्टम में आपका स्वागत है",
        "app_welcome_desc": "यह बुद्धिमान सहायक रोगी रिपोर्ट अंतर्ग्रहण और नैदानिक विश्लेषण को स्वचालित और प्रबंधित करता है।",
        "app_sidebar_desc": "मॉड्यूल के बीच नेविगेट करने के लिए कृपया बाईं ओर साइडबार का उपयोग करें:",
        "app_patient_reporter_bullet": "<strong>📝 पेशेंट रिपोर्टर:</strong> प्रतिकूल दवा घटनाओं की चरण-दर-चरण रिपोर्ट करने के लिए रोगियों के लिए एक संवादात्मक बहुभाषी इंटरफ़ेस।",
        "app_dashboard_bullet": "<strong>📊 ओनर डैशबोर्ड:</strong> एकत्रित ADR रिकॉर्ड का निरीक्षण, फ़िल्टर और निर्यात करने के लिए प्रशासकों के लिए एक व्यापक विश्लेषणात्मक डैशबोर्ड।",
        "app_db_success": "डेटाबेस सफलतापूर्वक प्रारंभ किया गया। सुनिश्चित करें कि आपका MySQL सर्वर (जैसे XAMPP) चल रहा है।",

        # dashboard.py translations
        "dash_title": "📊 ओनर डैशबोर्ड",
        "dash_no_reports": "डेटाबेस में कोई रिपोर्ट नहीं मिली। कृपया पहले एक रिपोर्ट सबमिट करें।",
        "dash_filter_reports": "रिपोर्ट फ़िल्टर करें",
        "dash_date_range": "तारीख सीमा",
        "dash_drug_category": "दवा की श्रेणी",
        "dash_gender": "लिंग",
        "dash_key_metrics": "प्रमुख मेट्रिक्स",
        "dash_total_reports": "कुल रिपोर्ट",
        "dash_filtered_reports": "फ़िल्टर की गई रिपोर्ट",
        "dash_top_category": "शीर्ष श्रेणी",
        "dash_analytics": "विश्लेषण",
        "dash_dist_title": "दवा श्रेणी वितरण",
        "dash_gender_split": "लिंग विभाजन",
        "dash_monthly_trend": "रिपोर्टों का मासिक रुझान",
        "dash_month_year": "माह-वर्ष",
        "dash_num_reports": "रिपोर्टों की संख्या",
        "dash_detailed_reports": "विस्तृत रिपोर्ट",
        "dash_download_csv": "📥 फ़िल्टर किया गया डेटा CSV के रूप में डाउनलोड करें",
        "dash_export_view_pdf": "व्यक्तिगत रिपोर्ट निर्यात / देखें (PDF)",
        "dash_select_report_by_id": "PDF के रूप में निर्यात/देखने के लिए रिपोर्ट चुनें (ID द्वारा)",
        "dash_download_pdf": "📥 रिपोर्ट {id} PDF डाउनलोड करें",
        "dash_view_pdf_inline": "👁️ डैशबोर्ड में PDF देखें",
        "dash_pdf_failed": "PDF डेटा प्राप्त करने में विफल।",
        "dash_pdf_gen_error": "PDF जनरेट करने या प्राप्त करने में विफल: {err}",
        "dash_admin_panel": "🗑️ एडमिनिस्ट्रेटर पैनल",
        "dash_admin_actions": "प्रशासक कार्रवाइयां एक्सेस करें",
        "dash_admin_pwd_label": "प्रशासक पासवर्ड दर्ज करें",
        "dash_auth_success": "अधिकृत पहुंच",
        "dash_select_delete_id": "हटाने के लिए रिपोर्ट ID चुनें",
        "dash_confirm_delete": "रिपोर्ट ID {id} को स्थायी रूप से हटाने की पुष्टि करें",
        "dash_btn_delete": "❌ रिपोर्ट स्थायी रूप से हटाएं",
        "dash_delete_success": "रिपोर्ट ID {id} सफलतापूर्वक हटा दी गई!",
        "dash_delete_failed": "डेटाबेस से रिपोर्ट हटाने में विफल।",
        "dash_check_confirm": "आगे बढ़ने के लिए कृपया पुष्टिकरण बॉक्स को चेक करें।",
        "dash_no_delete_avail": "हटाने के लिए कोई रिपोर्ट उपलब्ध नहीं है।",
        "dash_incorrect_pwd": "गलत पासवर्ड। प्रवेश वर्जित।",
        "dash_all": "सभी"
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

        # Navigation and buttons
        "btn_prev": "⬅️ मागील प्रश्न",
        "btn_quit": "🚪 मूल्यांकन बंद करा",
        "confirm_quit_title": "⚠️ मूल्यांकन बंद करण्याची खात्री करा",
        "confirm_quit_desc": "तुम्हाला नक्की बाहेर पडायचे आहे का? तुमची सध्याची प्रगती सेव्ह केली जाईल जेणेकरून तुम्ही नंतर पुन्हा सुरू करू शकाल.",
        "btn_quit_yes": "होय, बाहेर पडा आणि सेव्ह करा",
        "btn_quit_no": "नाही, मूल्यांकन सुरू ठेवा",
        "resume_title": "🔄 मागील मूल्यांकन पुन्हा सुरू करायचे?",
        "resume_desc": "आम्हाला तुमच्या मागील भेटीतील एक अपूर्ण मूल्यांकन आढळले आहे. आपण जिथे सोडले होते तिथून सुरू करू इच्छिता?",
        "btn_resume_yes": "होय, मूल्यांकन पुन्हा सुरू करा",
        "btn_resume_no": "नाही, नवीन मूल्यांकन सुरू करा",
        "current_response": "📝 **{label} साठी सध्याचे उत्तर:** *{ans}*",
        "edit_response_manually": "उत्तर मॅन्युअली एडिट करा:",
        "btn_save_changes": "💾 बदल सेव्ह करा",
        "btn_next_question": "➡️ पुढील प्रश्न",
        "record_answer_for": "🎙️ {label} साठी उत्तर रेकॉर्ड करा:",
        "speak_again_to_replace": "🎙️ उत्तर बदलण्यासाठी पुन्हा बोला / पुन्हा रेकॉर्ड करा:",
        "audio_input_label": "आवाज रेकॉर्ड करा",
        "voice_input_disabled": "🎙️ व्हॉइस इनपुट तात्पुरते अक्षम केले आहे (लापता डिपेंडन्सी). कृपया खाली आपले उत्तर टाईप करा.",
        "transcribing_voice": "🎙️ आवाजाचे भाषांतर होत आहे...",
        "edit_any_response": "✏️ कोणत्याही उत्तरामध्ये बदल करा",
        "select_field_to_edit": "बदल करण्यासाठी क्षेत्र निवडा:",
        "new_response_for": "'{label}' साठी नवीन उत्तर:",
        "updated_successfully": "'{label}' यशस्वीरित्या अपडेट केले!",
        "db_save_failed": "अहवाल सेव्ह करण्यात अयशस्वी. कृपया डेटाबेस कनेक्शन तपासा.",
        
        # Sidebar language header
        "sidebar_lang_header": "🌐 भाषा निवड",
        "sidebar_options_header": "पर्याय",

        # app.py landing page
        "app_title": "💊 ADR रिपोर्टर AI कॉन्फिगरेशन",
        "app_welcome_header": "अ‍ॅडव्हर्स ड्रग रिएक्शन (ADR) रिपोर्टर AI सिस्टीममध्ये आपले स्वागत आहे",
        "app_welcome_desc": "हा बुद्धिमान सहाय्यक रुग्ण अहवाल इनजेशन आणि क्लिनिकल विश्लेषणाचे स्वयंचलित आणि व्यवस्थापन करतो.",
        "app_sidebar_desc": "कृपया मॉड्यूल दरम्यान नेव्हिगेट करण्यासाठी डावीकडील साइडबार वापरा:",
        "app_patient_reporter_bullet": "<strong>📝 पेशंट रिपोर्टर:</strong> रुग्णांना प्रतिकूल औषध घटनांची टप्प्याटप्प्याने अहवाल देण्यासाठी एक संवादात्मक बहुभाषिक इंटरफेस.",
        "app_dashboard_bullet": "<strong>📊 ओनर डॅशबोर्ड:</strong> एकत्रित ADR रेकॉर्डची तपासणी, फिल्टर आणि निर्यात करण्यासाठी प्रशासकांसाठी एक व्यापक विश्लेषणात्मक डॅशबोर्ड.",
        "app_db_success": "डेटाबेस यशस्वीरित्या सुरू झाला. तुमचा MySQL सर्व्हर (उदा. XAMPP) चालू असल्याची खात्री करा.",

        # dashboard.py translations
        "dash_title": "📊 ओनर डॅशबोर्ड",
        "dash_no_reports": "डेटाबेसमध्ये कोणताही अहवाल आढळला नाही. कृपया आधी अहवाल सादर करा.",
        "dash_filter_reports": "अहवाल फिल्टर करा",
        "dash_date_range": "तारीख मर्यादा",
        "dash_drug_category": "औषधाचा वर्ग",
        "dash_gender": "लिंग",
        "dash_key_metrics": "महत्वाचे मोजमाप",
        "dash_total_reports": "एकूण अहवाल",
        "dash_filtered_reports": "फिल्टर केलेले अहवाल",
        "dash_top_category": "शीर्ष औषध वर्ग",
        "dash_analytics": "विश्लेषण",
        "dash_dist_title": "औषध वर्ग वितरण",
        "dash_gender_split": "लिंग विभाजन",
        "dash_monthly_trend": "अहवालांचा मासिक कल",
        "dash_month_year": "महिना-वर्ष",
        "dash_num_reports": "अहवालांची संख्या",
        "dash_detailed_reports": "तपशीलवार अहवाल",
        "dash_download_csv": "📥 फिल्टर केलेला डेटा CSV म्हणून डाउनलोड करा",
        "dash_export_view_pdf": "वैयक्तिक अहवाल निर्यात / पहा (PDF)",
        "dash_select_report_by_id": "PDF म्हणून निर्यात/पाहण्यासाठी अहवाल निवडा (ID द्वारे)",
        "dash_download_pdf": "📥 अहवाल {id} PDF डाउनलोड करा",
        "dash_view_pdf_inline": "👁️ डॅशबोर्डमध्ये PDF पहा",
        "dash_pdf_failed": "PDF डेटा मिळवण्यात अयशस्वी.",
        "dash_pdf_gen_error": "PDF व्युत्पन्न किंवा पुनर्प्राप्त करण्यात अयशस्वी: {err}",
        "dash_admin_panel": "🗑️ अ‍ॅडमिनिस्ट्रेटर पॅनेल",
        "dash_admin_actions": "प्रशासक क्रिया अ‍ॅक्सेस करा",
        "dash_admin_pwd_label": "प्रशासक पासवर्ड प्रविष्ट करा",
        "dash_auth_success": "अधिकृत प्रवेश",
        "dash_select_delete_id": "हटावण्यासाठी अहवाल ID निवडा",
        "dash_confirm_delete": "अहवाल ID {id} कायमचा काढून टाकण्याची पुष्टी करा",
        "dash_btn_delete": "❌ अहवाल कायमचा काढून टाका",
        "dash_delete_success": "अहवाल ID {id} यशस्वीरित्या काढून टाकला!",
        "dash_delete_failed": "डॅशबोर्ड मधून अहवाल काढून टाकण्यास अयशस्वी.",
        "dash_check_confirm": "कृपया पुढे जाण्यासाठी पुष्टीकरण बॉक्स तपासा.",
        "dash_no_delete_avail": "काढून टाकण्यासाठी कोणताही अहवाल उपलब्ध नाही.",
        "dash_incorrect_pwd": "चुकीचा पासवर्ड. प्रवेश नाकारला.",
        "dash_all": "सर्व"
    }
}

def init_language():
    if "language" not in st.session_state or not st.session_state.language:
        st.session_state.language = "English"

def get_current_language():
    init_language()
    return st.session_state.language

def get_text(key, **kwargs):
    lang = get_current_language()
    text = UI_TEXTS[lang].get(key, UI_TEXTS["English"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text

def render_sidebar_language_selector():
    init_language()
    try:
        idx = LANGUAGES.index(st.session_state.language)
    except ValueError:
        idx = 0
    
    st.sidebar.markdown("---")
    header_text = get_text("sidebar_lang_header")
    
    selected_lang = st.sidebar.selectbox(
        header_text,
        LANGUAGES,
        index=idx,
        key="global_language_selector"
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        # Trigger any page-specific reruns or callbacks if needed
        st.rerun()

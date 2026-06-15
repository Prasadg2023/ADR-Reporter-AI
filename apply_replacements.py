import os

file_path = r"C:\Users\hp\OneDrive\Desktop\Pharma4\ADR Reporter AI\pages\1_patient_reporter.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # Summary Editing Expander
    ('with st.expander("✏️ Edit any response"):', 'with st.expander(get_text("edit_any_response")):'),
    ('st.selectbox("Select field to edit:", edit_options, key="select_edit_field")', 'st.selectbox(get_text("select_field_to_edit"), edit_options, key="select_edit_field")'),
    ('new_val_orig = st.text_input(f"New response for \'{selected_edit_label}\':", value=current_val_orig, key=f"edit_input_{key}")', 'new_val_orig = st.text_input(get_text("new_response_for", label=selected_edit_label), value=current_val_orig, key=f"edit_input_{key}")'),
    ('if st.button("💾 Save Changes", use_container_width=True, key=f"save_edit_{key}"):', 'if st.button(get_text("btn_save_changes"), use_container_width=True, key=f"save_edit_{key}"):'),
    ('st.success(f"Updated \'{selected_edit_label}\' successfully!")', 'st.success(get_text("updated_successfully", label=selected_edit_label))'),
    
    # Submit, Restart, Completed Page
    ('if st.button(UI_TEXTS[lang]["btn_submit"], type="primary", use_container_width=True):', 'if st.button(get_text("btn_submit"), type="primary", use_container_width=True):'),
    ('st.error("Failed to save report. Please check database connection.")', 'st.error(get_text("db_save_failed"))'),
    ('if st.button(UI_TEXTS[lang]["btn_restart"], use_container_width=True):', 'if st.button(get_text("btn_restart"), use_container_width=True):'),
    ('st.success(UI_TEXTS[lang]["report_success"])', 'st.success(get_text("report_success"))'),
    ('if st.button(UI_TEXTS[lang]["btn_new"], use_container_width=True):', 'if st.button(get_text("btn_new"), use_container_width=True):')
]

for target, replacement in replacements:
    if target in content:
        content = content.replace(target, replacement)
        print(f"Replaced: {target[:40]}...")
    else:
        print(f"WARNING: Target not found: {target[:40]}...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement complete successfully!")

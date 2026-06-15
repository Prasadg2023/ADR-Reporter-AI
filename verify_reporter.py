import os
import json
import sqlite3
from streamlit.testing.v1 import AppTest

def cleanup():
    # Remove progress file if it exists
    prog_file = "pages/adr_reports_progress.json"
    if os.path.exists(prog_file):
        try:
            os.remove(prog_file)
        except Exception:
            pass
    # Remove SQLite DB if exists to start fresh
    db_file = "adr_reports.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception:
            pass

def test_flow():
    cleanup()
    print("Initializing AppTest...")
    at = AppTest.from_file("pages/1_patient_reporter.py")
    at.run(timeout=10)
    
    # 1. Verify Language Selection
    print("Checking language selection...")
    assert at.session_state.flow_state == "language_selection"
    # Select English (which is the first button in the language select card)
    english_btn = at.button[0]
    assert english_btn.label == "English"
    english_btn.click().run(timeout=10)
    
    # After selecting English, flow should change to chatting, and first question should be active
    assert at.session_state.flow_state == "chatting"
    assert at.session_state.language == "English"
    assert at.session_state.current_q_index == 0
    print("Language selection successful. Flow is chatting.")

    # 2. Verify Keyboard response auto-accept logic
    # Type input via chat input
    print("Sending keyboard response 'John Doe'...")
    at.chat_input[0].set_value("John Doe").run(timeout=10)
    
    # The response should be saved immediately and flow automatically advances to Q2 (index 1)
    print("Answers in session_state:", at.session_state.answers)
    print("Answers original in session_state:", at.session_state.answers_original)
    print("current_q_index:", at.session_state.current_q_index)
    assert at.session_state.answers_original["patient_name"] == "John Doe"
    assert at.session_state.current_q_index == 1
    print("Auto-accept and progression works correctly.")

    # 3. Test Navigation (Previous / Edit Previous Response)
    # Click "Previous Question" button to go back to Q1
    print("Clicking Previous Question...")
    prev_btn = at.button[0] # The button that is rendered when index > 0
    assert "Previous" in prev_btn.label
    prev_btn.click().run(timeout=10)
    
    # Assert we are back to Q1 (index 0)
    assert at.session_state.current_q_index == 0
    
    # Verify that the inline editing card is shown since Q1 has an answer
    # It has a text input with key inline_edit_0
    edit_input = at.text_input("inline_edit_0")
    assert edit_input.value == "John Doe"
    print("Going back displays inline edit block with previous answer.")
    
    # Change answer manually to "Johnathan Doe"
    edit_input.set_value("Johnathan Doe").run(timeout=10)
    
    # Find the Save Changes button
    save_changes_btn = at.button[0] # Save Changes button (since we render it inside column 1 of columns)
    assert "Save Changes" in save_changes_btn.label
    save_changes_btn.click().run(timeout=10)
    
    # Verify it updated and advanced to Q2
    assert at.session_state.answers_original["patient_name"] == "Johnathan Doe"
    assert at.session_state.current_q_index == 1
    print("Inline editing and saving updates response and advances.")

    # Answer Q2 to advance
    at.chat_input[0].set_value("john@example.com").run(timeout=10)
    assert at.session_state.answers["patient_email"] == "john@example.com"
    assert at.session_state.current_q_index == 2

    # 4. Test Quit Assessment and Save Progress
    # The sidebar buttons are accessed via at.sidebar
    quit_btn = at.sidebar.button[1] # Quit button in sidebar
    assert "Quit" in quit_btn.label
    quit_btn.click().run(timeout=10)
    
    # Assert confirmation is shown
    assert at.session_state.confirm_quit is True
    print("Quit confirmation dialog is active.")
    
    # Click Yes, Quit & Save
    yes_quit_btn = at.button[0]
    assert "Yes" in yes_quit_btn.label
    yes_quit_btn.click().run(timeout=10)
    
    # Assert session is cleared and progress file is written
    assert at.session_state.flow_state == "language_selection"
    prog_file = "pages/adr_reports_progress.json"
    assert os.path.exists(prog_file), "Progress file was not written!"
    with open(prog_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        assert saved_data["language"] == "English"
        assert saved_data["current_q_index"] == 2
        assert saved_data["answers_original"]["patient_name"] == "Johnathan Doe"
        assert saved_data["answers"]["patient_email"] == "john@example.com"
    print("Quit & Save saves progress perfectly and clears the session state.")

    # 5. Test Resume Assessment
    print("Testing resume assessment...")
    at2 = AppTest.from_file("pages/1_patient_reporter.py")
    at2.run(timeout=10)
    
    # Check that it asks to resume
    resume_btn = at2.button[0]
    assert "Resume" in resume_btn.label
    resume_btn.click().run(timeout=10)
    
    # Verify we resumed successfully
    assert at2.session_state.flow_state == "chatting"
    assert at2.session_state.language == "English"
    assert at2.session_state.current_q_index == 2
    assert at2.session_state.answers_original["patient_name"] == "Johnathan Doe"
    assert at2.session_state.answers["patient_email"] == "john@example.com"
    print("Resuming previous assessment works perfectly.")

    # 6. Complete remaining questions programmatically to verify summary and edit before submission
    questions_keys = [
        "patient_mobile", "age", "gender", "weight_kg",
        "drug_name", "indication", "medicine_start_date", "medicine_stop_date",
        "reaction_start_date", "reaction_end_date", "reaction_description",
        "drug_category_manual", "route_of_administration", "strength", "frequency",
        "batch_number", "expiry_date", "action_taken", "physician_name", "physician_contact"
    ]
    
    # Set answers directly in session state
    for k in questions_keys:
        if k == "age":
            at2.session_state.answers[k] = 30
            at2.session_state.answers_original[k] = "30"
        else:
            at2.session_state.answers[k] = "Test Val"
            at2.session_state.answers_original[k] = "Test Val"
    
    at2.session_state.current_q_index = 22
    at2.session_state.flow_state = "summary"
    at2.run(timeout=10)
    
    # Verify summary page renders
    assert at2.session_state.flow_state == "summary"
    print("Summary page renders correctly.")
    
    # Verify edit on summary page
    save_edit_btn = at2.button[0] # The Save Changes button inside the expander
    assert "Save" in save_edit_btn.label
    
    # Edit the text input for patient_name (key is edit_input_patient_name)
    at2.text_input("edit_input_patient_name").set_value("Johnathan Edited Doe").run(timeout=10)
    save_edit_btn.click().run(timeout=10)
    
    # Check that value was updated in answers
    assert at2.session_state.answers_original["patient_name"] == "Johnathan Edited Doe"
    print("Editing responses from summary page works correctly.")
    
    # Verify Submission
    submit_btn = at2.button[1] # Submit Report button
    assert "Submit" in submit_btn.label
    submit_btn.click().run(timeout=10)
    
    # After submission, it should be in 'completed' state
    if at2.session_state.flow_state != "completed":
        print("Flow state is:", at2.session_state.flow_state)
        for el in at2:
            val = getattr(el, 'value', None)
            label = getattr(el, 'label', None)
            try:
                print(f"Element {type(el).__name__}: label={label}, value={val}")
            except UnicodeEncodeError:
                print(f"Element {type(el).__name__}: label={repr(label)}, value={repr(val)}")
    assert at2.session_state.flow_state == "completed"
    # Progress file should be deleted
    assert not os.path.exists(prog_file)
    print("Final report submitted successfully. Progress file cleaned up.")
    cleanup()
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_flow()

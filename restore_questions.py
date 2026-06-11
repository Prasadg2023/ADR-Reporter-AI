import json
import re

log_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\ec05e6a2-aa97-41be-a631-a5482709dd7a\.system_generated\logs\transcript.jsonl"

print("Scanning transcript for step 44...")
found = False
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            step_index = data.get("step_index")
            if step_index == 44:
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    args = tc.get("args", {})
                    code = args.get("CodeContent")
                    if code:
                        print("Found code of step 44!")
                        
                        # Extract QUESTIONS block
                        q_match = re.search(r"QUESTIONS = \[(.*?)\]\n\n", code, re.DOTALL)
                        if q_match:
                            questions_str = q_match.group(0)
                            with open("extracted_questions.py", "w", encoding="utf-8") as out:
                                out.write(questions_str)
                            print("Saved QUESTIONS to extracted_questions.py")
                        
                        # Extract UI_TEXTS block
                        ui_match = re.search(r"UI_TEXTS = \{(.*?)\}\n\n", code, re.DOTALL)
                        if ui_match:
                            ui_str = ui_match.group(0)
                            with open("extracted_ui_texts.py", "w", encoding="utf-8") as out:
                                out.write(ui_str)
                            print("Saved UI_TEXTS to extracted_ui_texts.py")
                            
                        # Save the entire code of step 44 to a safe file
                        with open("step44_full_code.py", "w", encoding="utf-8") as out:
                            out.write(code)
                        print("Saved full code of step 44 to step44_full_code.py")
                        
                        found = True
                        break
            if found:
                break
        except Exception as e:
            print("Error parsing line:", e)

if not found:
    print("Could not find step 44.")

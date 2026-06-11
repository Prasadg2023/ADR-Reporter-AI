import json
import os

log_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\ec05e6a2-aa97-41be-a631-a5482709dd7a\.system_generated\logs\transcript.jsonl"
output_file = "pages/1_patient_reporter.py"

print("Scanning transcript for step 44...")
found = False
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            step_index = data.get("step_index")
            # We want step_index 44, or look for write_to_file tool calls
            if step_index == 44:
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    name = tc.get("name")
                    args = tc.get("args", {})
                    code = args.get("CodeContent")
                    if code:
                        print(f"Found CodeContent in step {step_index}!")
                        # Write it back to the original file path!
                        with open(output_file, "w", encoding="utf-8") as out:
                            out.write(code)
                        print("Restored pages/1_patient_reporter.py to step 44 version successfully!")
                        found = True
                        break
            if found:
                break
        except Exception as e:
            print("Error parsing line:", e)

if not found:
    print("Could not restore from step 44 directly. Let's find any tool call that wrote to 1_patient_reporter.py and print the step index.")
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    args = tc.get("args", {})
                    target = args.get("TargetFile", "")
                    if "1_patient_reporter.py" in target and args.get("CodeContent"):
                        print(f"Step {data.get('step_index')} wrote CodeContent of length {len(args.get('CodeContent'))}")
            except Exception:
                pass

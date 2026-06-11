import json
import re

log_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\ec05e6a2-aa97-41be-a631-a5482709dd7a\.system_generated\logs\transcript.jsonl"

print("Scanning log file...")
with open(log_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        try:
            data = json.loads(line)
            step_index = data.get("step_index")
            tool_calls = data.get("tool_calls", [])
            for tc in tool_calls:
                name = tc.get("name")
                args = tc.get("args", {})
                target_file = args.get("TargetFile", "")
                if "1_patient_reporter.py" in target_file:
                    print(f"Step {step_index}: Tool {name}")
                    desc = args.get("Description", "")
                    if desc:
                        print(f"  Description: {desc}")
                    # Look for questions or UI_TEXTS
                    repl = args.get("ReplacementContent", "")
                    if repl:
                        print(f"  ReplacementContent length: {len(repl)}")
                        if "QUESTIONS" in repl or "strength" in repl:
                            print("  Found QUESTIONS/strength in ReplacementContent!")
                            # Save it to a file
                            with open(f"repl_step_{step_index}.txt", "w", encoding="utf-8") as out:
                                out.write(repl)
        except Exception as e:
            pass
print("Scan completed.")

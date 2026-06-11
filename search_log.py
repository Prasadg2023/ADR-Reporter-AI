log_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\ec05e6a2-aa97-41be-a631-a5482709dd7a\.system_generated\logs\transcript.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        if "frequency" in line:
            idx = line.find("frequency")
            start = max(0, idx - 100)
            end = min(len(line), idx + 1000)
            print("FOUND:", line[start:end])

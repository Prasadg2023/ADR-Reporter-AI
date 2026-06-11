with open("pages/1_patient_reporter.py", "rb") as f:
    data = f.read()

# Decode with replacement of invalid characters so it becomes valid UTF-8
decoded = data.decode("utf-8", errors="replace")

with open("decoded_reporter.py", "w", encoding="utf-8") as out:
    out.write(decoded)

print("Decoded file saved to decoded_reporter.py")

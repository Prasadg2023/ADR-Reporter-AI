with open("extracted_view_11.txt", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
reconstructed = []
for l in lines:
    if ":" in l:
        parts = l.split(":", 1)
        if parts[0].strip().isdigit():
            # This is a line from the file view.
            # Strip the line number and the space after the colon
            reconstructed.append(parts[1])

print("Reconstructed lines count:", len(reconstructed))
with open("reconstructed_original.py", "w", encoding="utf-8") as out:
    out.write("\n".join(reconstructed))

# Now let's print lines around 200-300 in reconstructed_original.py
for idx in range(120, min(300, len(reconstructed))):
    print(idx + 1, repr(reconstructed[idx]))

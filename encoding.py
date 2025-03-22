import io

# Adjust "latin-1" to the detected current encoding if needed.
with io.open("trainorig.jsonl", "r", encoding="latin-1") as f:
    data = f.read()

with io.open("train.jsonl", "w", encoding="utf-8") as f:
    f.write(data)

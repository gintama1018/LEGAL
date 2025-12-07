# chunker.py

import os

text = open("constitution.txt", "r", encoding="utf-8").read()

words = text.split()
chunk_size = 300      # 250–300 words per chunk is perfect
chunks = []

for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i+chunk_size])
    chunks.append(chunk)

os.makedirs("chunks", exist_ok=True)

for idx, c in enumerate(chunks):
    with open(f"chunks/chunk_{idx}.txt", "w", encoding="utf-8") as f:
        f.write(c)

print("TOTAL CHUNKS CREATED:", len(chunks))

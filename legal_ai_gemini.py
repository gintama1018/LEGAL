import os
import random
import google.generativeai as genai

# ---------------------------------------------------------
# 1. CONFIGURE YOUR GEMINI API KEY
# ---------------------------------------------------------
genai.configure(api_key="AIzaSyBAL5tDY4hzRU8sFbNBo9bfBkT5nmFqUvU")  # <- apni key yahan


# ---------------------------------------------------------
# 2. LOAD ALL CHUNKS FROM /chunks FOLDER
# ---------------------------------------------------------
chunks = []

chunks_folder = "chunks"
for fname in os.listdir(chunks_folder):
    if fname.endswith(".txt"):
        path = os.path.join(chunks_folder, fname)
        with open(path, "r", encoding="utf-8") as f:
            chunks.append(f.read())

print(f"Loaded {len(chunks)} chunks from Constitution.")


# ---------------------------------------------------------
# 3. SMART CHUNK PICKER (keyword-based, simple but powerful)
# ---------------------------------------------------------
def pick_chunks_for_query(query: str, n: int = 5) -> str:
    """
    Very simple scoring:
    - split query into words
    - each chunk gets +1 score for every word it contains
    - take top-n scoring chunks
    - if all scores zero, fall back to random chunks
    """
    q_words = [w for w in query.lower().split() if len(w) > 3]  # skip tiny words
    scored = []

    for c in chunks:
        text_lower = c.lower()
        score = 0
        for w in q_words:
            if w in text_lower:
                score += 1
        scored.append((score, c))

    # sort by score desc
    scored.sort(key=lambda x: x[0], reverse=True)

    top = [c for s, c in scored[:n] if s > 0]

    # fallback: if nothing matched, just random sample
    if not top:
        top = random.sample(chunks, min(n, len(chunks)))

    return "\n\n---\n\n".join(top)


# ---------------------------------------------------------
# 4. ASK GEMINI A LEGAL QUESTION
# ---------------------------------------------------------
def ask_gemini(question: str) -> str:
    """Original non-streaming version for compatibility"""
    context = pick_chunks_for_query(question, n=5)

    prompt = f"""
You are a highly polished Indian Legal AI Assistant. 
FORMAT THE RESPONSE EXACTLY AS BELOW.
Do NOT change headings or styling.

============================================================
🟦 1. DETECTED ISSUE TYPE
------------------------------------------------------------
Provide a one-line issue classification with a relevant emoji.
Example: 🎓 Education – Exam Blocked due to Fees
============================================================

🟧 2. RELEVANT CONSTITUTIONAL ARTICLES / RIGHTS
------------------------------------------------------------
Format as a clean table:

| Article / Principle | Meaning (1–2 lines) | From Constitution Text? |
|--------------------|----------------------|--------------------------|
| **Article 21**     | Right to life, dignity, continuity of education | ❌ Not in provided text — using general legal principles |
| **Art 21A**        | Right to education (spirit applied to fairness) | ❌ Not in provided text |

If no article appears in text, clearly say:
"Articles not found in given chunks — applying general Indian legal principles."

============================================================

🟩 3. USER'S LEGAL RIGHTS (Simplified)
------------------------------------------------------------
Use clean bullet points with icons:

✔️ Right 1  
✔️ Right 2  
⚠️ Warning point  
ℹ️ Helpful info  

Make rights very easy to understand.

============================================================

🟪 4. STEPS THE USER SHOULD TAKE (Action Plan)
------------------------------------------------------------
Format as numbered list:

1. **Step Title** – 1–2 line explanation  
2. **Step Title** – explanation  
3. **Step Title** – explanation  

THEN add a sub-section:

**❌ What to Avoid:**  
- short bullet  
- short bullet  

============================================================

🟨 5. FORMAL COMPLAINT / FIR DRAFT
------------------------------------------------------------
Use bold headings, line breaks and placeholders:

**To,**  
The Principal / Registrar  
[College Name], [Address]

**Subject:** Request to allow exam appearance despite fee issue.

**Respected Sir/Madam,**  
[Body paragraphs formatted cleanly, with spacing]

**Sincerely,**  
[Your Name]  
[Contact]  
[Date]

============================================================

🟥 6. URGENCY SCORE
------------------------------------------------------------
Format EXACTLY like:

⭐ **Urgency: 8/10**  
Short justification (1 line).

============================================================

NOW ANSWER USING THIS FORMAT ONLY.

Below is the Constitution text for reference. Use it strictly.

=========================
CONSTITUTION TEXT:
{context}
=========================

USER QUESTION:
{question}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)
    return response.text


def ask_gemini_stream(question: str):
    """STREAMING VERSION - ChatGPT-like typing effect"""
    context = pick_chunks_for_query(question, n=5)

    prompt = f"""
You are a highly polished Indian Legal AI Assistant. 
FORMAT THE RESPONSE EXACTLY AS BELOW.
Do NOT change headings or styling.

============================================================
🟦 1. DETECTED ISSUE TYPE
------------------------------------------------------------
Provide a one-line issue classification with a relevant emoji.
Example: 🎓 Education – Exam Blocked due to Fees
============================================================

🟧 2. RELEVANT CONSTITUTIONAL ARTICLES / RIGHTS
------------------------------------------------------------
Format as a clean table:

| Article / Principle | Meaning (1–2 lines) | From Constitution Text? |
|--------------------|----------------------|--------------------------|
| **Article 21**     | Right to life, dignity, continuity of education | ❌ Not in provided text — using general legal principles |
| **Art 21A**        | Right to education (spirit applied to fairness) | ❌ Not in provided text |

If no article appears in text, clearly say:
"Articles not found in given chunks — applying general Indian legal principles."

============================================================

🟩 3. USER'S LEGAL RIGHTS (Simplified)
------------------------------------------------------------
Use clean bullet points with icons:

✔️ Right 1  
✔️ Right 2  
⚠️ Warning point  
ℹ️ Helpful info  

Make rights very easy to understand.

============================================================

🟪 4. STEPS THE USER SHOULD TAKE (Action Plan)
------------------------------------------------------------
Format as numbered list:

1. **Step Title** – 1–2 line explanation  
2. **Step Title** – explanation  
3. **Step Title** – explanation  

THEN add a sub-section:

**❌ What to Avoid:**  
- short bullet  
- short bullet  

============================================================

🟨 5. FORMAL COMPLAINT / FIR DRAFT
------------------------------------------------------------
Use bold headings, line breaks and placeholders:

**To,**  
The Principal / Registrar  
[College Name], [Address]

**Subject:** Request to allow exam appearance despite fee issue.

**Respected Sir/Madam,**  
[Body paragraphs formatted cleanly, with spacing]

**Sincerely,**  
[Your Name]  
[Contact]  
[Date]

============================================================

🟥 6. URGENCY SCORE
------------------------------------------------------------
Format EXACTLY like:

⭐ **Urgency: 8/10**  
Short justification (1 line).

============================================================

NOW ANSWER USING THIS FORMAT ONLY.

Below is the Constitution text for reference. Use it strictly.

=========================
CONSTITUTION TEXT:
{context}
=========================

USER QUESTION:
{question}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    print("\n🤖 AI is typing...\n")

    full_text = ""

    # STREAMING: Words appear LIVE like ChatGPT
    for chunk in model.generate_content(prompt, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)  # LIVE TYPING EFFECT
            full_text += chunk.text                # Store complete response

    print("\n")  # New line after completion
    return full_text


# ---------------------------------------------------------
# 5. TESTING THE SYSTEM (CLI)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n=== Legal AI System Ready (STREAMING MODE) ===\n")

    user_question = input("Enter your legal question: ")

    print("\n\n=== AI RESPONSE (LIVE STREAMING) ===\n")
    answer = ask_gemini_stream(user_question)  # STREAMING VERSION

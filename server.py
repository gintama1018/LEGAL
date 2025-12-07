from flask import Flask, request, jsonify, Response, stream_with_context, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import google.generativeai as genai

# Import all AI modules
from legal_ai_gemini import ask_gemini, pick_chunks_for_query
from multi_agent_system import multi_agent_response
from emotional_safety import safe_response, detect_crisis
from pdf_analyzer import extract_text_from_pdf, analyze_legal_document

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# PDF upload config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ROUTE 0: Serve the HTML frontend
@app.route("/")
def home():
    return send_file("index.html")


# ROUTE 1: Simple AI (Original - Non-streaming)
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    
    # Use emotional safety wrapper
    answer = safe_response(question, ask_gemini)
    return jsonify({"response": answer})


# ROUTE 1B: STREAMING VERSION (ChatGPT-like live typing)
@app.route("/ask-stream", methods=["POST"])
def ask_stream():
    data = request.json
    question = data.get("question", "")
    
    # Check for crisis first
    crisis_info = detect_crisis(question)
    
    def generate():
        """Generator function for SSE streaming"""
        
        if crisis_info['is_crisis']:
            # For crisis, send emergency info first
            yield f"data: {json.dumps({'chunk': '🆘 CRISIS SUPPORT ACTIVATED\\n\\n'})}\n\n"
            # Then continue with full response (non-streamed for crisis)
            from emotional_safety import generate_crisis_response
            full_response = generate_crisis_response(question, crisis_info)
            yield f"data: {json.dumps({'chunk': full_response})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
            return
        
        # Normal streaming for non-crisis questions
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
        
        # Stream chunks as they arrive
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                yield f"data: {json.dumps({'chunk': chunk.text})}\n\n"
        
        # Signal completion
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return Response(stream_with_context(generate()), 
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'X-Accel-Buffering': 'no'
                    })


# ROUTE 2: Multi-Agent System (UPGRADE 2)
@app.route("/multi-agent", methods=["POST"])
def multi_agent():
    data = request.json
    question = data.get("question", "")
    
    # Use emotional safety + multi-agent
    answer = safe_response(question, multi_agent_response)
    return jsonify({"response": answer})


# ROUTE 3: PDF Document Analysis (UPGRADE 1)
@app.route("/analyze-pdf", methods=["POST"])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    question = request.form.get('question', 'Analyze this document and explain my rights')
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract and analyze
        pdf_text = extract_text_from_pdf(filepath)
        analysis = analyze_legal_document(pdf_text, question)
        
        # Cleanup
        os.remove(filepath)
        
        return jsonify({"response": analysis})
    
    return jsonify({"error": "Invalid file type. Only PDF allowed"}), 400


if __name__ == "__main__":
    app.run(debug=True)

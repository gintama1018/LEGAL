import PyPDF2
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from uploaded PDF document
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def analyze_legal_document(pdf_text: str, user_question: str) -> str:
    """
    Analyze legal document and provide actionable steps
    """
    import google.generativeai as genai
    
    prompt = f"""
You are analyzing a legal document uploaded by a user.
FORMAT YOUR RESPONSE IN PREMIUM STYLE AS SHOWN BELOW.

DOCUMENT CONTENT:
{pdf_text[:8000]}  

USER'S QUESTION/CONCERN:
{user_question}

FORMAT YOUR RESPONSE EXACTLY AS:

============================================================
📄 DOCUMENT ANALYSIS
============================================================

🟦 DOCUMENT SUMMARY
------------------------------------------------------------
2-3 line overview of what this document is about.

============================================================

🟧 KEY LEGAL POINTS FOUND
------------------------------------------------------------
Format as table if applicable, or bullet points:

✔️ Point 1  
✔️ Point 2  
⚠️ Important clause  
ℹ️ Note  

============================================================

🟩 USER'S RIGHTS BASED ON THIS DOCUMENT
------------------------------------------------------------
✔️ Right 1 - explanation  
✔️ Right 2 - explanation  
⚠️ Warning/limitation  

============================================================

🟪 ACTION STEPS (What User Should Do Next)
------------------------------------------------------------
1. **Step Title** - explanation  
2. **Step Title** - explanation  
3. **Step Title** - explanation  

**❌ What to Avoid:**  
- bullet  
- bullet  

============================================================

🟨 COMPLAINT/RESPONSE DRAFT (Copy-Paste Ready)
------------------------------------------------------------
**To,**  
[Authority/Recipient]  
[Address]

**Subject:** [Subject line]

**Respected Sir/Madam,**

[Well-formatted body with proper spacing]

**Sincerely,**  
[Your Name]  
[Contact]  
[Date]

============================================================

⭐ URGENCY ASSESSMENT
------------------------------------------------------------
⭐ **Urgency: X/10**  
Brief reason.

============================================================

Keep response practical, professional, and actionable.
"""
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

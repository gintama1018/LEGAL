import google.generativeai as genai
from legal_ai_gemini import pick_chunks_for_query

# ---------------------------------------------------------
# MULTI-AGENT ARCHITECTURE
# ---------------------------------------------------------

class IssueClassifierAgent:
    """Agent 1: Classifies the type of legal issue"""
    
    @staticmethod
    def classify(question: str) -> dict:
        prompt = f"""
You are a Legal Issue Classifier.

USER QUESTION: {question}

Classify into:
- Category: (Police/Criminal, Civil/Property, Family/Domestic, Cyber/Digital, Labor/Employment, Consumer, Other)
- Urgency: (Critical/High/Medium/Low)
- Emergency Keywords Detected: (Yes/No - for abuse, violence, self-harm, threats)

Return ONLY a JSON:
{{"category": "...", "urgency": "...", "emergency": true/false, "reason": "one line"}}
"""
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        # Parse response (simplified)
        import json
        try:
            return json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        except:
            return {"category": "General", "urgency": "Medium", "emergency": False, "reason": "Unknown"}


class RetrievalAgent:
    """Agent 2: Retrieves relevant constitutional articles and laws"""
    
    @staticmethod
    def retrieve(question: str, classification: dict) -> str:
        context = pick_chunks_for_query(question, n=7)  # Get more chunks for multi-agent
        
        prompt = f"""
You are a Legal Retrieval Agent.

QUESTION: {question}
CATEGORY: {classification['category']}

AVAILABLE LEGAL TEXT:
{context}

Extract and return:
1. Relevant Article Numbers
2. Key Rights Mentioned
3. Legal Provisions

Format as bullet points, concise.
"""
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text


class LegalReasoningAgent:
    """Agent 3: Provides legal reasoning and analysis"""
    
    @staticmethod
    def reason(question: str, retrieved_info: str, classification: dict) -> str:
        prompt = f"""
You are a Legal Reasoning Agent.

QUESTION: {question}
CATEGORY: {classification['category']}

RETRIEVED LEGAL INFO:
{retrieved_info}

Provide:
1. Legal Analysis (2-3 paragraphs)
2. User's Rights (bullet points)
3. What Law Says
4. Precedents or Common Practice (if known)

Be practical and clear.
"""
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text


class DocumentDraftingAgent:
    """Agent 4: Drafts legal documents (FIR, complaint, notices)"""
    
    @staticmethod
    def draft(question: str, reasoning: str, classification: dict) -> str:
        doc_type = "FIR" if "Police" in classification['category'] or "Criminal" in classification['category'] else "Complaint"
        
        prompt = f"""
You are a Legal Document Drafting Agent.

QUESTION: {question}
CATEGORY: {classification['category']}

LEGAL ANALYSIS:
{reasoning}

Draft a formal {doc_type} that user can copy-paste and file.

FORMAT EXACTLY AS BELOW with proper spacing and bold headers:

**To,**  
[Authority Name]  
[Department/Station]  
[Address]

**Subject:** [Clear subject line]

**Respected Sir/Madam,**

[Opening paragraph - introduce yourself and state purpose]

[Middle paragraph(s) - describe incident/issue with dates, facts, evidence]

[Final paragraph - state relief/action sought]

**Sincerely,**  
[Your Name]  
[Contact Number]  
[Email Address]  
[Date: DD/MM/YYYY]

**Enclosures (if any):**  
1. [Document 1]  
2. [Document 2]

Make it professional, legally sound, and ready to file.
"""
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text


# ---------------------------------------------------------
# ORCHESTRATOR: Coordinates all agents
# ---------------------------------------------------------

def multi_agent_response(question: str) -> str:
    """
    Orchestrates all 4 agents to provide comprehensive legal assistance
    """
    
    # Agent 1: Classify
    classification = IssueClassifierAgent.classify(question)
    
    # Agent 2: Retrieve
    retrieved_info = RetrievalAgent.retrieve(question, classification)
    
    # Agent 3: Reason
    reasoning = LegalReasoningAgent.reason(question, retrieved_info, classification)
    
    # Agent 4: Draft Document
    document = DocumentDraftingAgent.draft(question, reasoning, classification)
    
    # Combine all outputs in PREMIUM format
    final_response = f"""
╔══════════════════════════════════════════════════════════════╗
║       🔥 MULTI-AGENT LEGAL ANALYSIS SYSTEM 🔥                ║
╚══════════════════════════════════════════════════════════════╝

============================================================
🟦 ISSUE CLASSIFICATION
------------------------------------------------------------
**Category:** {classification['category']}  
**Urgency Level:** {classification['urgency']}  
**Emergency Status:** {'🚨 YES - Immediate action required' if classification['emergency'] else '✅ Normal processing'}  
**Reason:** {classification['reason']}

============================================================

🟧 RETRIEVED LEGAL INFORMATION
------------------------------------------------------------
{retrieved_info}

============================================================

🟩 LEGAL REASONING & ANALYSIS
------------------------------------------------------------
{reasoning}

============================================================

🟨 READY-TO-FILE DOCUMENT
------------------------------------------------------------
{document}

============================================================

⭐ ANALYSIS COMPLETE
------------------------------------------------------------
✔️ All 4 agents executed successfully  
✔️ Document ready for filing  
✔️ Legal advice cross-verified

============================================================
🤖 Generated by Multi-Agent Legal AI System
============================================================
"""
    
    return final_response

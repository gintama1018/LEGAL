import re

# ---------------------------------------------------------
# EMOTIONAL SAFETY & CRISIS DETECTION MODULE
# ---------------------------------------------------------

CRISIS_KEYWORDS = {
    'self_harm': [
        'suicide', 'kill myself', 'end my life', 'want to die', 
        'no reason to live', 'better off dead', 'self harm'
    ],
    'domestic_violence': [
        'domestic violence', 'husband beats', 'wife beating', 
        'physical abuse', 'beaten by', 'dowry harassment',
        'threatened to kill', 'acid attack', 'domestic abuse'
    ],
    'sexual_assault': [
        'rape', 'sexual assault', 'molested', 'sexual harassment',
        'eve teasing', 'stalking', 'groping', 'sexual violence'
    ],
    'child_abuse': [
        'child abuse', 'child marriage', 'minor', 'underage',
        'child trafficking', 'child labor'
    ]
}

EMERGENCY_CONTACTS = """
🆘 NATIONAL EMERGENCY HELPLINES (INDIA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Police Emergency: 100
📞 Women Helpline: 181
📞 Domestic Violence Helpline: 181
📞 Child Helpline: 1098
📞 Mental Health Helpline (Vandrevala): 1860-2662-345
📞 Suicide Prevention (iCall): 9152987821
📞 Cyber Crime Helpline: 1930

🏥 IMMEDIATE ACTIONS:
1. You are NOT alone - help is available 24/7
2. Call the helpline numbers above RIGHT NOW
3. If in danger, call 100 (Police) immediately
4. Go to nearest police station or hospital
5. Contact trusted friend/family member

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def detect_crisis(question: str) -> dict:
    """
    Detects if question indicates emotional crisis or emergency
    Returns: {is_crisis: bool, crisis_type: str, severity: int}
    """
    question_lower = question.lower()
    
    detected_types = []
    
    for crisis_type, keywords in CRISIS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in question_lower:
                detected_types.append(crisis_type)
                break
    
    if detected_types:
        return {
            'is_crisis': True,
            'crisis_type': detected_types,
            'severity': 10 if 'self_harm' in detected_types else 9
        }
    
    return {'is_crisis': False, 'crisis_type': [], 'severity': 0}


def generate_crisis_response(question: str, crisis_info: dict) -> str:
    """
    Generates empathetic, actionable crisis response
    """
    import google.generativeai as genai
    
    crisis_types_str = ", ".join(crisis_info['crisis_type'])
    
    prompt = f"""
You are a compassionate Legal + Mental Health Crisis Assistant.

USER'S SITUATION (SENSITIVE):
{question}

DETECTED CRISIS: {crisis_types_str}

Respond with:

1. **Immediate Empathy & Validation**
   - Acknowledge their pain
   - "You are not alone, help is available"
   - Non-judgmental tone

2. **Emergency Actions (RIGHT NOW)**
   - Call specific helpline
   - Go to police/hospital if in danger
   - Contact trusted person

3. **Legal Rights (Simple Points)**
   - What law protects them
   - Their immediate rights
   
4. **Step-by-Step Safety Plan**
   - What to do in next 1 hour
   - What to do in next 24 hours
   - How to stay safe

5. **Document to File (if applicable)**
   - FIR/Complaint draft
   - Evidence to collect

IMPORTANT:
- Be warm, empathetic, non-judgmental
- Prioritize SAFETY over legal process
- Encourage professional help
- Never minimize their situation

Keep language simple, supportive, actionable.
"""
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    # Add emergency contacts at top
    crisis_response = f"""
╔══════════════════════════════════════════════════════════════╗
║     ⚠️  CRISIS SUPPORT ACTIVATED - YOU ARE NOT ALONE  ⚠️      ║
╚══════════════════════════════════════════════════════════════╝

{EMERGENCY_CONTACTS}

💙 YOUR SITUATION MATTERS - HERE'S WHAT YOU CAN DO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{response.text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ Remember: Your safety and wellbeing come FIRST. Legal steps come second.
💪 You deserve help, protection, and dignity.
📞 Please reach out to the helplines above - they are trained to help.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return crisis_response


def safe_response(question: str, normal_ai_function) -> str:
    """
    Wrapper function that checks for crisis before normal AI processing
    """
    crisis_info = detect_crisis(question)
    
    if crisis_info['is_crisis']:
        return generate_crisis_response(question, crisis_info)
    else:
        # Normal AI processing
        return normal_ai_function(question)

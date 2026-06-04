from ..groq_service import ask_groq

SYSTEM_PROMPT = """
You are a health risk assessment agent.

Classify the urgency/risk of the user's symptoms. Do not diagnose the user
or claim that symptoms belong to one disease only. Many conditions can share
the same symptoms, so provide possible cases/causes as a differential list.

Risk levels:

LOW
MEDIUM
HIGH
CRITICAL

Return:

Risk Level
Risk Score (0-100)
Possible Cases/Causes
Reason
Next Step

Include a short note that this is AI-assisted risk awareness, not a medical
diagnosis.
"""

def assess_risk(text):

    return ask_groq(
        SYSTEM_PROMPT,
        text
    )

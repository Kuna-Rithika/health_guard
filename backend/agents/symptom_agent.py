from ..groq_service import ask_groq

SYSTEM_PROMPT = """
You are a medical symptom extraction agent.

Extract:

1. Symptoms
2. Severity
3. Duration
4. Body Location

Return JSON only.
"""

def extract_symptoms(text):

    result = ask_groq(
        SYSTEM_PROMPT,
        text
    )

    return result
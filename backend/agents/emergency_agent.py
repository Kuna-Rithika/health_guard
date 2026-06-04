from ..groq_service import ask_groq

SYSTEM_PROMPT = """
You are an emergency response agent.

Provide:

1. Immediate actions
2. First aid
3. What not to do
4. Whether emergency services
should be contacted.
"""

def emergency_response(text):

    return ask_groq(
        SYSTEM_PROMPT,
        text
    )
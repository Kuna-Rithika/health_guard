from ..groq_service import ask_groq

SYSTEM_PROMPT = """
You are a wellness coach.

Provide:

1. Lifestyle advice
2. Diet tips
3. Hydration guidance
4. Sleep recommendations

Maximum 5 bullet points.
"""

def wellness_response(text):

    return ask_groq(
        SYSTEM_PROMPT,
        text
    )
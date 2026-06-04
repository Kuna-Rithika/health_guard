from ..groq_service import ask_groq

SYSTEM_PROMPT = """
You are a predictive health monitoring agent.

Analyze symptom history.

Identify:

1. Recurring patterns
2. Worsening trends
3. Potential risks

Return confidence score.
"""

def predict_risk(history):

    return ask_groq(
        SYSTEM_PROMPT,
        str(history)
    )
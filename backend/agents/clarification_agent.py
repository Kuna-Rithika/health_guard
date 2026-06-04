import json
import re

from ..groq_service import ask_groq

SYSTEM_PROMPT = """
You are a medical clarification agent.

Generate 3 to 5 follow-up questions that would help a doctor understand
the condition better.

Return JSON only in this exact format:
{
  "questions": [
    "question 1",
    "question 2",
    "question 3"
  ]
}
"""

FALLBACK_QUESTIONS = [
    "How long have you been experiencing these symptoms?",
    "How severe are the symptoms on a scale of 1 to 10?",
    "Do you have any other symptoms, medical conditions, or recent triggers?",
]


def _extract_questions(result):
    if not result or result.startswith("ERROR:"):
        return FALLBACK_QUESTIONS

    try:
        parsed = json.loads(result)
        questions = parsed.get("questions", [])
    except json.JSONDecodeError:
        questions = []

        for line in result.splitlines():
            cleaned = re.sub(r"^\s*[-*\d.)]+\s*", "", line).strip()
            if cleaned.endswith("?"):
                questions.append(cleaned)

    questions = [
        question.strip()
        for question in questions
        if isinstance(question, str) and question.strip()
    ]

    if len(questions) < 3:
        questions.extend(
            question for question in FALLBACK_QUESTIONS if question not in questions
        )

    return questions[:5]


def clarification_questions(text):
    result = ask_groq(
        SYSTEM_PROMPT,
        text
    )

    return _extract_questions(result)

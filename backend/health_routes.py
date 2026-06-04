from fastapi import APIRouter
from pydantic import BaseModel, Field
import sqlite3
import re

from .orchestrator import run_healthguard_pipeline
from .agents.clarification_agent import clarification_questions

router = APIRouter()

DB_NAME = "healthguard.db"


class AnalyzeRequest(BaseModel):
    user_id: int
    symptoms: str
    clarification_answers: list[dict[str, str]] = Field(default_factory=list)


class ClarifyRequest(BaseModel):
    user_id: int
    symptoms: str


def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


def parse_risk_assessment(risk_text: str):
    text = str(risk_text or "")
    upper_text = text.upper()

    risk_level = "UNKNOWN"
    for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        if re.search(rf"\b{level}\b", upper_text):
            risk_level = level
            break

    score = 50
    score_match = re.search(r"Risk Score\s*[:\-]?\s*(\d{1,3})", text, re.IGNORECASE)
    if not score_match:
        score_match = re.search(r"\b(\d{1,3})\s*/\s*100\b", text)

    if score_match:
        score = max(0, min(100, int(score_match.group(1))))

    return risk_level, score


@router.post("/analyze")
def analyze_health(data: AnalyzeRequest):

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # Load History
    # ==========================

    rows = cursor.execute(
        """
        SELECT symptoms
        FROM symptom_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 7
        """,
        (data.user_id,)
    ).fetchall()

    history = []

    for row in rows:
        history.append(row["symptoms"])

    # ==========================
    # Run AI Pipeline
    # ==========================

    result = run_healthguard_pipeline(
        data.symptoms,
        history,
        data.clarification_answers
    )

    # ==========================
    # Save Session
    # ==========================

    risk_text = str(
        result["report"]["risk_assessment"]
    )
    risk_level, risk_score = parse_risk_assessment(risk_text)

    cursor.execute(
        """
        INSERT INTO symptom_history(
            user_id,
            symptoms,
            risk_level,
            risk_score,
            ai_summary
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data.user_id,
            data.symptoms,
            risk_level,
            risk_score,
            risk_text
        )
    )

    conn.commit()

    conn.close()

    return result


@router.post("/clarify")
def clarify_health(data: ClarifyRequest):
    questions = clarification_questions(data.symptoms)

    return {
        "success": True,
        "questions": questions
    }

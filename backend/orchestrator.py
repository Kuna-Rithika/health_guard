from .agents.security_agent import security_check
from .agents.symptom_agent import extract_symptoms
from .agents.clarification_agent import clarification_questions
from .agents.pattern_agent import detect_patterns
from .agents.risk_agent import assess_risk
from .agents.predictive_agent import predict_risk
from .agents.emergency_agent import emergency_response
from .agents.wellness_agent import wellness_response


def _build_clinical_context(user_input, clarification_answers=None):
    if not clarification_answers:
        return user_input

    answer_lines = []
    for item in clarification_answers:
        question = item.get("question", "").strip()
        answer = item.get("answer", "").strip()
        if question and answer:
            answer_lines.append(f"Q: {question}\nA: {answer}")

    if not answer_lines:
        return user_input

    return (
        f"Initial symptoms:\n{user_input}\n\n"
        f"Clarification answers:\n" + "\n\n".join(answer_lines)
    )


def run_healthguard_pipeline(user_input, history=None, clarification_answers=None):
    if history is None:
        history = []

    report = {}

    # =====================================================
    # AGENT 0 - SECURITY
    # =====================================================

    security_result = security_check(user_input)

    if not security_result["safe"]:

        return {
            "success": False,
            "error": security_result["message"]
        }

    clean_text = security_result["clean_text"]
    clinical_context = _build_clinical_context(clean_text, clarification_answers)

    report["security"] = "Passed"

    # =====================================================
    # AGENT 1 - SYMPTOM COLLECTION
    # =====================================================

    symptom_data = extract_symptoms(clinical_context)

    report["symptoms"] = symptom_data

    # =====================================================
    # AGENT 2 - CLARIFICATION
    # =====================================================

    if clarification_answers:
        clarification = clarification_answers
    else:
        clarification = clarification_questions(clean_text)

    report["clarification_questions"] = clarification

    # =====================================================
    # AGENT 3 - PATTERN DETECTION
    # =====================================================

    patterns = detect_patterns(history)

    report["patterns"] = patterns

    # =====================================================
    # AGENT 4 - RISK ASSESSMENT
    # =====================================================

    risk_result = assess_risk(clinical_context)

    report["risk_assessment"] = risk_result

    # =====================================================
    # AGENT 5 - PREDICTION
    # =====================================================

    prediction = predict_risk(history)

    report["prediction"] = prediction

    # =====================================================
    # DETERMINE FINAL PATH
    # =====================================================

    risk_text = str(risk_result).upper()

    if "CRITICAL" in risk_text or "HIGH" in risk_text:

        emergency = emergency_response(clinical_context)

        report["route"] = "EMERGENCY"

        report["final_response"] = emergency

    else:

        wellness = wellness_response(clinical_context)

        report["route"] = "WELLNESS"

        report["final_response"] = wellness

    return {
        "success": True,
        "report": report
    }

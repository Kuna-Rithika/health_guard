const API_URL = "https://health-guard-caq0.onrender.com";

async function analyzeSymptoms(userId, symptoms) {
    return analyzeSymptomsWithAnswers(userId, symptoms, []);
}

async function getClarificationQuestions(userId, symptoms) {
    const response = await fetch(
        `${API_URL}/clarify`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                symptoms: symptoms
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        return {
            error: data.error || data.detail || `Server error: ${response.status}`
        };
    }

    return data;
}

async function analyzeSymptomsWithAnswers(userId, symptoms, clarificationAnswers) {

    const response = await fetch(
        `${API_URL}/analyze`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                symptoms: symptoms,
                clarification_answers: clarificationAnswers
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        return {
            error: data.error || data.detail || `Server error: ${response.status}`
        };
    }

    return data;
}

const API_URL =
"https://healthguard-backend-reg8.onrender.com";

function setResult(content) {
    const resultEl = document.getElementById('result');
    if (!resultEl) return;
    resultEl.innerHTML = content;
}

let clarificationState = {
    stage: 'initial',
    symptoms: '',
    questions: []
};

async function submitSymptoms() {
    const symptoms = document.getElementById('symptomInput')?.value?.trim();
    const userId = localStorage.getItem('user_id');

    if (!userId) {
        window.location.href = 'login.html';
        return;
    }

    if (!symptoms) {
        setResult('<p>Please enter your symptoms before analyzing.</p>');
        return;
    }

    if (clarificationState.stage === 'clarifying') {
        await submitClarifiedSymptoms(userId, symptoms);
        return;
    }

    await requestClarification(userId, symptoms);
}

async function requestClarification(userId, symptoms) {
    setResult('<p>Analyzing symptoms, please wait...</p>');

    try {
        const data = await getClarificationQuestions(userId, symptoms);
        if (!data) {
            setResult('<p>Clarification failed: No response received.</p>');
            return;
        }

        if (data.error) {
            setResult(`<p>${data.error}</p>`);
            return;
        }

        if (data.success && Array.isArray(data.questions) && data.questions.length >= 3) {
            clarificationState = {
                stage: 'clarifying',
                symptoms,
                questions: data.questions.slice(0, 5)
            };
            setResult(renderClarificationForm(clarificationState.questions));
            setAnalyzeButtonText('Analyze With Answers');
            const statusEl = document.getElementById('healthStatus');
            if (statusEl) statusEl.innerText = 'Please answer the clarification questions.';
            return;
        }

        setResult('<p>Could not generate clarification questions. Please try again.</p>');
    } catch (error) {
        console.error(error);
        setResult('<p>Unable to generate clarification questions at this time. Please try again.</p>');
    }
}

async function submitClarifiedSymptoms(userId, currentSymptoms) {
    const answers = collectClarificationAnswers();

    if (answers.some((item) => !item.answer)) {
        setResult(`
            ${renderClarificationForm(clarificationState.questions, answers)}
            <p class="form-error">Please answer all clarification questions before analyzing.</p>
        `);
        return;
    }

    const symptoms = currentSymptoms || clarificationState.symptoms;
    setResult('<p>Running pattern detection and full health analysis...</p>');

    try {
        const data = await analyzeSymptomsWithAnswers(userId, symptoms, answers);
        if (!data) {
            setResult('<p>Analysis failed: No response received.</p>');
            return;
        }

        if (data.error) {
            setResult(`<p>${data.error}</p>`);
            return;
        }

        if (data.success && data.report) {
            setResult(renderAgentReport(data.report));
            resetClarificationState();
            const statusEl = document.getElementById('healthStatus');
            if (statusEl) statusEl.innerText = 'Analysis complete';
            return;
        }

        setResult(`<pre>${JSON.stringify(data, null, 2)}</pre>`);
    } catch (error) {
        console.error(error);
        setResult('<p>Unable to analyze symptoms at this time. Please try again.</p>');
    }
}

function renderClarificationForm(questions, existingAnswers = []) {
    const answerByQuestion = existingAnswers.reduce((acc, item) => {
        acc[item.question] = item.answer;
        return acc;
    }, {});

    const fields = questions
        .map((question, index) => {
            const safeQuestion = escapeHtml(question);
            const savedAnswer = escapeHtml(answerByQuestion[question] || '');

            return `
                <div class="clarification-item">
                    <label for="clarificationAnswer${index}">
                        ${index + 1}. ${safeQuestion}
                    </label>
                    <textarea
                        id="clarificationAnswer${index}"
                        class="clarification-answer"
                        data-question="${safeQuestion}"
                        rows="3"
                        placeholder="Type your answer..."
                    >${savedAnswer}</textarea>
                </div>
            `;
        })
        .join('');

    return `
        <div class="clarification-form">
            <h3>Clarification Questions</h3>
            ${fields}
        </div>
    `;
}

function collectClarificationAnswers() {
    return Array.from(document.querySelectorAll('.clarification-answer')).map((input) => ({
        question: input.dataset.question,
        answer: input.value.trim()
    }));
}

function renderAgentReport(report) {
    const order = [
        'security',
        'symptoms',
        'clarification_questions',
        'patterns',
        'risk_assessment',
        'prediction',
        'route',
        'final_response'
    ];

    const names = {
        security: 'Security Check',
        symptoms: 'Symptom Extraction',
        clarification_questions: 'Clarification Questions',
        patterns: 'Pattern Detection',
        risk_assessment: 'Risk Assessment',
        possible_cases: 'Possible Cases',
        prediction: 'Predictive Risk Analysis',
        route: 'Decision Route',
        final_response: 'Final AI Response'
    };

    const sections = order
        .filter((key) => key in report)
        .map((key) => {
            return `
                <div class="agent-block">
                    <h3>${names[key] || key}</h3>
                    <div class="agent-output">${formatAgentValue(report[key])}</div>
                </div>
            `;
        })
        .join('');

    return `
        <div class="agent-report">
            ${sections}
        </div>
    `;
}

function formatAgentValue(value) {
    if (value === null || value === undefined) {
        return '<em>No data returned.</em>';
    }

    if (typeof value === 'string') {
        return `<div class="formatted-text">${formatMedicalText(value)}</div>`;
    }

    if (typeof value === 'number' || typeof value === 'boolean') {
        return `<pre>${value}</pre>`;
    }

    if (Array.isArray(value)) {
        return `
            <ul>
                ${value.map((item) => `<li>${formatAgentValue(item)}</li>`).join('')}
            </ul>
        `;
    }

    if (typeof value === 'object') {
        return `
            <div class="object-block">
                ${Object.entries(value)
                    .map(
                        ([key, val]) =>
                            `<div><strong>${escapeHtml(key)}:</strong> ${formatAgentValue(val)}</div>`
                    )
                    .join('')}
            </div>
        `;
    }

    return `<pre>${escapeHtml(String(value))}</pre>`;
}

function formatMedicalText(text) {
    return escapeHtml(text)
        .replace(/\\\*\\\*([\s\S]*?)\\\*\\\*/g, '<strong>$1</strong>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(
            /(^|\n)(\s*)(Risk Level|Risk Score|Possible Cases\/Causes|Possible Cases|Possible Causes|Reason|Next Step|Note|Symptoms|Severity|Duration|Body Location|Confidence|Recommendation|Warning Signs):/g,
            '$1$2<strong>$3:</strong>'
        );
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function applyPrompt(promptText) {
    const input = document.getElementById('symptomInput');
    if (input) input.value = promptText;
    resetClarificationState();
    setResult('<p>Submit symptoms to see your latest analysis.</p>');
}

function setAnalyzeButtonText(text) {
    const analyzeButton = document.getElementById('analyzeButton');
    if (analyzeButton) analyzeButton.innerText = text;
}

function resetClarificationState() {
    clarificationState = {
        stage: 'initial',
        symptoms: '',
        questions: []
    };
    setAnalyzeButtonText('Analyze');
}

function initHealthPage() {
    const analyzeButton = document.getElementById('analyzeButton');
    const voiceButton = document.getElementById('voiceButton');
    const symptomInput = document.getElementById('symptomInput');
    const promptButtons = document.querySelectorAll('.prompt-chip');

    analyzeButton?.addEventListener('click', submitSymptoms);
    voiceButton?.addEventListener('click', startVoiceInput);
    symptomInput?.addEventListener('input', () => {
        if (
            clarificationState.stage === 'clarifying' &&
            symptomInput.value.trim() !== clarificationState.symptoms
        ) {
            resetClarificationState();
            setResult('<p>Symptoms changed. Click Analyze to get fresh clarification questions.</p>');
        }
    });
    promptButtons.forEach((button) => {
        button.addEventListener('click', () => applyPrompt(button.dataset.prompt));
    });
}

document.addEventListener('DOMContentLoaded', () => {
    if (typeof ensureLoggedInRedirect === 'function') {
        ensureLoggedInRedirect();
    }
    initHealthPage();
});

window.resetHealthClarification = resetClarificationState;

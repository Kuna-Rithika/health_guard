const btn = document.getElementById("themeToggle");

if (btn) {
    btn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            btn.innerHTML = "Light Mode";
        } else {
            btn.innerHTML = "Dark Mode";
        }
    });
}

const API_URL = "http://127.0.0.1:8000";

function toTitleCase(value) {
    return value
        .split(/\s+/)
        .filter(Boolean)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

function cleanCaseName(value) {
    return value
        .replace(/^[\s\-*\d.)]+/, '')
        .replace(/\([^)]*\)/g, '')
        .replace(/^(possible\s+)?(?:case|cause|condition)\s*[:\-]\s*/i, '')
        .replace(/[:.]+$/g, '')
        .trim();
}

function extractPossibleCases(summary) {
    if (!summary) return [];

    const text = String(summary);
    const sectionMatch = text.match(
        /Possible\s+(?:Cases\/Causes|Cases|Causes)\s*:?\s*([\s\S]*?)(?=\n\s*(?:Reason|Next Step|Note|Risk Level|Risk Score)\b|$)/i
    );

    const sectionText = sectionMatch ? sectionMatch[1] : '';
    if (!sectionText.trim()) return [];

    return sectionText
        .split(/\n|,|;|\bor\b/gi)
        .map(cleanCaseName)
        .filter(item => item.length >= 3 && !/^\d+$/.test(item))
        .map(toTitleCase);
}

const symptomStopWords = new Set([
    'and', 'with', 'have', 'has', 'feel', 'feels', 'feeling', 'pain', 'very',
    'mild', 'severe', 'the', 'that', 'this', 'from', 'while', 'walking', 'my',
    'i', 'am', 'are', 'is', 'a', 'an', 'of', 'to', 'in', 'on', 'for'
]);

function extractSymptomTerms(symptoms) {
    if (!symptoms) return [];

    return String(symptoms)
        .toLowerCase()
        .replace(/[^a-z0-9\s,;/-]/g, ' ')
        .split(/,|;|\/|\band\b|\bwith\b|\n/gi)
        .map(item => item.trim())
        .filter(Boolean)
        .flatMap(item => item.split(/\s+/).length > 4 ? item.split(/\s+/) : [item])
        .map(item => item.replace(/^(i|am|have|has|feel|feeling|my)\s+/i, '').trim())
        .filter(item => item.length >= 3)
        .filter(item => !symptomStopWords.has(item))
        .map(toTitleCase);
}

async function loadDashboard() {
    const userId = localStorage.getItem("user_id");
    const userName = localStorage.getItem("user_name") || "User";

    const welcomeEl = document.getElementById("welcomeMessage");
    if (welcomeEl) welcomeEl.innerText = `Welcome back, ${userName}`;

    if (!userId) return;

    try {
        const userResponse = await fetch(`${API_URL}/users/${userId}`);
        const user = await userResponse.json();

        const riskEl = document.getElementById("riskValue");
        if (riskEl) riskEl.innerText = user.risk || "UNKNOWN";

        const historyResponse = await fetch(`${API_URL}/history/${userId}`);
        const history = await historyResponse.json();

        const reportsEl = document.getElementById("reportsCount");
        if (reportsEl) reportsEl.innerText = history.length;

        const scoreEl = document.getElementById("healthScore");
        if (scoreEl) scoreEl.innerText = history.length > 0 ? Math.max(50, 100 - history.length * 2) : "--";

        const reportsGenEl = document.getElementById('reportsGenerated');
        if (reportsGenEl) reportsGenEl.innerText = history.length;

        const latestSymptomEl = document.getElementById('latestSymptom');
        if (latestSymptomEl) latestSymptomEl.innerText = history[0]?.symptoms || '--';

        const labels = history.map(h => h.date);
        const riskScores = history.map(h => h.risk_score || 0);

        const freq = {};
        history.forEach(h => {
            const symptomTerms = extractSymptomTerms(h.symptoms);
            const items = symptomTerms.length ? symptomTerms : extractPossibleCases(h.summary);

            items.forEach(item => {
                freq[item] = (freq[item] || 0) + 1;
            });
        });

        const caseEntries = Object.entries(freq)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);
        const caseLabels = caseEntries.map(([name]) => name);
        const caseCounts = caseEntries.map(([, count]) => count);

        if (window.Chart) {
            const rctx = document.getElementById('riskChart')?.getContext('2d');
            if (rctx) {
                new Chart(rctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Risk Score',
                            data: riskScores,
                            borderColor: 'rgba(255,99,132,1)',
                            backgroundColor: 'rgba(255,99,132,0.2)'
                        }]
                    }
                });
            }

            const sctx = document.getElementById('symptomChart')?.getContext('2d');
            if (sctx) {
                new Chart(sctx, {
                    type: 'bar',
                    data: {
                        labels: caseLabels,
                        datasets: [{
                            label: 'Symptom Frequency',
                            data: caseCounts,
                            backgroundColor: 'rgba(54,162,235,0.6)'
                        }]
                    }
                });
            }
        }
    } catch (err) {
        console.error("Failed to load dashboard data", err);
    }
}

loadDashboard();

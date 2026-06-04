const API_URL = "http://127.0.0.1:8000";

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerText = value;
}

function setFormattedText(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = formatMedicalText(value);
}

function formatMedicalText(text) {
    return escapeHtml(text || 'No condition history')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(
            /(^|\n)(Risk Level|Risk Score|Possible Cases\/Causes|Possible Cases|Possible Causes|Reason|Next Step|Note):/g,
            '$1<strong>$2:</strong>'
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

async function loadProfile() {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users/${userId}`);
        if (!response.ok) {
            throw new Error('Failed to load profile');
        }

        const user = await response.json();

        setText('userName', user.name || 'Unknown');
        setText('userAge', user.age !== null && user.age !== undefined ? user.age : '--');
        setText('riskLevel', user.risk || 'Unknown');
        setText('userId', user.id || '--');
        setText('userEmail', user.email || '--');
        setFormattedText('condition', user.condition || 'No condition history');

        const healthScore = document.getElementById('healthScore');
        if (healthScore) {
            if (user.risk_score !== null && user.risk_score !== undefined) {
                const score = Math.max(0, Math.min(100, 100 - Number(user.risk_score)));
                healthScore.innerText = score;
            } else {
                healthScore.innerText = '--';
            }
        }

        // Load health patterns from history
        await loadHealthPatterns(userId);

        setText('profileStatus', 'Profile loaded');
    } catch (error) {
        setText('profileStatus', 'Unable to load profile');
        setText('userName', 'Guest');
    }
}

async function loadHealthPatterns(userId) {
    try {
        const response = await fetch(`${API_URL}/history/${userId}`);
        if (!response.ok) return;

        const history = await response.json();
        if (!history || history.length === 0) {
            document.getElementById('commonSymptoms').innerText = 'No symptom data available';
            document.getElementById('healthTrend').innerText = 'No trend data available';
            return;
        }

        // Extract common symptoms
        const symptomMap = {};
        history.forEach(h => {
            if (h.symptoms) {
                h.symptoms.split(',').forEach(sym => {
                    const s = sym.trim().toLowerCase();
                    symptomMap[s] = (symptomMap[s] || 0) + 1;
                });
            }
        });

        const topSymptoms = Object.entries(symptomMap)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 4)
            .map(([sym, count]) => `${sym} (${count} times)`)
            .join(', ');

        setText('commonSymptoms', topSymptoms || 'No patterns identified');

        // Health trend
        const riskScores = history.map(h => Number(h.risk_score || 0)).filter(s => s);
        let trendText = 'Stable';
        if (riskScores.length >= 2) {
            const recent = riskScores.slice(0, 3);
            const avg = recent.reduce((a, b) => a + b, 0) / recent.length;
            if (avg > 50) trendText = 'High risk pattern detected';
            else if (avg > 30) trendText = 'Moderate symptoms recurring';
            else trendText = 'Improving health status';
        }
        setText('healthTrend', trendText);

        // Possible causes and recommendations based on common symptoms
        const causes = generateHealthInsights(topSymptoms);
        document.getElementById('possibleCauses').innerHTML = causes.causes;
        document.getElementById('recommendations').innerHTML = causes.recommendations;
    } catch (error) {
        console.error('Error loading health patterns:', error);
    }
}

function generateHealthInsights(symptoms) {
    const symptomsLower = symptoms.toLowerCase();
    
    let causes = 'Analyzing patterns...';
    let recommendations = 'Consult with healthcare provider for personalized advice';

    if (symptomsLower.includes('headache')) {
        causes = 'Possible causes: Stress, dehydration, tension, or migraines';
        recommendations = '• Increase water intake<br>• Practice stress management<br>• Maintain regular sleep schedule';
    } else if (symptomsLower.includes('fatigue')) {
        causes = 'Possible causes: Sleep deprivation, anemia, or thyroid issues';
        recommendations = '• Ensure 7-9 hours sleep<br>• Balanced diet with iron-rich foods<br>• Regular light exercise';
    } else if (symptomsLower.includes('fever')) {
        causes = 'Possible causes: Viral infection, bacterial infection, or inflammation';
        recommendations = '• Stay hydrated<br>• Rest and monitor temperature<br>• Seek medical care if persistent';
    } else if (symptomsLower.includes('cough')) {
        causes = 'Possible causes: Respiratory infection, allergies, or irritation';
        recommendations = '• Stay hydrated<br>• Use honey or throat lozenges<br>• Avoid irritants and smoke';
    } else if (symptomsLower.includes('pain')) {
        causes = 'Possible causes: Muscle strain, inflammation, or injury';
        recommendations = '• Apply ice or heat therapy<br>• Gentle stretching exercises<br>• Anti-inflammatory diet';
    } else if (symptomsLower.includes('nausea')) {
        causes = 'Possible causes: Digestive issues, food sensitivity, or motion sickness';
        recommendations = '• Eat light, bland foods<br>• Ginger or peppermint tea<br>• Avoid heavy meals';
    } else {
        causes = 'Based on your symptom patterns, conditions may vary. Professional consultation recommended.';
        recommendations = '• Monitor symptoms regularly<br>• Keep health records<br>• Schedule regular checkups';
    }

    return { causes, recommendations };
}

document.addEventListener('DOMContentLoaded', () => {
    if (typeof ensureLoggedInRedirect === 'function') {
        ensureLoggedInRedirect();
    }
    loadProfile();
});

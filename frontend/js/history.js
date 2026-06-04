const API_URL = "https://health-guard-caq0.onrender.com";

function getRiskClass(level) {
    if (!level) return 'medium';
    const risk = level.toLowerCase();
    if (risk.includes('critical')) return 'critical';
    if (risk.includes('high')) return 'high';
    if (risk.includes('low')) return 'low';
    return 'medium';
}

function renderHistoryItem(item) {
    const riskClass = getRiskClass(item.risk_level);
    return `
        <div class="history-card">
            <div class="date">${item.date || 'Unknown date'}</div>
            <div class="symptom">${item.symptoms || 'No symptoms recorded'}</div>
            <span class="risk ${riskClass}">${item.risk_level || 'Unknown'}</span>
        </div>
    `;
}

async function loadHistory() {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/history/${userId}`);
        if (!response.ok) throw new Error('Unable to load history');

        const data = await response.json();
        const timeline = document.getElementById('timeline');
        const totalRecords = document.getElementById('totalRecords');
        const riskLevel = document.getElementById('riskLevel');
        const historyHealthScore = document.getElementById('historyHealthScore');
        const historyStatus = document.getElementById('historyStatus');

        totalRecords.innerText = data.length;
        timeline.innerHTML = data.length ? data.map(renderHistoryItem).join('') : '<div class="empty-state">No history records found.</div>';

        if (data.length > 0) {
            const latest = data[0];
            riskLevel.innerText = latest.risk_level || '--';
            historyHealthScore.innerText = latest.risk_score || '--';
            historyStatus.innerText = 'History updated';
        } else {
            riskLevel.innerText = '--';
            historyHealthScore.innerText = '--';
            historyStatus.innerText = 'No history records yet';
        }
    } catch (error) {
        document.getElementById('historyStatus').innerText = 'Unable to load history';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (typeof ensureLoggedInRedirect === 'function') {
        ensureLoggedInRedirect();
    }
    loadHistory();
});

function logout() {
    const confirmed = window.confirm('Are you sure you want to log out?');
    if (!confirmed) return;
    localStorage.clear();
    window.location.href = 'login.html';
}

function ensureLoggedInRedirect() {
    const userId = localStorage.getItem('user_id');
    if (!userId) window.location.href = 'login.html';
}

// Exporting to global scope is intentional for simple pages
window.logout = logout;
window.ensureLoggedInRedirect = ensureLoggedInRedirect;

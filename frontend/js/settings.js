const API_URL = "http://127.0.0.1:8000";

function updateTheme(mode) {
    if (mode === 'dark') {
        document.body.classList.add('dark-theme');
        localStorage.setItem('theme_mode', 'dark');
    } else {
        document.body.classList.remove('dark-theme');
        localStorage.setItem('theme_mode', 'light');
    }
}

function setButtonState(buttonId, enabled, labelOn, labelOff) {
    const button = document.getElementById(buttonId);
    if (!button) return;
    button.innerText = enabled ? labelOn : labelOff;
}

function loadSettings() {
    const userId = localStorage.getItem('user_id');
    const settingsUser = document.getElementById('settingsUser');
    const settingsName = document.getElementById('settingsName');
    const settingsEmail = document.getElementById('settingsEmail');

    if (!userId) {
        if (settingsUser) settingsUser.innerText = 'Guest';
        return;
    }

    fetch(`${API_URL}/users/${userId}`)
        .then(r => r.json())
        .then(user => {
            if (settingsUser) settingsUser.innerText = `Signed in as ${user.name} (${user.email})`;
            if (settingsName) settingsName.innerText = user.name;
            if (settingsEmail) settingsEmail.innerText = user.email;
        })
        .catch(() => {
            if (settingsUser) settingsUser.innerText = 'Unable to load user';
        });
}

function initializeSettings() {
    const themeButton = document.getElementById('themeToggle');
    const notificationsButton = document.getElementById('notificationsToggle');
    const locationButton = document.getElementById('locationToggle');
    const pinButton = document.getElementById('pinToggle');
    const fingerprintButton = document.getElementById('fingerprintToggle');
    const sleepButton = document.getElementById('sleepToggle');
    const fitnessButton = document.getElementById('fitnessToggle');
    const brightnessSlider = document.getElementById('brightnessRange');
    const brightnessValue = document.getElementById('brightnessValue');
    const stepGoalInput = document.getElementById('stepGoal');
    const feedbackButton = document.getElementById('submitFeedback');

    const savedTheme = localStorage.getItem('theme_mode') || 'light';
    updateTheme(savedTheme);
    if (themeButton) {
        themeButton.innerText = savedTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
        themeButton.addEventListener('click', () => {
            const nextTheme = savedTheme === 'dark' ? 'light' : 'dark';
            updateTheme(nextTheme);
            themeButton.innerText = nextTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
        });
    }

    const savedNotifications = localStorage.getItem('notifications_enabled') !== 'false';
    setButtonState('notificationsToggle', savedNotifications, 'Notifications ON', 'Notifications OFF');
    notificationsButton?.addEventListener('click', () => {
        const current = localStorage.getItem('notifications_enabled') !== 'false';
        const next = !current;
        localStorage.setItem('notifications_enabled', next);
        setButtonState('notificationsToggle', next, 'Notifications ON', 'Notifications OFF');
    });

    const savedLocation = localStorage.getItem('location_enabled') !== 'false';
    setButtonState('locationToggle', savedLocation, 'Location ON', 'Location OFF');
    locationButton?.addEventListener('click', () => {
        const current = localStorage.getItem('location_enabled') !== 'false';
        const next = !current;
        localStorage.setItem('location_enabled', next);
        setButtonState('locationToggle', next, 'Location ON', 'Location OFF');
    });

    const savedPin = localStorage.getItem('pin_lock_enabled') === 'true';
    setButtonState('pinToggle', savedPin, 'PIN ON', 'PIN OFF');
    pinButton?.addEventListener('click', () => {
        const next = localStorage.getItem('pin_lock_enabled') !== 'true';
        localStorage.setItem('pin_lock_enabled', next);
        setButtonState('pinToggle', next, 'PIN ON', 'PIN OFF');
    });

    const savedFingerprint = localStorage.getItem('fingerprint_enabled') === 'true';
    setButtonState('fingerprintToggle', savedFingerprint, 'Fingerprint ON', 'Fingerprint OFF');
    fingerprintButton?.addEventListener('click', () => {
        const next = localStorage.getItem('fingerprint_enabled') !== 'true';
        localStorage.setItem('fingerprint_enabled', next);
        setButtonState('fingerprintToggle', next, 'Fingerprint ON', 'Fingerprint OFF');
    });

    const savedSleep = localStorage.getItem('sleep_reminders_enabled') !== 'false';
    setButtonState('sleepToggle', savedSleep, 'Sleep ON', 'Sleep OFF');
    sleepButton?.addEventListener('click', () => {
        const current = localStorage.getItem('sleep_reminders_enabled') !== 'false';
        const next = !current;
        localStorage.setItem('sleep_reminders_enabled', next);
        setButtonState('sleepToggle', next, 'Sleep ON', 'Sleep OFF');
    });

    const savedFitness = localStorage.getItem('fitness_reminders_enabled') !== 'false';
    setButtonState('fitnessToggle', savedFitness, 'Fitness ON', 'Fitness OFF');
    fitnessButton?.addEventListener('click', () => {
        const current = localStorage.getItem('fitness_reminders_enabled') !== 'false';
        const next = !current;
        localStorage.setItem('fitness_reminders_enabled', next);
        setButtonState('fitnessToggle', next, 'Fitness ON', 'Fitness OFF');
    });

    const savedBrightness = Number(localStorage.getItem('brightness_level') || 80);
    if (brightnessSlider) {
        brightnessSlider.value = savedBrightness;
        brightnessValue.innerText = `${savedBrightness}%`;
        brightnessSlider.addEventListener('input', () => {
            const value = Number(brightnessSlider.value);
            brightnessValue.innerText = `${value}%`;
            localStorage.setItem('brightness_level', value);
        });
    }

    const savedStepGoal = Number(localStorage.getItem('step_goal') || 8000);
    if (stepGoalInput) {
        stepGoalInput.value = savedStepGoal;
        stepGoalInput.addEventListener('change', () => {
            const value = Number(stepGoalInput.value) || 0;
            localStorage.setItem('step_goal', value);
            stepGoalInput.value = value;
        });
    }

    feedbackButton?.addEventListener('click', () => {
        const feedbackInput = document.getElementById('feedbackInput');
        const feedbackMessage = document.getElementById('feedbackMessage');
        if (!feedbackInput || !feedbackMessage) return;

        const text = feedbackInput.value.trim();
        if (!text) {
            feedbackMessage.innerText = 'Please enter feedback before sending.';
            return;
        }

        feedbackMessage.innerText = 'Thanks for your feedback!';
        feedbackInput.value = '';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    initializeSettings();
});

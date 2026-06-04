const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

let recognition = null;
if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
        const statusEl = document.getElementById('healthStatus');
        if (statusEl) statusEl.innerText = 'Listening... Speak now.';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("symptomInput");
        if (input) input.value = transcript;
        if (typeof window.resetHealthClarification === 'function') {
            window.resetHealthClarification();
        }
        const statusEl = document.getElementById('healthStatus');
        if (statusEl) statusEl.innerText = 'Voice input captured. Press Analyze when ready.';
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        alert('Voice recognition error: ' + event.error);
        const statusEl = document.getElementById('healthStatus');
        if (statusEl) statusEl.innerText = 'Voice recognition error. Please try again.';
    };

    recognition.onend = () => {
        const statusEl = document.getElementById('healthStatus');
        if (statusEl && statusEl.innerText.includes('Listening')) {
            statusEl.innerText = 'Voice input ended. Review your symptoms and click Analyze.';
        }
    };
}

function startVoiceInput() {
    if (!recognition) {
        alert('Voice input is not supported in this browser.');
        return;
    }

    try {
        recognition.start();
    } catch (error) {
        console.error('Speech recognition error:', error);
        alert('Unable to start voice recognition. Please try again.');
    }
}

window.startVoiceInput = startVoiceInput;

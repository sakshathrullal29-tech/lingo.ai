const API_URL = "https://YOUR-RENDER-URL.onrender.com";

const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");

const sourceLanguage = document.getElementById("sourceLanguage");
const targetLanguage = document.getElementById("targetLanguage");

const translateBtn = document.getElementById("translateBtn");
const swapBtn = document.getElementById("swapBtn");
const micBtn = document.getElementById("micBtn");
const copyBtn = document.getElementById("copyBtn");

const charCount = document.getElementById("charCount");
const statusMessage = document.getElementById("statusMessage");


inputText.addEventListener("input", () => {
    charCount.textContent = `${inputText.value.length} characters`;
});


swapBtn.addEventListener("click", () => {
    const oldSource = sourceLanguage.value;
    sourceLanguage.value = targetLanguage.value;
    targetLanguage.value = oldSource;

    const oldText = inputText.value;
    inputText.value = outputText.textContent === "Your translation will appear here..."
        ? ""
        : outputText.textContent;

    outputText.textContent = oldText || "Your translation will appear here...";

    charCount.textContent = `${inputText.value.length} characters`;
});


translateBtn.addEventListener("click", async () => {

    const text = inputText.value.trim();

    if (!text) {
        statusMessage.textContent = "Please enter something to translate.";
        return;
    }

    if (sourceLanguage.value === targetLanguage.value) {
        outputText.textContent = text;
        statusMessage.textContent = "Source and target languages are the same.";
        return;
    }

    translateBtn.disabled = true;
    translateBtn.querySelector("span").textContent = "Translating...";
    statusMessage.textContent = "Aloy Vaani is translating...";

    try {

        const response = await fetch(`${API_URL}/translate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                source_language: sourceLanguage.value,
                target_language: targetLanguage.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Translation failed");
        }

        outputText.textContent = data.translation;

        statusMessage.textContent = "Translation complete ✨";

    } catch (error) {

        console.error(error);

        outputText.textContent = "Unable to translate right now.";
        statusMessage.textContent =
            "Backend is unavailable. Please try again later.";

    } finally {

        translateBtn.disabled = false;
        translateBtn.querySelector("span").textContent = "Translate";
    }
});


copyBtn.addEventListener("click", async () => {

    const text = outputText.textContent;

    if (
        !text ||
        text === "Your translation will appear here..."
    ) {
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        statusMessage.textContent = "Translation copied! 📋";
    } catch {
        statusMessage.textContent = "Couldn't copy the translation.";
    }
});


let recognition = null;

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        micBtn.textContent = "🔴";
        statusMessage.textContent = "Listening...";
    };

    recognition.onresult = (event) => {

        const transcript =
            event.results[0][0].transcript;

        inputText.value = transcript;

        charCount.textContent =
            `${inputText.value.length} characters`;

        statusMessage.textContent =
            "Voice captured 🎙️";
    };

    recognition.onerror = () => {
        statusMessage.textContent =
            "Microphone couldn't be accessed.";
    };

    recognition.onend = () => {
        micBtn.textContent = "🎙️";
    };

} else {

    micBtn.disabled = true;
    micBtn.title = "Speech recognition is not supported in this browser.";
}


micBtn.addEventListener("click", () => {

    if (!recognition) {
        statusMessage.textContent =
            "Voice recognition is not supported here.";
        return;
    }

    recognition.start();
});
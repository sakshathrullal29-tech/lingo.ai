from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)


# Simple lightweight translation dictionary.
# This keeps the Render server extremely small and memory-friendly.

TRANSLATIONS = {
    ("en", "hi"): {
        "hello": "नमस्ते",
        "hello world": "नमस्ते दुनिया",
        "good morning": "सुप्रभात",
        "good night": "शुभ रात्रि",
        "thank you": "धन्यवाद",
        "how are you": "आप कैसे हैं?",
        "what is your name": "आपका नाम क्या है?",
        "i am fine": "मैं ठीक हूँ",
        "welcome": "स्वागत है",
        "yes": "हाँ",
        "no": "नहीं"
    },

    ("en", "kn"): {
        "hello": "ನಮಸ್ಕಾರ",
        "hello world": "ನಮಸ್ಕಾರ ಜಗತ್ತು",
        "good morning": "ಶುಭೋದಯ",
        "good night": "ಶುಭ ರಾತ್ರಿ",
        "thank you": "ಧನ್ಯವಾದಗಳು",
        "how are you": "ನೀವು ಹೇಗಿದ್ದೀರಿ?",
        "what is your name": "ನಿಮ್ಮ ಹೆಸರೇನು?",
        "i am fine": "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ",
        "welcome": "ಸ್ವಾಗತ",
        "yes": "ಹೌದು",
        "no": "ಇಲ್ಲ"
    },

    ("hi", "en"): {
        "नमस्ते": "hello",
        "नमस्ते दुनिया": "hello world",
        "सुप्रभात": "good morning",
        "शुभ रात्रि": "good night",
        "धन्यवाद": "thank you",
        "हाँ": "yes",
        "नहीं": "no"
    },

    ("kn", "en"): {
        "ನಮಸ್ಕಾರ": "hello",
        "ನಮಸ್ಕಾರ ಜಗತ್ತು": "hello world",
        "ಶುಭೋದಯ": "good morning",
        "ಶುಭ ರಾತ್ರಿ": "good night",
        "ಧನ್ಯವಾದಗಳು": "thank you",
        "ಹೌದು": "yes",
        "ಇಲ್ಲ": "no"
    }
}


@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json(silent=True) or {}

    text = str(data.get("text", "")).strip()
    source = data.get("source_language", "en")
    target = data.get("target_language", "hi")

    if not text:
        return jsonify({
            "error": "Please enter text."
        }), 400

    if source == target:
        return jsonify({
            "translation": text
        })

    key = (source, target)
    dictionary = TRANSLATIONS.get(key, {})

    result = dictionary.get(
        text.lower(),
        "Translation for this sentence is not available yet."
    )

    return jsonify({
        "translation": result
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Aloy Vaani"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)


LANGUAGE_CODES = {
    "en": "en",
    "hi": "hi",
    "kn": "kn"
}


@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Aloy Vaani"
    })


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

    if source not in LANGUAGE_CODES or target not in LANGUAGE_CODES:
        return jsonify({
            "error": "Unsupported language."
        }), 400

    try:
        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "sl": LANGUAGE_CODES[source],
            "tl": LANGUAGE_CODES[target],
            "dt": "t",
            "q": text
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()

        translated_parts = []

        for item in result[0]:
            if item and item[0]:
                translated_parts.append(item[0])

        translation = "".join(translated_parts)

        if not translation:
            return jsonify({
                "error": "Translation returned empty."
            }), 500

        return jsonify({
            "translation": translation
        })

    except requests.RequestException as error:

        print("Translation request failed:", error)

        return jsonify({
            "error": "Translation service is temporarily unavailable."
        }), 503

    except Exception as error:

        print("Unexpected translation error:", error)

        return jsonify({
            "error": "Translation failed."
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
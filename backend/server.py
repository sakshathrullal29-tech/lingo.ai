```text
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

app = Flask(__name__)
CORS(app)

MODEL_NAME = "facebook/nllb-200-distilled-600M"

print("Loading Lingo AI multilingual translator...")
print("English <-> Hindi <-> Kannada")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Multilingual translator loaded!")

LANGUAGES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "kn": "kan_Knda"
}


@app.route("/")
def home():
    return jsonify({
        "message": "Lingo AI backend is running!",
        "languages": [
            "English",
            "Hindi",
            "Kannada"
        ]
    })


@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    text = data.get("text", "").strip()
    source = data.get("source_language", "en")
    target = data.get("target_language", "hi")

    if not text:
        return jsonify({
            "error": "No text received"
        }), 400

    if source not in LANGUAGES:
        return jsonify({
            "error": "Unsupported source language"
        }), 400

    if target not in LANGUAGES:
        return jsonify({
            "error": "Unsupported target language"
        }), 400

    if source == target:
        return jsonify({
            "text": text,
            "translation": text,
            "source_language": source,
            "target_language": target
        })

    source_code = LANGUAGES[source]
    target_code = LANGUAGES[target]

    tokenizer.src_lang = source_code

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():

        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_code),
            max_length=256
        )

    translation = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]

    return jsonify({
        "text": text,
        "translation": translation,
        "source_language": source,
        "target_language": target
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
```

# Version: v4.3 | Date: 06/27/2025 | Updated for 3-voice environment setup on Render

import os
import requests
from flask import Flask, render_template, request, send_file, jsonify
from dotenv import load_dotenv
from io import BytesIO

app = Flask(__name__)
load_dotenv()

# Load API key and voice IDs from environment
api_key = os.getenv("ELEVENLABS_API_KEY")
voice_ids = {
    "Bernard": os.getenv("VOICE_ID_BERNARD"),
    "Snowflake": os.getenv("VOICE_ID_SNOWFLAKE"),
    "Pepper": os.getenv("VOICE_ID_PEPPER")
}

@app.route("/")
def index():
    return render_template("index.html", voices=list(voice_ids.keys()))

@app.route("/api/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    voice = data.get("voice", "")

    if not text or not voice or voice not in voice_ids:
        return jsonify({"error": "Missing or invalid input"}), 400

    voice_id = voice_ids[voice]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("Error from ElevenLabs:", response.text)
        return jsonify({"error": "Something went wrong!"}), 500

    return send_file(BytesIO(response.content), mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)

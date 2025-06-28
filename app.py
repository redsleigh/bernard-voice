# Version: v5.0 | Date: 06/28/2025 | Voice selector and ElevenLabs integration

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Voice IDs from environment variables
VOICE_IDS = {
    "Bernard": os.getenv("BERNARD_VOICE_ID"),
    "Snowflake": os.getenv("SNOWFLAKE_VOICE_ID"),
    "Pepper": os.getenv("PEPPER_VOICE_ID"),
}

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route("/api/speak", methods=["POST"])
def speak():
    data = request.json
    voice_name = data.get("voice")
    text = data.get("message", "")

    if not voice_name or not text:
        return jsonify({"error": "Voice and message required"}), 400

    voice_id = VOICE_IDS.get(voice_name)
    if not voice_id:
        return jsonify({"error": "Invalid voice selection"}), 400

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        output_path = "static/output.mp3"
        with open(output_path, "wb") as f:
            f.write(response.content)
        return send_file(output_path, mimetype="audio/mpeg")
    else:
        print("Error:", response.text)
        return jsonify({"error": "Failed to generate audio"}), 500

if __name__ == "__main__":
    app.run(debug=True)

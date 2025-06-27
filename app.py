# Version: v4.2.3 | Date: 06/27/2025 | Voice selector integrated
from flask import Flask, request, send_file, render_template
from io import BytesIO
import os
import requests

app = Flask(__name__)

# Set your ElevenLabs API key here
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_MAP = {
    "bernard": "voice_id_1",   # Replace with real IDs
    "twinkle": "voice_id_2",
    "jingles": "voice_id_3"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("text", "")
    voice_key = data.get("voice", "bernard")
    voice_id = VOICE_MAP.get(voice_key, VOICE_MAP["bernard"])

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return f"Error: {response.text}", 500

    audio_data = BytesIO(response.content)
    return send_file(audio_data, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)

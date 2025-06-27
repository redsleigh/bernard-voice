# Version: v4.2.4 | Date: 06/27/2025 | Background set to festive-bg-v2.png from static/
from flask import Flask, request, send_file, render_template
from io import BytesIO
import os
import requests

app = Flask(__name__, static_folder='static')

# ElevenLabs API Key (set in your Render environment variables)
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Voice IDs from ElevenLabs
VOICE_MAP = {
    "bernard": "VCgLBmBjldJmfphyB8sZ",
    "snowflake": "uHiItyLY8A5jJv9AKoH9",
    "pepper": "W4crgEyhEtLRIj1Y3LnP"
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
    return synthesize_speech(text, voice_id)

def synthesize_speech(text, voice_id):
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

    return send_file(BytesIO(response.content), mimetype="audio/mpeg")

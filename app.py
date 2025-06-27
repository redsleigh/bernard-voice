from flask import Flask, render_template, request, send_file, jsonify
import requests
import os
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Load environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE_ID = os.getenv("VOICE_ID")

# Voice map for UI selection
VOICE_MAP = {
    "Bernard": DEFAULT_VOICE_ID,
    "Snowflake": "uHiItyLY8A5jJv9AKoH9",
    "Pepper": "W4crgEyhEtLRIj1Y3LnP"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    message = data.get("message", "")
    voice = data.get("voice", "Bernard")
    voice_id = VOICE_MAP.get(voice, DEFAULT_VOICE_ID)

    if not ELEVENLABS_API_KEY or not voice_id:
        return jsonify({"error": "Missing API key or voice ID"}), 500

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"

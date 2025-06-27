import os
import requests
from flask import Flask, request, render_template, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_IDS = {
    "Bernard (Default)": "VCgLBmBjldJmfphyB8sZ",
    "Snowflake": "uHiItyLY8A5jJv9AKoH9",
    "Pepper": "W4crgEyhEtLRIj1Y3LnP"
}

@app.route("/")
def index():
    return render_template("index.html", voices=list(VOICE_IDS.keys()))

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    voice_name = request.form.get("voice")
    voice_id = VOICE_IDS.get(voice_name)

    if not text or not voice_id:
        return "Invalid input", 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    json_data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        with open("static/bernard_output.mp3", "wb") as f:
            f.write(response.content)
        return "/static/bernard_output.mp3"
    else:
        return f"Error: {response.status_code} - {response.text}", 500

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)

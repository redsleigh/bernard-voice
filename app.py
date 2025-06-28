import os
from flask import Flask, request, send_file, render_template_string
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_IDS = {
    "Bernard": os.getenv("VOICE_ID_BERNARD"),
    "Snowflake": os.getenv("VOICE_ID_SNOWFLAKE"),
    "Pepper": os.getenv("VOICE_ID_PEPPER"),
}

@app.route("/")
def index():
    with open("templates/index.html") as f:
        return render_template_string(f.read())

@app.route("/api/speak", methods=["POST"])
def speak():
    data = request.get_json()
    message = data.get("message", "")
    voice_name = data.get("voice", "Bernard")
    voice_id = VOICE_IDS.get(voice_name)

    if not API_KEY or not voice_id or not message:
        return "Missing data", 400

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": message,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
        )

        if response.status_code != 200:
            return "Voice API error", 500

        audio_data = BytesIO(response.content)
        return send_file(audio_data, mimetype="audio/mpeg")

    except Exception as e:
        print("ERROR:", e)
        return "Server error", 500

if __name__ == "__main__":
    app.run(debug=True)

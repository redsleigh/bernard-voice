from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Replace with your actual ElevenLabs API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Optional: map voices to IDs if you have custom voices
VOICE_ID_MAP = {
    "Bernard": "EXAVITQu4vr4xnSDxMaL"  # Replace with your actual Bernard voice ID
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/speak", methods=["POST"])
def speak():
    data = request.json
    voice = data.get("voice", "Bernard")
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    voice_id = VOICE_ID_MAP.get(voice, VOICE_ID_MAP["Bernard"])

    # Send request to ElevenLabs API
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": message,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.75
                }
            }
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to get audio"}), 500

        # Save the mp3 file
        audio_path = "static/bernard_output.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)

        return jsonify({"audio_url": f"/{audio_path}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Load environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

@app.route("/api/speak", methods=["POST"])
def speak():
    data = request.get_json()
    message = data.get("message", "")
    voice = data.get("voice", VOICE_ID)

    if not message:
        return jsonify({"error": "Message is required"}), 400

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        output_path = "static/bernard_output.mp3"
        with open(output_path, "wb") as f:
            f.write(response.content)
        return jsonify({"audio_url": f"/{output_path}"})
    else:
        return jsonify({"error": "Failed to get audio", "details": response.text}), 500

@app.route("/")
def index():
    return "Bernard Voice Assistant API is running!"

if __name__ == "__main__":
    app.run(debug=True)

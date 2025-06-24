from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route("/generate", methods=["POST"])
def generate_voice():
    try:
        data = request.get_json()
        text = data.get("text", "")
        voice_id = data.get("voice_id", "")

        if not text or not voice_id:
            return jsonify({"error": "Missing text or voice_id"}), 400

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return jsonify({"error": "ElevenLabs API error"}), 500

        # Save audio to file
        with open("static/response.mp3", "wb") as f:
            f.write(response.content)

        return jsonify({"audio_url": "/static/response.mp3"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

# Version: v4.2.4 | Date: 06/27/2025 | Description: Fixed API key name to match Render environment variable; added voice selector functionality.

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

# ✅ Use correct environment variable name set in Render
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Default fallback voice
DEFAULT_VOICE_ID = "VCgLBmBjldJmfphyB8sZ"  # Bernard

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text", "")
    voice_id = data.get("voice_id", DEFAULT_VOICE_ID)

    if not text:
        return jsonify({"error": "No text provided."}), 400

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json=payload,
            headers=headers
        )
        if response.status_code == 200:
            return response.content, 200, {'Content-Type': 'audio/mpeg'}
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

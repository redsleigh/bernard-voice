from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]
    if not ELEVENLABS_API_KEY or not VOICE_ID:
        return jsonify({"error": "API key or Voice ID not configured"}), 500

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to generate audio"}), 500

        return response.content, 200, {"Content-Type": "audio/mpeg"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

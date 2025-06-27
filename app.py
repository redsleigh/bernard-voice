import os
import time
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Voice ID mapping (replace with your actual voice IDs)
voice_ids = {
    "Bernard": "YOUR_BERNARD_VOICE_ID",
    "Pepper": "YOUR_PEPPER_VOICE_ID",
    "Obie": "YOUR_OBIE_VOICE_ID"
}

@app.route('/')
def index():
    return render_template('index.html', voices=list(voice_ids.keys()))

@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        data = request.get_json()
        voice = data.get("voice")
        text = data.get("text")

        if not voice or not text:
            return jsonify({"error": "Missing voice or text"}), 400

        voice_id = voice_ids.get(voice)
        if not voice_id:
            return jsonify({"error": f"Voice '{voice}' not found"}), 404

        print(f"[INFO] Generating speech for voice '{voice}' with text: {text}")

        # Call ElevenLabs API
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": os.getenv("ELEVEN_API_KEY"),
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.8
                }
            }
        )

        if response.status_code != 200:
            print("[ERROR] ElevenLabs response:", response.text)
            return jsonify({"error": "TTS failed"}), 500

        # Save with timestamp to prevent caching
        timestamp = int(time.time())
        filename = f"bernard_output_{timestamp}.mp3"
        filepath = os.path.join("static", filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"[SUCCESS] Audio saved as {filename}")
        return jsonify({"audio_url": f"/static/{filename}"})

    except Exception as e:
        print("[EXCEPTION]", str(e))
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Root route to serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle message and return audio URL
@app.route('/generate', methods=['POST'])
def generate_audio():
    data = request.get_json()
    message = data.get('message')
    voice = data.get('voice', 'Bernard')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    voice_map = {
        "Bernard": os.getenv("BERNARD_VOICE_ID"),
        "Joey": os.getenv("JOEY_VOICE_ID")
    }

    voice_id = voice_map.get(voice)
    if not voice_id:
        return jsonify({'error': 'Invalid voice selection'}), 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
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

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open("static/bernard_output.mp3", "wb") as f:
            f.write(response.content)
        return jsonify({"audio_url": "/static/bernard_output.mp3"})
    else:
        return jsonify({'error': 'Failed to generate audio'}), 500

if __name__ == '__main__':
    app.run(debug=True)

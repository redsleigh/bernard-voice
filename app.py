from flask import Flask, request, send_file
import requests
import tempfile
import os

app = Flask(__name__)

# Your ElevenLabs API key
ELEVENLABS_API_KEY = "your_api_key_here"

# Voice ID mappings
VOICE_IDS = {
    "bernard": "VCgLBmBjldJmfphyB8sZ",
    "pepper": "W4crgEyhEtLRIj1Y3LnP",
    "snowflake": "uHiItyLY8A5jJv9AKoH9"
}

DEFAULT_VOICE_ID = VOICE_IDS["bernard"]

def get_voice_id_from_text(text):
    lowered = text.lower()
    if "pepper" in lowered:
        return VOICE_IDS["pepper"]
    elif "snowflake" in lowered:
        return VOICE_IDS["snowflake"]
    elif "bernard" in lowered:
        return VOICE_IDS["bernard"]
    return DEFAULT_VOICE_ID

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    if not data or "text" not in data:
        return {"error": "Missing 'text' in request"}, 400

    text = data["text"]
    voice_id = get_voice_id_from_text(text)

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.65,
            "similarity_boost": 0.75
        }
    }

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    response = requests.post(tts_url, headers=headers, json=payload, stream=True)

    if response.status_code != 200:
        return {"error": f"Text-to-speech failed: {response.text}"}, 500

    # Save the streamed audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        temp_file_path = f.name

    return send_file(temp_file_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)

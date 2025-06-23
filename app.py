import os
from flask import Flask, render_template, request, send_from_directory
import requests
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        user_text = request.form.get("user_input")
        if user_text:
            voice_id = os.environ.get("VOICE_ID")
            elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
            if not voice_id or not elevenlabs_api_key:
                return "Missing environment variables for voice or API key."

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": user_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                filename = f"{uuid.uuid4().hex}.mp3"
                filepath = os.path.join("static", filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                audio_file = filename
            else:
                return f"API request failed with status {response.status_code}: {response.text}"

    return render_template("index.html", audio_file=audio_file)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

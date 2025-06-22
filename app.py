from flask import Flask, render_template, request
import requests
import uuid
import os

app = Flask(__name__)
os.makedirs("static", exist_ok=True)

ELEVEN_LABS_API_KEY = "sk_00ef76630743f0baa0c95da661f8440389e8cbb237d72ff1"
VOICE_ID = "VGcLBmBJldJmfphy8BsZ"

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None

   if request.method == "POST":
    text = request.form["text"]
    output_path = f"static/bernard_{uuid.uuid4().hex[:8]}.mp3"
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.7
        }
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        audio_file = output_path
    else:
        print("❌ ElevenLabs API Error:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")


    return render_template("index.html", audio_file=audio_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

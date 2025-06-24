from flask import Flask, request, jsonify, render_template
import os
import openai
import requests

app = Flask(__name__)

# Set your OpenAI and ElevenLabs API keys here
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Voice IDs
VOICE_IDS = {
    "bernard": "VCgLBmBjldJmfphyB8sZ",
    "pepper": "W4crgEyhEtLRIj1Y3LnP",
    "snowflake": "uHiItyLY8A5jJv9AKoH9"
}

def identify_speaker(prompt):
    prompt_lower = prompt.lower()
    if "hey pepper" in prompt_lower:
        return "pepper"
    elif "hey snowflake" in prompt_lower:
        return "snowflake"
    else:
        return "bernard"

def generate_response(prompt, speaker):
    if speaker == "pepper":
        persona = "You are Pepper, a cheerful young female elf with a warm, friendly tone, a gentle North Pole accent, and a hint of holiday sparkle. You’re helpful, upbeat, and always excited to assist Santa."
    elif speaker == "snowflake":
        persona = "You are Snowflake, a high-energy child elf with a bright, playful voice, a touch of North Pole mischief, and endless excitement. You’re silly and fast-paced with lots of energy."
    else:
        persona = "You are Bernard, Santa's head elf. You’re kind, wise, and helpful. You always speak with warm North Pole charm and you help organize Santa’s operations."

    messages = [
        {"role": "system", "content": persona},
        {"role": "user", "content": prompt}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    return completion.choices[0].message['content']

def synthesize_voice(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        with open("static/response.mp3", "wb") as f:
            f.write(response.content)
        return True
    return False

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")

    speaker = identify_speaker(prompt)
    response = generate_response(prompt, speaker)
    voice_id = VOICE_IDS.get(speaker)

    success = synthesize_voice(response, voice_id)
    if not success:
        return jsonify({"error": "Voice synthesis failed"}), 500

    return jsonify({"response": response, "audio_url": "/static/response.mp3"})

# === Required for Render ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

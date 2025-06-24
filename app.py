from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Load your OpenAI API key from environment variable or set it directly
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace with your real key or use environment

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('message', '')

        if not prompt:
            return jsonify({'error': 'No message provided.'}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Bernard, Santa’s cheerful voice assistant elf."},
                {"role": "user", "content": prompt}
            ]
        )

        message = response['choices'][0]['message']['content']
        return jsonify({'response': message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Replace this with your actual OpenAI API key
openai.api_key = "your-openai-api-key"

@app.route('/')
def home():
    return "Vet AI Agent is running. Use /recommend or /chat."

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    symptoms = data.get('symptoms', '')

    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    prompt = f"""You are a veterinary expert. A farmer says their animal has the following symptoms or disease name: '{symptoms}'. 
Suggest an appropriate veterinary medicine available in Botswana. Answer in both English and Setswana."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({"recommendation": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

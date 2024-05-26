from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

conversation_context = []

def generate_response(prompt):
    global conversation_context
    conversation_context.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a polite and helpful customer service agent."}
        ] + conversation_context
    )
    reply = response.choices[0].message['content'].strip()
    conversation_context.append({"role": "assistant", "content": reply})
    return reply

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = generate_response(user_input)
    return jsonify({"response": response})

@app.route("/")
def index():
    return "Hello, this is your chatbot application!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

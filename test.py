from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_response(user_input, intents):
    user_input = user_input.lower()  # Convert user input to lowercase
    for intent in intents["intents"]:
        if user_input in map(str.lower, intent["patterns"]):  # Convert patterns to lowercase for comparison
            return random.choice(intent["responses"])
    return "I'm sorry, I don't understand."

@app.route('/')
def index():
    chatbot_config = load_config('chatbot_config.json')
    return render_template('index.html', chatbot_config=chatbot_config)

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.form['msg']
    chatbot_config = load_config('chatbot_config.json')
    bot_response = get_response(user_input, chatbot_config)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)

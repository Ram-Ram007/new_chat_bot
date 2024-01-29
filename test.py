from flask import Flask, render_template, request, jsonify
import json
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_response(user_input, intents):
    user_input = user_input.lower()  # Convert user input to lowercase
    for intent in intents["intents"]:
        if user_input in map(str.lower, intent["patterns"]):  # Convert patterns to lowercase for comparison
            return random.choice(intent["responses"])

    # If no response from intents, try web scraping
    scraped_response = scrape_website(user_input)
    if scraped_response:
        return scraped_response

    return random.choice(["Theriyala Bro", "crt aaa keelu da","Oru alavuku thaa bro"])

def scrape_website(query):
    # Example: Web scraping code to extract information from a website
    url = f'https://www.mediwavedigital.com/q={query}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract information based on HTML structure
        # For example, extract the text from the first paragraph
        first_paragraph = soup.find('p')
        if first_paragraph:
            return first_paragraph.get_text()

    return None

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
    app.run(debug=True,port=8000)

from flask import Flask, render_template, request, jsonify
import json
import random
import requests
from bs4 import BeautifulSoup
import os  # Add this import statement

app = Flask(__name__)

# OpenWeatherMap API key, replace 'YOUR_API_KEY' with your actual API key
OPENWEATHERMAP_API_KEY = 'ecee0f874624bd9269fff2db43b2cce6'

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': OPENWEATHERMAP_API_KEY, 'units': 'metric'}
    
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        return f"The weather in {city} is {main_weather} ({description}) with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't fetch the weather information at the moment."

def get_response(user_input, intents):
    user_input = user_input.lower()  

    if "weather" in user_input:
        # Extract city from user input using a more robust approach
        # For simplicity, assuming the city is the last word in the user input
        words = user_input.split()
        city = words[-1]
        return get_weather(city)

    for intent in intents["intents"]:
        if user_input in map(str.lower, intent["patterns"]): 
            return random.choice(intent["responses"])

    scraped_response = scrape_website(user_input)
    if scraped_response:
        return scraped_response

    return random.choice(["Theriyala Bro", "crt aaa keelu da", "Oru alavuku thaa bro"])

def scrape_website(query):
    url = f'https://www.mediwavedigital.com/q={query}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
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
    app.run(debug=True)

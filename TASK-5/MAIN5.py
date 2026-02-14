import streamlit as st
from datetime import datetime
import requests

# -------------------------
# Function to get current time
# -------------------------
def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

# -------------------------
# Function to get weather
# -------------------------
def get_weather(city="Chennai"):
    api_key = "************************" # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"The weather in {city} is {desc} with temperature {temp}°C."
        else:
            return "Sorry, I couldn't fetch the weather right now."
    except:
        return "Error connecting to the weather service."

# -------------------------
# Rule-based chatbot logic
# -------------------------
def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Dictionary of rules
    rules = {
        "hi": "Hello! How can I help you today?",
        "hello": "Hi there! How are you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "what is your name": "I am StreamBot, your rule-based assistant.",
        "bye": "Goodbye! Have a nice day!",
        "help": "You can ask me simple questions like greetings, my name, current time, or weather."
    }
    
    # Check for rules first
    for key in rules:
        if key in user_input:
            return rules[key]
    
    # Dynamic responses
    if "time" in user_input:
        return f"The current time is {get_current_time()}"
    
    if "weather" in user_input:
        # Optionally, you can detect city from input; for simplicity, using default city
        return get_weather()
    
    return "Sorry, I don't understand. Can you rephrase?"

# -------------------------
# Streamlit App UI
# -------------------------
st.title("🗨️ Enhanced Rule-Based Chatbot")

# Input box for user
user_input = st.text_input("You: ", "")

# Send button
if st.button("Send"):
    if user_input:
        response = chatbot_response(user_input)
        st.text_area("Bot:", value=response, height=100)

import streamlit as st
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import wikipedia
from datetime import datetime

# -------------------------
# Initialize text-to-speech
# -------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    # Using a list to display in Streamlit UI
    st.session_state.chat_history.append(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# -------------------------
# Voice Command Logic
# -------------------------
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("Listening... Speak now!")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-IN")
            return query.lower().strip()
        except Exception:
            return "none"

# -------------------------
# Streamlit UI Setup
# -------------------------
st.set_page_config(page_title="Spectra Voice Assistant", page_icon="🎙️")
st.title("🎙️ Spectra Mini Assistant")
st.subheader("Control your PC with your voice")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar info
st.sidebar.title("Commands to Try")
st.sidebar.markdown("""
- **Wikipedia:** "Who is Elon Musk?"
- **Time:** "What time is it?"
- **Web:** "Open YouTube" / "Google"
- **App:** "Open Edge"
""")

# The "Trigger" Button
if st.button("🔴 Click to Speak", use_container_width=True):
    query = take_command()
    
    if query != "none":
        st.session_state.chat_history.append(f"User: {query}")
        
        # 1. Wikipedia Search
        if "wikipedia" in query or "who is" in query or "what is" in query:
            speak("Searching Wikipedia...")
            search_query = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
            try:
                results = wikipedia.summary(search_query, sentences=2)
                speak(results)
            except:
                speak("I couldn't find information on that topic.")

        # 2. Time
        elif "time" in query:
            time_now = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time_now}")

        # 3. Web Apps
        elif "youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # 4. Open Edge
        elif "edge" in query:
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if os.path.exists(edge_path):
                speak("Opening Microsoft Edge")
                os.startfile(edge_path)
            else:
                speak("Edge path not found.")
        
        # 5. Greetings
        elif any(greet in query for greet in ["hello", "hi", "hey"]):
            speak("Hello! How can I help you today?")
            
        else:
            speak("Command not recognized.")
    else:
        st.warning("I didn't hear anything. Please try again.")

# Display Chat History
st.divider()
for message in reversed(st.session_state.chat_history):
    if "User:" in message:
        st.chat_message("user").write(message.replace("User: ", ""))
    else:
        st.chat_message("assistant").write(message.replace("Assistant: ", ""))
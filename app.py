import streamlit as st
from audiorecorder import audiorecorder
import speech_recognition as sr

# Define a simple chatbot response
def chatbot_response(user_input):
    responses = {
        "hello": "Hi there!",
        "how are you": "I'm a bot, so I'm always good!",
        "bye": "Goodbye!",
    }
    return responses.get(user_input.lower(), "I don't understand that.")

st.title("Chatbot with Speech Recognition")

# Record audio using audiorecorder
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    st.audio(audio.tobytes())
    st.write("Audio recorded successfully!")

    # Save audio file
    audio_path = "recorded_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(audio.tobytes())

    # Recognize speech using SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write(f"You said: {text}")

            # Get chatbot response
            response = chatbot_response(text)
            st.write(f"Chatbot: {response}")
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")

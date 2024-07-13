import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import speech_recognition as sr
import numpy as np

# Define a simple chatbot response
def chatbot_response(user_input):
    responses = {
        "hello": "Hi there!",
        "how are you": "I'm a bot, so I'm always good!",
        "bye": "Goodbye!",
    }
    return responses.get(user_input.lower(), "I don't understand that.")

st.title("Chatbot with Speech Recognition")

# WebRTC client settings
client_settings = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Capture audio from the microphone
webrtc_ctx = webrtc_streamer(
    key="audio",
    mode=WebRtcMode.SENDRECV,
    client_settings=client_settings,
)

if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    if audio_frames:
        # Convert audio to numpy array
        audio_frame = audio_frames[0]
        audio_data = np.frombuffer(audio_frame.to_ndarray(), np.int16)

        # Save audio data to a file
        audio_path = "recorded_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_data.tobytes())

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

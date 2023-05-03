import random
import requests
import speech_recognition as sr
import pyttsx3
from playsound import playsound

# Initialize SpeechRecognition and Sphinx
r = sr.Recognizer()
mic = sr.Microphone()

try:
    with mic as source:
        # Listen to microphone input
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        # Convert speech to text using Sphinx
        text = r.recognize_sphinx(audio)
    # Request TTS from remote API
    response = requests.post(url, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
    if response.status_code == 200:
        # Save remote TTS output to variable
        remote_output = response.content
        # Save remote TTS output to file
        with open('output-remote.mp3', 'wb') as f:
            f.write(remote_output)
        # Play remote TTS output
        playsound('output-remote.mp3')
    else:
        raise Exception(f"Remote TTS failed with status code {response.status_code}")
except Exception as e:
    # If remote TTS fails, use local TTS
    print(f"Remote TTS failed: {e}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # change the index to change voice
    engine.setProperty('VoiceAge', 90)
    engine.save_to_file(text, 'output-local.mp3')
    engine.runAndWait()
    playsound('output-local.mp3')

# Print the generated output to console
print(text)

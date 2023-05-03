import random
import requests
import pyttsx3
from playsound import playsound

# Read text from file
with open('generated_output.txt', 'r') as f:
    text = f.read().strip()

# Define a list of URL strings
url_list = [
    "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
    "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld",
    "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
    "https://api.elevenlabs.io/v1/text-to-speech/ErXwobaYiN019PkySvjV",
    "https://api.elevenlabs.io/v1/text-to-speech/MF3mGyEYCl7XYWbV9V6O",
    "https://api.elevenlabs.io/v1/text-to-speech/TxGEqnHWrfWFTfGW9XjX",
    "https://api.elevenlabs.io/v1/text-to-speech/VR6AewLTigWG4xSOukaG",
    "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
    "https://api.elevenlabs.io/v1/text-to-speech/yoZ06aMxZJJ28mfd3POQ",
]

CHUNK_SIZE = 1024
url = random.choice(url_list)  # Choose a URL string randomly

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "56c063b7c2565ae63674330602fd53e4"
}

try:
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
# print(text)

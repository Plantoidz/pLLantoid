import random
import requests
import pyttsx3
from playsound import playsound

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('x', type=str)

args = parser.parse_args()




# Read text from file
with open('./haikus/' + args.x, 'r') as f:
    text = f.read().strip()

# Define a list of URL strings
url_list = [
    "https://api.elevenlabs.io/v1/text-to-speech/GVujtglNiEdibm78n7Fw",
]

CHUNK_SIZE = 1024
url = random.choice(url_list)  # Choose a URL string randomly

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "yZ9OUSqs45j6A2GkseTx"
}

try:
    # Request TTS from remote API
    response = requests.post(url, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
    if response.status_code == 200:
        # Save remote TTS output to variable
        remote_output = response.content
        # Save remote TTS output to file
        with open('./haikus/mp3s/' + args.x + '.mp3', 'wb') as f:
            f.write(remote_output)
        # Play remote TTS output
        playsound('./haikus/mp3s/' + args.x + '.mp3')
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

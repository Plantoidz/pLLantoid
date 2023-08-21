import requests
import os
from threading import Lock
from datetime import datetime
from playsound import playsound

# Configuration
eleven_labs_api_key = "7392d8c1aed03a77decf691927128ba3"  # replace with your API key
voice_url = "https://api.elevenlabs.io/v1/text-to-speech/o7lPjDgzlF8ZloHzVPeK"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": eleven_labs_api_key
}
counter = 0
lock = Lock()

# Ensure the directory structure exists
current_mode = "default"
dir_structure = os.path.join("working", current_mode, "audio")
if not os.path.exists(dir_structure):
    os.makedirs(dir_structure)

# Function to send text to Eleven Labs API
def send_to_eleven_labs_api(text):
    global counter
    
    # Send the responses to Eleven Labs API
    response = requests.post(voice_url, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
    if response.status_code == 200:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with lock:  # Acquire lock before accessing counter
            filename = os.path.join(dir_structure, f"{timestamp}_response{counter}.mp3")
            counter += 1  # Safely increment counter
        
        with open(filename, "wb") as f:
            f.write(response.content)
            print(f"\n\nGenerating audio for: {filename}")
                    
        return filename
    else:
        print(f"Request to API failed with status code {response.status_code}.")
        return None

if __name__ == "__main__":
    text = input("Enter the text you want to convert to speech: ")
    audio_file = send_to_eleven_labs_api(text)
    if audio_file:
        playsound(audio_file)

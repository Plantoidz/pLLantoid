import requests
import pyttsx3
from playsound import playsound

# Read text from file
with open('generated_haiku.txt', 'r') as f:
    text = f.read().strip()

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "<your-key>"
}

data = {
  "text": text,
  "voice_settings": {
    "stability": 0,
    "similarity_boost": 0
  }
}

remote_tts_success = False

try:
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open('output-remote.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        remote_tts_success = True
except Exception as e:
    print(f"Remote TTS failed: {e}")

# Play the generated audio
if remote_tts_success:
    playsound('output-remote.mp3')
else:
    # Initialize pyttsx3
    engine = pyttsx3.init()

    # Set voice properties
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # change the index to change voice
    engine.setProperty('VoiceAge', 90)

    # Convert text to speech
    engine.save_to_file(text, 'output-local.mp3')
    engine.runAndWait()

    # Print message to indicate success
    print('local TTS complete!')
    playsound('output-local.mp3')

# Print message to indicate success
print('TTS process complete!')





# import requests
# import pyttsx3
# from playsound import playsound

# # Read text from file
# with open('generated_haiku.txt', 'r') as f:
#     text = f.read().strip()

# CHUNK_SIZE = 1024
# url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

# headers = {
#   "Accept": "audio/mpeg",
#   "Content-Type": "application/json",
#   "xi-api-key": "56c063b7c2565ae63674330602fd53e4"
# }

# data = {
#   "text": text,
#   "voice_settings": {
#     "stability": 0,
#     "similarity_boost": 0
#   }
# }

# response = requests.post(url, json=data, headers=headers)
# with open('output.mp3', 'wb') as f:
#     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#         if chunk:
#             f.write(chunk)

# # Print message to indicate success
# print('remote TTS complete!')

# # Play the generated audio
# playsound('output-remote.mp3')


# # Read text from file
# with open('generated_haiku.txt', 'r') as f:
#     text = f.read().strip()

# # Initialize pyttsx3
# engine = pyttsx3.init()

# # Set voice properties
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id) # change the index to change voice
# engine.setProperty('VoiceAge', 90)


# # Convert text to speech
# engine.save_to_file(text, 'output.mp3')
# engine.runAndWait()

# # Print message to indicate success
# print('local TTS complete!')

# # Play the generated audio
# playsound('output-local.mp3')
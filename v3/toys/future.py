import random
import subprocess
import requests
from playsound import playsound

# Define the five word arrays
# ... (the rest of the code for generating words) ...

# Call the haiku_generator.py script as a subprocess
haiku_process = subprocess.run(['python', 'haiku_generator.py', ecology_word, renewal_word, positivity_word, regeneration_word, indigenous_word], capture_output=True, text=True)
generated_haiku = haiku_process.stdout.strip()

# Print the output
print(generated_haiku)

# Set up API endpoint and API key
url = 'https://api.11labs.ai/v1/synthesize/tts'
api_key = 'your_api_key_here'

# Set up request parameters
payload = {
    'voice': 'en-US-Standard-D',
    'text': generated_haiku
}
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Send API request and save audio response to file
response = requests.post(url, json=payload, headers=headers)

with open('generated_haiku.wav', 'wb') as f:
    f.write(response.content)

# Play the generated haiku
playsound('generated_haiku.wav')

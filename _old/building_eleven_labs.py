# Read the text from the input file
with open(f'working/{current_mode}/audio/{timestamp}_{character}_responses.json', "r") as f:
    text = f.read()

# Choose a random URL string from the list
voice = "https://api.elevenlabs.io/v1/text-to-speech/o7lPjDgzlF8ZloHzVPeK"
url = (voice)

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": eleven_labs_api_key
}

    # Request TTS from remote API
response = requests.post(url, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
print(response.status_code)
if response.status_code == 200:
    # Save remote TTS output to a local audio file with an epoch timestamp
    filename = f"working/{current_mode}/audio/{timestamp}_response.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)
        print(f"Sermon saved to sermons/{timestamp}_sermon.mp3")
        
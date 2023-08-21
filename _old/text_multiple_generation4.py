import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Assuming these are defined elsewhere in your code:
voice = "https://api.elevenlabs.io/v1/text-to-speech/o7lPjDgzlF8ZloHzVPeK"
eleven_labs_api_key = "b74b7e7ae1605ee65d2f3e10145f54d0"  # replace with your API key

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": eleven_labs_api_key
}

counter = 0

def send_to_api(text):
    global counter

    response = requests.post(voice, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        # Use the counter for a sequential filename
        filename = f"affirmations/{counter}_affirmation.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
            print(f"Affirmation clips saved to {filename}")
        counter += 1
        return filename
    else:
        print(f"Request to API failed with status code {response.status_code}.")
        return None

def main():
    global counter
    counter = 0  # Resetting the counter to 0 at the beginning of main

    with open(f"analysis/test.json", "r") as file:
        texts = json.load(file)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(send_to_api, text) for text in texts}
        for future in as_completed(futures):
            print(f"Task completed with result: {future.result()}")

if __name__ == "__main__":
    main()

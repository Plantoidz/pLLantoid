import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

########  Affirmation  ########

voice = "https://api.elevenlabs.io/v1/text-to-speech/o7lPjDgzlF8ZloHzVPeK"
eleven_labs_api_key = "b74b7e7ae1605ee65d2f3e10145f54d0"  # replace with your API key

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": eleven_labs_api_key
}

def send_to_api(text):
    response = requests.post(voice, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        filename = f"affirmations/{text[:10]}_affirmation.mp3"  # Filename derived from the first 10 characters of the text
        with open(filename, "wb") as f:
            f.write(response.content)
            print(f"Affirmation clips saved to {filename}")
        return filename
    else:
        print(f"Request to API failed with status code {response.status_code}.")
        return None

def main():
    timestamp = int(time.time())  # Assuming the timestamp in the filename is the current time
    # with open(f"analysis/{timestamp}_affirmations.json", "r") as file:
    with open(f"analysis/test.json", "r") as file:
        texts = json.load(file)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(send_to_api, text) for text in texts}
        for future in as_completed(futures):
            print(f"Task completed with result: {future.result()}")

if __name__ == "__main__":
    main()
import json
import os
import requests

def send_to_eleven_labs_api_and_save(description, mode_name):
    url = "https://api.elevenlabs.io/v1/text-to-speech/o7lPjDgzlF8ZloHzVPeK"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "b74b7e7ae1605ee65d2f3e10145f54d0"
    }
    payload = {
        "text": description,
        "voice_settings": {"stability": 0, "similarity_boost": 0}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # Assuming the response content is an MP3 file
        with open(f"../modes/{mode_name}/beep_start.mp3", "wb") as mp3_file:
            mp3_file.write(response.content)
        print(f"Saved response for '{description}' as {mode_name}.mp3")
    else:
        print(f"Failed to send description: '{description}'. Status Code: {response.status_code}")

# Read JSON file
with open("../modes/modes_single_v2.json", "r") as json_file:
    data = json.load(json_file)
    for mode, mode_data in data["MODES"].items():
        dir_path = f"../modes/{mode}"

        # Check if directory exists
        if os.path.isdir(dir_path):
            print(f"Directory for mode '{mode}' exists. Skipping...")
            continue  # Skip the current iteration
        else:
            # Create the directory if it doesn't exist
            os.makedirs(dir_path)
            print(f"Created directory for mode '{mode}'")

        description = mode_data["description"]
        send_to_eleven_labs_api_and_save(description, mode)

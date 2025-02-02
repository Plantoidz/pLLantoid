from dotenv import load_dotenv
import traceback
import sys
import io
import logging
import pyaudio
import wave
import time
import openai
import requests
import json
from playsound import playsound
import tempfile
import os
import sounddevice as sd
import speech_recognition as sr
import numpy as np
import random
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import subprocess
import threading
from pydub import AudioSegment, effects
from pydub.playback import play
from pydub.generators import Sine
from io import BytesIO

# TODO — time it

# set the correct audio interface
def get_device_with_max_channels():
    devices = sd.query_devices()
    max_channels = 0
    max_device_id = None

    for device in devices:
        if device['max_output_channels'] > max_channels:
            max_channels = device['max_output_channels']
            max_device_id = device['index']
            # print(f"We have {max_channels} channels")


    if max_device_id is None:
        raise ValueError("No suitable device found.")
    
    return max_device_id, max_channels
    
def get_mode_data(file_path):
    # Load the dictionary from the given JSON file
    with open(file_path, 'r') as file:
        modes_dict = json.load(file)
    
    # Get the list of mode keys from the dictionary
    mode_keys = list(modes_dict["MODES"].keys())
    
    # Choose a mode key at random
    chosen_mode_key = random.choice(mode_keys)
    
    # Return the dictionary corresponding to that mode
    return modes_dict["MODES"][chosen_mode_key]

# Specify the path to your JSON file
file_path = 'modes/modes_single_v2.json'

# Get a random mode's data
current_mode_data = get_mode_data(file_path)
print(current_mode_data)

def initialize_mode_sounds():
    # Load the sounds
    
    ambient_sounds = [f'{current_mode}/ambient{i}.mp3' for i in range(1, 5)]
    acknowledgement_sounds = [f'{current_mode}/acknowledgement{i}.mp3' for i in range(1, 5)]
    understanding_sounds = [f'{current_mode}/understanding{i}.mp3' for i in range(1, 5)]
    greeting_sounds = [f'{current_mode}/greeting{i}.wav' for i in range(1, 5)]
    fail_sounds = [f'{current_mode}/fail{i}.wav' for i in range(1, 5)]
    problem_sounds = [f'{current_mode}/problem{i}.wav' for i in range(1, 5)]  # Adding problem sounds

    return (
        random.choice(ambient_sounds),
        random.choice(acknowledgement_sounds),
        random.choice(understanding_sounds),
        random.choice(greeting_sounds),
        random.choice(fail_sounds),
        random.choice(problem_sounds)
    )

    # Call the function and unpack the results into the respective variables
    ambient, acknowledgement, understanding, greeting, fail, problem = initialize_mode_sounds()

# load API keys
def load_api_keys():
    openai_key = "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"
    # TODO: remove API keys
    # openai_key = os.environ.get("OPENAI")
    if not openai_key:
        raise ValueError("OpenAI API key not found. Ensure the .env file has the correct key set.")
    else:
        openai.api_key = openai_key
    
    eleven_labs_api_key = os.environ.get("ELEVEN")
    
# load characters

#TODO: reconcile these into a single function
def load_character_configs(filename="working/config_characters_v2.json"):
    with open(filename, "r") as file:
        config = json.load(file)
        return config["characters"]

def load_characters_from_config(api, config_file="working/config_characters_v2.json"):
    character_configs = load_character_configs(config_file)
    
    for character_data in character_configs:
        character = Character(
            character_data["name"],
            character_data["description"],
            character_data["system_message"],
            character_data["default_channel"],
            character_data["eleven_voice_id"]
        )
        api.assign_character(character)

# announce the session
def announce_session():
    timestamp = str(int(time.time()))
    config_data = get_mode_data()
    if config_data:
        for key, value in config_data.items():
            globals()[key] = value
    if config_data and 'current_mode' in config_data:
        print(f"\n\nCurrent mode is: {config_data['current_mode']}")
    else:
        print("Unable to retrieve current mode.")

class Character:
    def __init__(self, name, description, system_message, default_channel, eleven_voice_id):
        self.name = name
        self.description = description
        self.system_message = system_message
        self.default_channel = default_channel
        self.eleven_voice_id = eleven_voice_id
        self.device_id, self.max_channels = get_device_with_max_channels()

class ChannelAPI:
    
    def __init__(self):
        self.channels = {}
        self.characters = {}
        self.sound_playback_lock = threading.Lock() # Create a lock for sequential sound playback
        self.audio_playback_complete = threading.Event() # Create a signal that all sound playback is complete

    def assign_character(self, character):
        if character.default_channel in self.channels:
            print(f"Channel {character.default_channel} already has a character assigned.")
            return False
        self.channels[character.default_channel] = character.name
        self.characters[character.default_channel] = character
        print(f"\n\nAssigned {character.name} to channel {character.default_channel}.")
        return True
    
    def get_assigned_character(self, channel):
        return self.characters.get(channel, None)
    
    def process_text_and_synthesize(self, channel, text, timestamp):
        character = self.get_assigned_character(channel)
        if character is None:
            print(f"\n\nNo character assigned to channel {channel}.")
            return

        def worker(channel, text, character, timestamp):
            # Sending request to remote text processing API
            processed_text = self.send_to_language_model(text, character, timestamp)
            # Sending to remote audio synthesis API
            audio_data, audio_filename = self.send_to_audio_synthesis(channel, processed_text, timestamp)
            # Route the synthesized audio to the assigned channel
            # Use the lock to ensure sequential sound playback
            # with self.sound_playback_lock:
            self.route_to_channel(channel, audio_data, audio_filename, character.max_channels, character.device_id)

    #     # Start the workers
    #     threading.Thread(target=worker, args=(channel, text, character, timestamp)).start()

    #TODO: stagger the initiation of the threads — maybe good for low powered devices 

        self.start_threads_staggered(worker, channel, text, character, timestamp)

    def send_to_language_model(self, text, character, timestamp):

        #TODO: reintroduce chainable prompts

        # # Extract the analysis from the recording
        # prompt = f"{reasoning_prompt1}:\n\n{text}."
        # # print("Prompt:\n\n" + prompt)
        # response = openai.Completion.create(
        #     engine=model_id,
        #     prompt=prompt,
        #     max_tokens=max_tokens
        # )

        # # Save the analysis to a local file with an epoch timestamp
        # filename = f"working/{current_mode}/analysis/{timestamp}_{character.name}_analysis.txt"
        # with open(filename, "w") as f:
        #     f.write(response.choices[0].text)
        # reasoning_prompt1_analysis = response.choices[0].text
        # # print(f"\n\n{reasoning_prompt1_msg}:\n\n{reasoning_prompt1_analysis}")

        # Come up with responses
        prompt = f"{responding_prompt1}\n\n'{text}.'"
        # print(f"Response prompt:\n\n{prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{character.system_message}"},
                {"role": "user", "content": f"{prompt}"}
                ]
            )
        # Save the responses to a local file with an epoch timestamp
        filename = f"working/{current_mode}/audio/{timestamp}_{character.name}_responses.json"
        with open(filename, "w") as f:
            f.write(response.choices[0]['message']['content'])
        responses = response.choices[0]['message']['content']
        #TODO: fix the logging so we can see the character
        print(f"\n\n{character.name} response:\n\n{responses}")
        return responses

    def send_to_audio_synthesis(self, channel, processed_text, timestamp):

        character = self.get_assigned_character(channel)

        eleven_voice_id = character.eleven_voice_id

        if character is None:
            print(f"No character assigned to channel {channel}.")
            return

        # Read the text from the input file
        with open(f'working/{current_mode}/audio/{timestamp}_{character.name}_responses.json', "r") as f:
            text = f.read()

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": "b74b7e7ae1605ee65d2f3e10145f54d0"
        }

        # Request TTS from remote API
        response = requests.post(eleven_voice_id, json={"text": text, "voice_settings": {"stability": 0, "similarity_boost": 0}}, headers=headers)
        # print(f"ElevenLabs API response: {response.status_code}")
        if response.status_code:
            # Save remote TTS output to a local audio file with an epoch timestamp
            filename = f"working/{current_mode}/audio/{timestamp}_{character.name}_response.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
                # print(f"\n\nGenerating audio for working/{current_mode}/audio/{timestamp}_{character.name}_response.mp3")
        return response.content, filename

    def start_threads_staggered(self, worker_func, channel, text, character, timestamp, delay=0):
        # Start the thread
        threading.Thread(target=worker_func, args=(channel, text, character, timestamp)).start()
        # Sleep for the specified delay time
        time.sleep(delay)
       
    def route_to_channel(self, channel, audio_data, filename, max_channels, max_device_id):
        character = self.get_assigned_character(channel)
        if character is None:
            print(f"No character assigned to channel {channel}.")
            return

        # Load audio file using pydub from disk
        # TODO: just read the audio data, it will save on IO
        sound = AudioSegment.from_file(filename, format="mp3")

        # Convert sound to numpy array and normalize
        samples = np.array(sound.get_array_of_samples()).astype(np.float32) / (2**15)
        # print(max_channels) #8
        # print(max_device_id) #0
        max_output_channels = sd.query_devices(max_device_id)['max_output_channels']

        if max_channels == 2:
            channel = 0

        if channel >= max_output_channels:
            raise ValueError(f"The device only has {max_channels} output channel(s).")

        # Create an empty array with the correct number of output channels
        zeros = np.zeros((len(samples), max_output_channels), dtype=np.float32)

        # Copy the mono audio data to the desired channel
        zeros[:, channel] = samples

        # Wait for previous sound to finish
        # self.audio_playback_complete.wait()

        # Lock sound playback
        with self.sound_playback_lock:
            # Reset the event indicating that sound playback has started
            self.audio_playback_complete.clear()

            # Stream the audio 
            # TODO: better logging
            # print(f"\n\n{self.character} speaking on {self.channel}")
            with sd.OutputStream(device=max_device_id, channels=max_output_channels, samplerate=sound.frame_rate) as stream:
                stream.write(zeros)

                # # Check for the stream's active status
                # while stream.active:
                #     time.sleep(0.1)  # Wait for a short duration before checking again

            # # Reset the event for the next run
            self.audio_playback_complete.set()

        pass

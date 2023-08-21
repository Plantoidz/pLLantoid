from dotenv import load_dotenv
import sys
import os
import time
import io
import logging
import requests
import json
from playsound import playsound
import tempfile
import traceback
import sounddevice as sd
import speech_recognition as sr
import random
import subprocess
import threading
from io import BytesIO
from embodiment_api import get_device_with_max_channels, get_mode_data,load_api_keys, load_character_configs, load_characters_from_config, announce_session, Character, ChannelAPI


# atmospherics before loading a mode
def initialize_global_sounds():
    base_path = 'global/media/'
    
    ambient_sounds = [f'{base_path}ambient{i}.mp3' for i in range(1, 5)]
    acknowledgement_sounds = [f'{base_path}acknowledgement{i}.mp3' for i in range(1, 5)]
    greeting_sounds = [f'{base_path}greeting{i}.wav' for i in range(1, 5)]
    fail_sounds = [f'{base_path}fail{i}.wav' for i in range(1, 5)]
    problem_sounds = [f'{base_path}problem{i}.wav' for i in range(1, 5)]  # Adding problem sounds

    return (
        random.choice(ambient_sounds),
        random.choice(acknowledgement_sounds),
        random.choice(greeting_sounds),
        random.choice(fail_sounds),
        random.choice(problem_sounds)
    )

ambient, acknowledgement, greeting, fail, problem = initialize_global_sounds()

def wait_for_wake_word(r):
    """Wait for the wake word to be spoken."""
    logging.info("Waiting for wake word...")
    wake_phrases = ["Ready", "Reading", "Red tea", "Rudy", "Ton", "Tone", "Listening", "Activate", "Rody", "Leaving", "Heavy", "Tony", "Danny", "Wake", "Ruddy"]

    with sr.Microphone() as source:

        while True:

            print("I'm listening...")
            # Listen for speech and store it as audio data
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, 10, 3)
            text = ""

            try:
                # Recognize the speech input using Google Speech Recognition
                text = r.recognize_google(audio)

            except sr.UnknownValueError:
                pass # print("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                print("\n\nCould not request results from Google Speech Recognition service; {0}".format(e))
                exit()

            if(text):
                print("I heard: " + text)

                for phrase in wake_phrases:
                    if phrase.lower() in text.strip().lower():
                        print(f"\n\nWake phrase detected!")
                        playsound(greeting)  # Play the greeting sound
                        return

def passive_listener():
   # TODO: looping
   # TODO: give up if too many tries
    # Initialize the recognizer
    r = sr.Recognizer()

    # Set the microphone as the source
    time.sleep(1)  # wait for 1 second
    
    """Run continuously, restarting on error."""
    while True:
        try:
            # text = wait_for_wake_word(r)
            activate_chatter(r)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        time.sleep(1)

def activate_chatter(r):
    # TODO: ensure no audio is playing
    # TODO: take one of the previous inputs to enable the chatter to go indefinitely (audio from outside the system feeding back in)
    print("\n\nChatter activated!")
    api = ChannelAPI()
    # TODO: get the current mode first
    playsound(f"global/media/beep_start.mp3")
    with sr.Microphone() as source:
        # TODO: kill if too many tries

        # Begin transcribing microphone audio stream
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 100, 10)
        time.sleep(1)
        playsound(acknowledgement)

        text = ""

        try:
            # Recognize the speech input using Google Speech Recognition
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("\n\nGoogle Speech Recognition could not understand audio")
            playsound(fail)
        except sr.RequestError as e:
            print("\n\nCould not request results from Google Speech Recognition service; {0}".format(e))
            playsound(problem)
            exit()

        if text:
            print("I heard: " + text)
            playsound(acknowledgement)
            #TODO: play ambient sound on n channel (not plantoids)
            load_characters_from_config(api)
            timestamp = str(int(time.time()))  # Get a current timestamp
            for channel in api.channels.keys():
                api.process_text_and_synthesize(channel, text, timestamp)

# TODO: long-term memory

                # turns.append({"speaker": USER_NAME, "text": text})

                # prompt = inject_transcript_into_prompt(turns, episode.prompt_text)
                # print(prompt)

                # # Generate the response from the GPT model
                # gptmagic(turns, prompt)

                # stop_event.set()
                # sound_thread.join()

                # time.sleep(1)
                # playsound("modes/plantony/media/beep_stop.wav")

#TODO: better debugging modes where we can pass values through CLI
if __name__ == "__main__":
    load_api_keys()
    initialize_global_sounds()
    get_mode_data()
    current_mode = get_mode_data()
    r = sr.Recognizer()  # Initialize r here
    # wait_for_wake_word(r)
    # announce_session()
    activate_chatter(r)
    # passive_listener()

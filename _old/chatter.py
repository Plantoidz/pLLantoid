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
import socket
from embodiment import get_device_with_max_channels, get_mode_data, load_character_configs, load_characters_from_config, Character, ChannelAPI

chatter_finished_event = threading.Event()

def poke_network_once(host="8.8.8.8", port=53):
    """
    Opens a socket connection to a host once to keep the network active.
    
    Args:
    - host (str): The hostname or IP address of the target system.
    - port (int): The port number to connect to. Default is 53 (DNS).
    """
    try:
        with socket.create_connection((host, port), timeout=1):
            print(f"Kept the connection active by connecting to {host}:{port}")
    except Exception as e:
        print(f"Failed to connect to {host}:{port}. Error: {e}")
        sys(exit)

def wait_for_wake_word(r):
    """Wait for the wake word to be spoken."""
    greeting_sounds = ['global/media/greeting1.mp3', 'global/media/greeting2.mp3', 'global/media/greeting3.mp3', 'global/media/greeting4.mp3']
    greeting = random.choice(greeting_sounds)


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

            if(text):
                print("I heard: " + text)

                for phrase in wake_phrases:
                    if phrase.lower() in text.strip().lower():
                        print(f"\n\nWake phrase detected!")
                        playsound(greeting, block=False)  # Play the greeting sound
                        activate_chatter(r)
                        # chatter_finished_event.set()  # TODO: Signal that activate_chatter has finished
                        return

def activate_chatter(r):
    time.sleep(1)
    current_mode, responding_prompt1 = get_mode_data()
    timestamp = str(int(time.time()))
    print("\n\nChatter activated!")
    api = ChannelAPI(current_mode=f"{current_mode}")

    with sr.Microphone() as source:
        print("\n\nI'm listening...")
        
        audio = r.listen(source, 90, 30)

        with open(f"working/{current_mode}/recordings/{timestamp}_recording.wav", "wb") as f:
            f.write(audio.get_wav_data())

        problem_sounds = ['global/media/problem1.mp3', 'global/media/problem2.mp3', 'global/media/problem3.mp3', 'global/media/problem4.mp3', 'global/media/problem5.mp3']
        fail_sounds = ['global/media/fail1.mp3', 'global/media/fail2.mp3', 'global/media/fail3.mp3', 'global/media/fail4.mp3', 'global/media/fail5.mp3', 'global/media/fail6.mp3', 'global/media/fail7.mp3', 'global/media/fail8.mp3', 'global/media/fail9.mp3']
        ack_sounds = ['global/media/acknowledgement1.mp3', 'global/media/acknowledgement2.mp3', 'global/media/acknowledgement3.mp3', 'global/media/acknowledgement4.mp3', 'global/media/acknowledgement5.mp3', 'global/media/acknowledgement6.mp3', 'global/media/acknowledgement7.mp3']
        ambient_sounds = ['global/media/ambient1.mp3', 'global/media/ambient2.mp3', 'global/media/ambient3.mp3']
        problem = random.choice(problem_sounds)
        fail = random.choice(fail_sounds)
        ack = random.choice(ack_sounds)
        ambient = random.choice(ambient_sounds)

        playsound(ack, block=False)

        text = ""

        # MAX_RETRIES = 3
        # retry_count = 0

        # while retry_count < MAX_RETRIES:
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("\n\nGoogle Speech Recognition could not understand audio")
            playsound(fail)
            # retry_count += 1
            # if retry_count == MAX_RETRIES:
            print("Max retries reached. Exiting.")
            return
        except sr.RequestError as e:
            print("\n\nCould not request results from Google Speech Recognition service; {0}".format(e))
            playsound(problem)
            # sys.exit()

        if text:
            print("\n\nI heard: " + text)

            # Record the transcript with a timestamp
            with open(f"working/{current_mode}/recordings/{timestamp}_recording.txt", "w") as f:
                f.write(text)
            
            playsound(ambient, block=False)

            load_characters_from_config(api)
            for channel in api.channels.keys():
                api.process_text_and_synthesize(channel, text, timestamp, responding_prompt1)

#TODO: better debugging modes where we can pass values through CLI
if __name__ == "__main__":
    # TODO: listener event for Arduino (red LEDs)
    poke_network_once()
    # playsound("global/media/cleanse.mp3")
    r = sr.Recognizer()  # Initialize r here
    wait_for_wake_word(r) 
    # chatter_finished_event.wait() 
    # playsound("global/media/cleanse.mp3")
    # os.execv(sys.executable, ['python'] + sys.argv)

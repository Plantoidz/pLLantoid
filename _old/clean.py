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
from embody import get_device_with_max_channels, get_mode_data, load_character_configs, load_characters_from_config, Character, ChannelAPI

def wait_for_wake_word(r):
    """Wait for the wake word to be spoken."""
    logging.info("Waiting for wake word...")
    wake_phrases = ["Ready", "Reading", "Red tea", "Rudy", "Ton", "Tone", "Listening", "Activate", "Rody", "Leaving", "Heavy", "Tony", "Danny", "Wake", "Ruddy"]

    with sr.Microphone() as source:

        while True:

            print("I'm listening...")
            # Listen for speech and store it as audio data
            r.adjust_for_ambient_noise(source, 5)
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
    timestamp = str(int(time.time()))
    print("\n\nChatter activated!")
    api = ChannelAPI(current_mode=f"{current_mode}")

    # TODO: kill if too many tries

    with sr.Microphone() as source:
    
        # Begin transcribing microphone audio stream
        print("\n\nI'm listening...")
        # TODO: listener event for Arduino (red LEDs)
        r.adjust_for_ambient_noise(source)

        # TODO: tune these parameters
        
        audio = r.listen(source, 100, 10)

        # TODO: write this to file

        with open(f"working/{current_mode}/recordings/{timestamp}_recording.wav", "wb") as f:
            f.write(audio.get_wav_data())

        time.sleep(1)

        # TODO: play ambient sound

        ack_sounds = ['global/media/acknowledgement1.mp3', 'global/media/acknowledgement2.mp3', 'global/media/acknowledgement3.mp3', 'global/media/acknowledgement4.mp3']
        ack = random.choice(ack_sounds)
        playsound(ack, block=False)

        text = ""

        try:
            # Recognize the speech input using Google Speech Recognition
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("\n\nGoogle Speech Recognition could not understand audio")
            # playsound(fail)
        except sr.RequestError as e:
            print("\n\nCould not request results from Google Speech Recognition service; {0}".format(e))
            # playsound(problem)

        if text:
            print("\n\nI heard: " + text)

            # Record the transcript with a timestamp
            with open(f"working/{current_mode}/recordings/{timestamp}_recording.txt", "w") as f:
                f.write(text)
            
            # TODO: reintroduce ambient sounds
            ambient_sounds = ['global/media/ambient1.mp3', 'global/media/ambient1.mp3', 'global/media/ambient2.mp3', 'global/media/ambient4.mp3']
            ambient = random.choice(ambient_sounds)
            playsound(ambient, block=False)

            load_characters_from_config(api)
            for channel in api.channels.keys():
                api.process_text_and_synthesize(channel, text, timestamp, responding_prompt1)


#TODO: better debugging modes where we can pass values through CLI
if __name__ == "__main__":
    current_mode, responding_prompt1 = get_mode_data()
    # TODO: listener event for Arduino (red LEDs)
    r = sr.Recognizer()  # Initialize r here
    # wait_for_wake_word(r) 
    # passive_listener()
    activate_chatter(r)
    # playsound("global/media/cleanse.mp3")
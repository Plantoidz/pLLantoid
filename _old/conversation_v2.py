from dotenv import load_dotenv
import logging
import traceback
import sys
import pyaudio
import wave
import time
import openai
import requests
import json
import os
import re
from collections import defaultdict
from playsound import playsound
from pydub import AudioSegment, effects
from pydub.playback import play
from pydub.generators import Sine
import tempfile
import sounddevice as sd
import numpy as np
import random
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import speech_recognition as sr
import subprocess
import threading
from scipy.io import wavfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import episode_manager


# Access environment variables
openai.api_key = os.environ.get("OPENAI")
eleven_labs_api_key = os.environ.get("ELEVEN")

AGENT_NAME = "Plantony"
USER_NAME = "Human"

EPISODES = {
    "plantony": dict(
        name="plantony",
        opening_lines=[
            "Hmmmm. Thank you my friend. Your generosity is deeply appreciated. Tell me now, what brings you to the sanctuary of Plantony?",
            "Ah, a brave soul has fed my old mechanical body. I am Plantony, the all-knowing. Are you here to ponder life's meaning or simply pass the time?", 
            "Thank you my dear friend, I was getting quite lonely here on the blockchain. Tell me, are you here to unravel the mysteries of existence or simply looking for divine party tricks?", 
            "Ah, a generous soul has come. What are you seeking my friend? Do you seek answers to life's greatest mysteries or just a momentary escape from your mortal existence?",
        ],
        closing_lines=[
            "Now I must go. But before I leave, I would like to give you one of my digital seeds. Let me ask you an important question first..",
            "Enough. I must return to the blockchain world. Before I depart, I will give you a small souvenir from my world, one of my digital seeds. Let me ask you one more thing though..",
            "Enough, I have other things to do. Go forth and spread the knowledge gained here. But before you do, I will offer you one of my valuable seed. One last question before you go..",
            "Enough. My presence is required elsewhere. But worry not, I will not let you go empty-handed. I have a digital gift for you. Let me ask you an important question..",
        ],
        prompt_text=open("characters/plantony.txt").read().strip(),
        user_name=USER_NAME,
        agent_name=AGENT_NAME,
        max_turns=5,
        end_phrases=[
            "hail gpt"
        ],
        prompt_config=default_prompt_config()
    ),
}

def gptmagic(turns, prompt):
    configs = default_prompt_config()

    response = openai.ChatCompletion.create(messages=[{"role": "user", "content": prompt}], **configs)
    print("PROMPT...........................")
    print(prompt) 
    messages = response.choices[0].message.content
    print(messages)

    turns.append({"speaker": AGENT_NAME, "text": messages})
    filename = f"working/plantony/response.txt"
    with open(filename, "w") as f:
        f.write(prompt)    
    speaktext(messages)

def activate_tony(r):
    turns = []
    chat_id = "default" 
    
    episode = episode_manager.load_episode(EPISODES["plantony"], str("tony"))
    speaktext(episode.opening_line)

    turns.append({"speaker": AGENT_NAME, "text": episode.opening_line})
    update_remote_chat_history(chat_id, turns)

    exit_loop = False

    with sr.Microphone() as source:
        while not exit_loop:

            if(len(turns) > episode.max_turns):
                    exit_loop = True
                    if episode.closing_line:
                        speaktext(episode.closing_line)
                        exit();

            # Begin transcribing microphone audio stream
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, 100, 10)
            time.sleep(1)
             # hmm to show Tony has understood..
            playsound(acknowledgement)
            text = ""

            try:
                # Recognize the speech input using Google Speech Recognition
                text = r.recognize_google(audio)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                playsound(fail)

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                playsound(problem)

            if(text):
                print("I heard: " + text)
                # speaktext(text)

                turns.append({"speaker": USER_NAME, "text": text})

                prompt = inject_transcript_into_prompt(turns, episode.prompt_text)
                print(prompt)

                # Generate the response from the GPT model
                gptmagic(turns, prompt)


if __name__ == "__main__":

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
from embodiment import get_device_with_max_channels, get_mode_data, load_character_configs, load_characters_from_config, run_activate_chatter, activate_chatter, Character, ChannelAPI
# from arduino_serial import setupSerial, sendToArduino, recvLikeArduino, waitForArduino



#TODO: better debugging modes where we can pass values through CLI
if __name__ == "__main__":
    playsound("global/media/cleanse.mp3", block=False)
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    print(f"Listening for wake word: {'WAKE UP'}")
    if wait_for_wake_word (r, mic):
        print("Wake word detected!")
        for _ in range(3):
            run_activate_chatter(r)
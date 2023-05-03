import os
import pyttsx3
import subprocess
from playsound import playsound
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('x', type=str)

args = parser.parse_args()

input_file = "./haikus/"+args.x
output_file = "./haikus/mp3s/"+args.x+".wav"

# Check if the input file exists
if not os.path.exists(input_file):
    # If it doesn't exist, create it with some default text
    with open(input_file, "w") as f:
        f.write("This is some default text.")

engine = pyttsx3.init()

with open(input_file, "r") as f:
    text = f.read()

engine.save_to_file(text, output_file)
engine.runAndWait()

# Use subprocess.run to invoke the espeak command
subprocess.run(["espeak", "-w", output_file, text, "-v", "en+f5"])

# Play the sound
playsound(output_file)

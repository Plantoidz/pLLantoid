import os
import pyttsx3
from playsound import playsound

input_file = "generated_output.txt"
output_file = "output-local.wav"

engine = pyttsx3.init()

with open(input_file, "r") as f:
    text = f.read()

engine.save_to_file(text, output_file)
engine.runAndWait()

os.system(f"espeak -w {output_file} '{text}' -v en+croak")

# Play the sound
playsound(output_file)

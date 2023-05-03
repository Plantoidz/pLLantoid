import os
import pyttsx3
from playsound import playsound

input_file = "workspace/generated_output.txt"
output_file = "output-local.wav"

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

os.system(f"espeak -w {output_file} '{text}' -v en+croak")

# Play the sound
playsound(output_file)

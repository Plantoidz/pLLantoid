import random
from gtts import gTTS
import subprocess
import sys
import pygame
import os
import time
import os
from llama_cpp import Llama

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Initialize pygame mixer
pygame.mixer.init()



# List of ambient sounds
ambient_sounds = [
    'wav/ambient1.mp3',
    'wav/ambient2.mp3',
    'wav/ambient3.mp3',
    'wav/ambient4.mp3',
    'wav/ambient5.mp3'
]

# Choose a random ambient sound
ambient_sound = random.choice(ambient_sounds)

# Load the sound into pygame mixer
pygame.mixer.music.load(ambient_sound)

# Start playing the ambient sound
pygame.mixer.music.play(loops=-1)

#get the file name from epoch
timename = sys.argv[1]

# Get the generated_input variable from the command-line arguments
generated_input = sys.argv[2]

# Format the text as a string
prompt = f"### Instruction: You live in the future. Write a short poem about {generated_input}. ### Response:"

llm = Llama(model_path="../models/ggml-alpaca-7b-q4.bin")
output = llm(prompt, max_tokens=100, echo=True)

# Extract the response from the LLM
generated_text = output['choices'][0]['text']

# Print the instruction and response
print(f"Generated text: {generated_text}")  

# Extract the text after ### Response:
generated_output = generated_text.split('### Response:')[1].strip()

# Print just the response
print(f"Cleaned up text: {generated_output}")  

# Stop playing the ambient sound
pygame.mixer.music.stop()

# Write generated haiku to file

cwd = os.getcwd() 
fh = cwd + '/haikus/' + timename

with open(fh, 'w') as f:
    f.write(generated_output)

# with open('generated_output.txt', 'w') as f:
#    f.write(generated_output)

sys.exit()

import random
from gtts import gTTS
from playsound import playsound
import subprocess

# Define the five word arrays
ecology_words = ['sustainability', 'conservation', 'biodiversity', 'ecosystem', 'green']
renewal_words = ['regrowth', 'rejuvenation', 'rebirth', 'restoration', 'replenishment']
positivity_words = ['optimism', 'hope', 'prosperity', 'joy', 'happiness']
regeneration_words = ['renewal', 'revitalization', 'redevelopment', 'reconstruction', 'reestablishment']
indigenous_words = ['ancestral', 'traditional', 'native', 'aboriginal', 'indigenous']

# Randomly select one word from each of the five arrays
ecology_word = random.choice(ecology_words)
renewal_word = random.choice(renewal_words)
positivity_word = random.choice(positivity_words)
regeneration_word = random.choice(regeneration_words)
indigenous_word = random.choice(indigenous_words)

# Format the text as a string
haiku = f"### Instruction: Write a hopeful note from the future, evoking: {ecology_word}, {renewal_word}, {positivity_word}, {regeneration_word}, {indigenous_word}. ### Response:"

from llama_cpp import Llama
llm = Llama(model_path="./models/ggml-alpaca-7b-q4.bin")
output = llm(haiku, max_tokens=32, echo=True)

# Extract the generated haiku from the output
generated_text = output['choices'][0]['text']
# Extract the haiku text after ### Response:
generated_haiku = generated_text.split('### Response:\n')[1].strip()

# Print the output
print(generated_haiku)

# Write generated haiku to file
with open('generated_haiku.txt', 'w') as f:
    f.write(generated_haiku)

# Call TTS script using subprocess
subprocess.run(['python3', 'tts_script.py'])

# # Extract the generated haiku from the output
# generated_text = output['choices'][0]['text']
# # Extract the haiku text after ### Response:
# generated_haiku = generated_text.split('### Response:\n')[1].strip()

# # Cut off anything after the last period in the generated haiku
# last_period_index = generated_haiku.rfind('.')
# if last_period_index != -1:
#     generated_haiku = generated_haiku[:last_period_index+1]

# # Print the resulting generated haiku
# print(generated_haiku)

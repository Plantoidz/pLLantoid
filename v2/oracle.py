import random
from gtts import gTTS
import subprocess
import sys

from llama_cpp import Llama

# Get the generated_input variable from the command-line arguments
generated_input = sys.argv[1]

# Format the text as a string
prompt = f"### Instruction: Write a short poem, including the words: {generated_input}. ### Response:"

llm = Llama(model_path="./models/ggml-alpaca-7b-q4.bin")
output = llm(prompt, max_tokens=32, echo=True)

# Extract the response from the LLM
generated_text = output['choices'][0]['text']

# Print the instruction and response
print(f"Generated text: {generated_text}")  

# Extract the text after ### Response:
generated_output = generated_text.split('### Response:')[1].strip()

# Print just the response
# print(f"Cleaned up text: {generated_output}")  

# Write generated haiku to file
with open('generated_output.txt', 'w') as f:
    f.write(generated_output)

sys.exit()

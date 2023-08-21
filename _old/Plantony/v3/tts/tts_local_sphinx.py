import os
from pocketsphinx import AudioFile, get_model_path

# Set the path to the generated_output.txt file
text_file = 'generated_output.txt'

# Set the path to save the output file
output_file = 'output-local.wav'

# Set the language model and dictionary paths
model_path = get_model_path()
lm_path = os.path.join(model_path, 'en-us.lm.bin')
dict_path = os.path.join(model_path, 'cmudict-en-us.dict')

# Open the generated_output.txt file and convert it to speech
with open(text_file, 'r') as file:
    text = file.read().replace('\n', ' ')

# Create the AudioFile object
audio = AudioFile(audio_file=output_file,
                  lm=lm_path,
                  dic=dict_path)

# Convert the text to speech and save the output file
audio.from_text(text)
audio.save()

# Play the file
from playsound import playsound
playsound(output_file)

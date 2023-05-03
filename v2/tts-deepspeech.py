import deepspeech
import wave
import io
from playsound import playsound

# Read text from file
with open('generated_output.txt', 'r') as f:
    text = f.read().strip()

# Load DeepSpeech model
model_path = 'path/to/deepspeech-model.pbmm'
model = deepspeech.Model(model_path)
model.enableExternalScorer('path/to/deepspeech-scorer.scorer')

# Synthesize speech using DeepSpeech
with wave.open('output-local.wav', 'wb') as wave_file:
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(44100)
    wave_data = model.synthesize(text)
    wave_file.writeframes(wave_data)

# Play the synthesized speech
playsound('output-local.wav')

# Print the generated output to console
# print(text)

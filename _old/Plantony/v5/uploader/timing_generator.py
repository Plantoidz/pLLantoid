import speech_recognition as sr

# Create a recognizer object
r = sr.Recognizer()

# Load the audio file
with sr.AudioFile('audio.wav') as source:
    # Use the recognizer to record the audio
    audio = r.record(source)

# Use Google Cloud Speech-to-Text to transcribe the audio
text = r.recognize_google(audio)

# Get the timing information for each word in the transcription
timing_info = r.recognize_google(audio, show_all=True)

# Print the text and timing information
print(text)
print(timing_info)

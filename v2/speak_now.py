import random
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import speech_recognition as sr
import subprocess
import threading
import playsound


# Initialize the recognizer
r = sr.Recognizer()

# Define the list of sound files
ambient_sounds = [
    'wav/ambient1.mp3',
    'wav/ambient2.mp3',
    'wav/ambient3.mp3',
    'wav/ambient4.mp3',
    'wav/ambient5.mp3'
]

# Load the start and stop beep sound files
beep_start = 'wav/beep1.wav'
beep_stop = 'wav/beep5.wav'

# Play the start beep
playsound.playsound(beep_start)

# Set the microphone as the source
with sr.Microphone() as source:

    print("Leave a message for the future...")
    # Listen for speech and store it as audio data
    audio = r.listen(source)

# Use the recognizer to convert speech to text
try:
    # Recognize the speech input using Google Speech Recognition
    text = r.recognize_google(audio)
    print("I heard: " + text)

    # Split the text into words
    words = text.split()

    # Filter out the stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Filter out the frequently occurring words
    fdist = FreqDist(nltk.corpus.brown.words())
    common_words = set([word.lower() for word, count in fdist.most_common(50)])
    filtered_words = [word for word in filtered_words if word.lower() not in common_words]

    # Shuffle the filtered words randomly
    random.shuffle(filtered_words)

    # Select the first five words
    selected_words = filtered_words[:5]

    # Combine the selected words into a single string
    generated_input = " ".join(selected_words)

    # Print the output
    print("I resonate with these concepts: " + generated_input)

    # Spawn the LLM subprocess and pass the generated_input variable as a command-line argument
    oracle_process = subprocess.Popen(['python3', 'oracle.py', generated_input])

    # Play a random ambient sound while waiting for the first subprocess to complete
    ambient_sound = random.choice(ambient_sounds)
    sound_thread = threading.Thread(target=playsound.playsound, args=(ambient_sound,))
    sound_thread.start()

    # Wait for the first subprocess to complete before starting the second subprocess
    oracle_process.wait()

    # Stop playing the ambient sound
    playsound.playsound(beep_stop)

    # Call the TTS subprocess using subprocess
    tts_process = subprocess.run(['python3', 'tts_script.py'])

except sr.UnknownValueError:
    print("I couldn't understand you.")
except sr.RequestError as e:
    print("I can't reach the internet; {0}".format(e))
except Exception as e:
    print("An error occurred: {0}".format(e))

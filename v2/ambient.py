import speech_recognition as sr
import random
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import subprocess

# Download the stop words list and the Brown corpus
nltk.download('stopwords')
nltk.download('brown')

# Initialize the recognizer
r = sr.Recognizer()

# Initialize Pygame mixer for playing sounds
pygame.mixer.init()

# Load the sound files
beep_start = pygame.mixer.Sound('wav/beep1.wav')
beep_stop = pygame.mixer.Sound('wav/beep5.wav')
ambient = pygame.mixer.Sound('wav/ambient1.mp3')

# Play the start beep
beep_start.play()

while True:
    # Set the microphone as the source
    with sr.Microphone() as source:

        print("Say something!")
        # Listen for speech and store it as audio data
        audio = r.listen(source)

    # Use the recognizer to convert speech to text
    try:
        # Recognize the speech input using Google Speech Recognition
        text = r.recognize_google(audio)
        print("You said: " + text)

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

        # Play the ambient sound until the subprocess is called
        ambient.play(-1)

        # Spawn the subprocess and pass the generated_input variable as a command-line argument
        process = subprocess.Popen(['python3', 'oracle.py', generated_input])

    except sr.UnknownValueError:
        print("I couldn't understand you.")

    except sr.RequestError as e:
        print("I can't reach the internet; {0}".format(e))

    except Exception as e:
        print("An error occurred: {0}".format(e))

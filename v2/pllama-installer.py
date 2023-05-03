import nltk
import subprocess


# Install PortAudio using Homebrew
try:
    subprocess.check_call(['python3', 'install', '-r', 'requirements.txt'])
    print("PortAudio has been installed successfully!")
except subprocess.CalledProcessError:
    print("PortAudio installation failed.")

# Download the required resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('brown')


# Install PortAudio using Homebrew
try:
    subprocess.check_call(['brew', 'install', 'portaudio'])
    print("PortAudio has been installed successfully!")
except subprocess.CalledProcessError:
    print("PortAudio installation failed.")


# Install PortAudio using Homebrew
try:
    subprocess.check_call(['brew', 'install', 'espeak'])
    print("PortAudio has been installed successfully!")
except subprocess.CalledProcessError:
    print("espeak installation failed.")

# Install PortAudio using Homebrew
try:
    subprocess.check_call(['brew', 'install', 'ffmpeg'])
    print("PortAudio has been installed successfully!")
except subprocess.CalledProcessError:
    print("espeak installation failed.")

# Verify that the resources have been downloaded successfully
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# # Example usage
# text = "This is an example sentence with some stop words."
# tokens = nltk.word_tokenize(text.lower())
# filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
# freq_dist = FreqDist(filtered_tokens)
# print(freq_dist.most_common())

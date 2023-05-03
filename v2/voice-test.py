import subprocess

# List of phrases to generate MP3s for
phrases = [
    "Hello, world!",
    "How are you today?",
    "I am a computer program.",
    "This is a test.",
    "Espeak is awesome!",
]

# List of en-us voice IDs
voice_ids = [
    "en-us",
    "us-mbrola-1",
    "us-mbrola-2",
    "us-mbrola-3",
]

# Loop through the voice IDs and generate an MP3 for each one
for voice_id in voice_ids:
    # Loop through the phrases and generate an MP3 for each one
    for i, phrase in enumerate(phrases):
        # Generate the MP3 using espeak
        subprocess.call(["espeak", "-w", f"test_{voice_id}_{i}.wav", "-v", f"{voice_id}", phrase])
        # Convert the WAV file to MP3 using ffmpeg
        subprocess.call(["ffmpeg", "-i", f"test_{voice_id}_{i}.wav", f"test_{voice_id}_{i}.mp3"])
        # Delete the temporary WAV file
        subprocess.call(["rm", f"test_{voice_id}_{i}.wav"])

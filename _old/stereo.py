import numpy as np
from pydub import AudioSegment
import sounddevice as sd

def route_sound(filename, device_id, channel):

    # Load audio file using pydub
    sound = AudioSegment.from_file(filename, format="mp3")

    # Convert sound to numpy array
    samples = np.array(sound.get_array_of_samples())

    # Normalize and convert to float32
    samples = samples.astype(np.float32) / (2**15)

    # Play sound on the specified device
    with sd.OutputStream(device=device_id, samplerate=sound.frame_rate, channels=1) as stream:
        stream.write(samples)

if __name__ == "__main__":
    # Test the function
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 0)
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 1)

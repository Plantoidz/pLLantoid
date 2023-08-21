import numpy as np
from pydub import AudioSegment
import sounddevice as sd

def route_sound(filename, device_id, channel):

    # Load audio file using pydub
    sound = AudioSegment.from_file(filename, format="mp3")

    # Convert sound to numpy array and normalize
    samples = np.array(sound.get_array_of_samples()).astype(np.float32) / (2**15)
    
    max_output_channels = sd.query_devices(device_id)['max_output_channels']

    if channel >= max_output_channels:
        raise ValueError(f"The device only has {max_output_channels} output channel(s).")

    # Create an empty array with the correct number of output channels
    zeros = np.zeros((len(samples), max_output_channels), dtype=np.float32)

    # Copy the mono audio data to the desired channel
    zeros[:, channel] = samples

    # Start a stream and play it
    with sd.OutputStream(device=device_id, channels=max_output_channels, samplerate=sound.frame_rate) as stream:
        stream.write(zeros)

if __name__ == "__main__":
    # Test the function
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 0)
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 1)
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 0)

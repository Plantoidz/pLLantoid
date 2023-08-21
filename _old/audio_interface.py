import sounddevice as sd
import numpy as np
from scipy.io import wavfile

def route_sound(filename, device_id, channel):
    # Load the audio file
    fs, data = wavfile.read(filename)
    
    # Ensure audio data is mono
    if len(data.shape) == 2:  # If the audio is stereo
        data = np.mean(data, axis=1)  # We take the average of both channels

    max_output_channels = sd.query_devices(device_id)['max_output_channels']

    if channel >= max_output_channels:
        raise ValueError(f"The device only has {max_output_channels} output channel(s).")

    # Create an empty array with the correct number of output channels
    zeros = np.zeros((len(data), max_output_channels), dtype=np.float32)

    # Convert data to float32
    data = data.astype(np.float32)
    
    # Copy the mono audio data to the desired channel
    zeros[:, channel] = data

    # Start a stream and play it
    with sd.OutputStream(device=device_id, channels=max_output_channels, samplerate=fs) as stream:
        stream.write(zeros)

# Example usage
route_sound('../working/affirmations/0_affirmation.wav', 0, 0)
route_sound('../working/affirmations/0_affirmation.wav', 0, 1)
route_sound('../working/affirmations/0_affirmation.wav', 0, 0)

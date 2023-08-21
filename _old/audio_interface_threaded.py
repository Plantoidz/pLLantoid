import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import threading

class SoundPlayer:
    def __init__(self, filename, device_id, channel):
        self.filename = filename
        self.device_id = device_id
        self.channel = channel
        self.thread = threading.Thread(target=self.play)
        
    def route_sound(self):
        # Load the audio file
        fs, data = wavfile.read(self.filename)

        # Ensure audio data is mono
        if len(data.shape) == 2:  # If the audio is stereo
            data = np.mean(data, axis=1)  # We take the average of both channels

        max_output_channels = sd.query_devices(self.device_id)['max_output_channels']

        if self.channel >= max_output_channels:
            raise ValueError(f"The device only has {max_output_channels} output channel(s).")

        # Create an empty array with the correct number of output channels
        zeros = np.zeros((len(data), max_output_channels), dtype=np.float32)

        # Convert data to float32
        data = data.astype(np.float32)

        # Copy the mono audio data to the desired channel
        zeros[:, self.channel] = data

        # Start a stream and play it
        with sd.OutputStream(device=self.device_id, channels=max_output_channels, samplerate=fs) as stream:
            stream.write(zeros)

    def play(self):
        self.route_sound()

    def start(self):
        self.thread.start()


# Example usage
player1 = SoundPlayer('audio1.wav', 0, 1)
player2 = SoundPlayer('audio2.wav', 1, 0)

player1.start()
player2.start()

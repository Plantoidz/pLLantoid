import numpy as np
from pydub import AudioSegment
import sounddevice as sd

def route_sound(filename, device_id, channel):
    # Load audio file using pydub
    sound = AudioSegment.from_file(filename, format="mp3")

    # Convert sound to numpy array
    samples = np.array(sound.get_array_of_samples())

    if sound.channels == 2:
        # Split stereo audio into left and right channels
        left_channel = samples[::2]
        right_channel = samples[1::2]

        # If channel is 0 (left), mute the right channel; and vice versa
        if channel == 0:
            right_channel = np.zeros_like(right_channel)
        else:
            left_channel = np.zeros_like(left_channel)

        # Interleave left and right channels
        samples = np.column_stack((left_channel, right_channel)).ravel()

    elif sound.channels == 1 and channel == 1:
        # If mono audio and right channel is desired, duplicate the audio for both channels
        samples = np.column_stack((np.zeros_like(samples), samples)).ravel()

    # Normalize and convert to float32
    samples = samples.astype(np.float32) / (2**15)

    # Play sound on the specified device
    with sd.OutputStream(device=device_id, samplerate=sound.frame_rate, channels=sound.channels) as stream:
        stream.write(samples)

if __name__ == "__main__":
    # Test the function
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 0)
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 1)
    route_sound('../working/affirmations/0_affirmation.mp3', 0, 0)

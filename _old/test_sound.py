import sounddevice as sd
import numpy as np

samplerate = 44100  # Hertz
duration = 1.0  # seconds

# Generate a time array
time = np.arange(samplerate * duration) / samplerate

# Generate a 440 Hz sine wave 
frequency = 440  # Hertz
signal = 0.5 * np.sin(2 * np.pi * frequency * time)

# Get device list
devices = sd.query_devices()
# Print all devices
for idx, device in enumerate(devices):
    print(f"Device #{idx}: {device['name']}")

# Ask user for output device
device_id = int(input("Enter the device ID for output: "))

# Map the signal to channel 1 (replace with the channel you want to play the sound on)
mapping = [0] * devices[device_id]['max_output_channels']
mapping[0] = 1  # change 0 to the index of the channel you want to use

# Play the sound
sd.play(signal[:, np.newaxis] * mapping, samplerate, device=device_id)
sd.wait()
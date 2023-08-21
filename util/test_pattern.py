import sounddevice as sd
import numpy as np

def tone(frequency=440, duration=1, samplerate=44100):
    """Generate a simple sinusoidal waveform."""
    t = np.arange(int(samplerate * duration)) / samplerate
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def play_on_channel(channel, channels_total, duration=1, samplerate=44100):
    """Play an ascending tone only on a specific channel."""
    frequency = 440 + channel * 50
    signal = tone(frequency, duration, samplerate)
    
    # Create a silence signal for other channels
    zeros = np.zeros(int(samplerate * duration))
    
    # Create a multi-channel signal with silence on every channel except the target one
    all_channels_signal = [zeros] * channels_total
    all_channels_signal[channel] = signal
    
    sd.play(np.column_stack(all_channels_signal), samplerate)

def main():
    devices = sd.query_devices()
    default_device = sd.default.device

    print("Default Device ID:", default_device)
    print("\nAvailable devices:")
    for idx, device in enumerate(devices):
        print("ID:", idx, "-", device['name'], "with", device['max_output_channels'], "channels")

    device_id = int(input("\nEnter the device ID to test (or press Enter to use the default): ") or default_device)
    device_info = sd.query_devices(device_id)
    channels = device_info['max_output_channels']

    print(f"\nPlaying on device '{device_info['name']}' with {channels} channels...")

    for channel in range(channels):
        print(f"Playing tone on channel {channel + 1}/{channels}...")
        play_on_channel(channel, channels)
        sd.wait()  # Wait until audio playback is done

    print("Test finished!")

if __name__ == "__main__":
    main()

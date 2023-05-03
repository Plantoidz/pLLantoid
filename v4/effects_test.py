import soundfile as sf
import numpy as np
from scipy.signal import lfilter

# Load audio file
audio, sample_rate = sf.read("recordings/1683151234_recording.wav")

# Define reverb parameters
reverb_time = 10 # seconds
decay = 0.1

# Create reverb filter
N = int(reverb_time * sample_rate)
impulse_response = np.zeros(N)
impulse_response[0] = 1.0
filter_coeffs = lfilter([1.0], [1.0, decay], impulse_response)

# Apply reverb effect to audio
reverb_audio = np.convolve(audio, filter_coeffs)

# Write reverb audio to file
sf.write("recordings/1683151234_recording_reverb.wav", reverb_audio, sample_rate)

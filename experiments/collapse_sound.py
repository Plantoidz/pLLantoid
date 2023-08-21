# from pydub import AudioSegment
# from pydub.playback import play
# import numpy as np

# # Load an audio file
# audio = AudioSegment.from_file("working/festival_fear/audio/1692034060_Plantony_response.mp3", format="mp3")

# def apply_fm_modulation(segment, rate=5, depth=50):
#     samples = np.array(segment.get_array_of_samples())
#     t = np.linspace(0, len(samples) / segment.frame_rate, num=len(samples))
#     fm = depth * np.sin(2 * np.pi * rate * t)
#     samples_fm = (samples * np.sin(fm)).astype(np.int16)
#     return segment._spawn(samples_fm.tobytes())

# # Split the audio into three parts
# first_third = len(audio) // 3
# second_third = 2 * len(audio) // 3

# # Apply FM modulation of increasing depth to the middle third
# middle = audio[first_third:second_third]

# depths = np.linspace(0, 500, num=len(middle))
# modulated_audio = AudioSegment.empty()
# for depth, frame in zip(depths, middle):
#     modulated_frame = apply_fm_modulation(frame, rate=5, depth=depth)
#     modulated_audio += modulated_frame

# # Concatenate the audio segments to get the final audio
# final_audio = audio[:first_third] + modulated_audio + audio[second_third:]

# # Play the final audio
# play(final_audio)


# from pydub import AudioSegment
# from pydub.playback import play
# import numpy as np

# # Load an audio file
# audio = AudioSegment.from_file("working/festival_fear/audio/1692036322_SarcasticWitty_response.mp3", format="mp3")

# def apply_fm_modulation(segment, rate=5, depth=50):
#     samples = np.array(segment.get_array_of_samples())
#     t = np.linspace(0, len(samples) / segment.frame_rate, num=len(samples))
#     fm = depth * np.sin(2 * np.pi * rate * t)
#     samples_fm = (samples * np.sin(fm)).astype(np.int16)
#     return segment._spawn(samples_fm.tobytes())

# # Split the audio into 300 parts
# slices_count = 300
# slice_length = len(audio) // slices_count

# modulated_audio = AudioSegment.empty()
# for i in range(slices_count):
#     slice_start = i * slice_length
#     slice_end = (i + 1) * slice_length
#     audio_slice = audio[slice_start:slice_end]
#     depth = i / slices_count * 500  # Adjust the 500 value to taste
#     modulated_slice = apply_fm_modulation(audio_slice, rate=5, depth=depth)
#     modulated_audio += modulated_slice

# # Play the final audio
# play(modulated_audio)


from pydub import AudioSegment
from pydub.playback import play
import numpy as np

# Load an audio file
audio = AudioSegment.from_file("working/festival_fear/audio/1692036322_SarcasticWitty_response.mp3", format="mp3")

def apply_fm_modulation(segment, rate=5, depth=50):
    samples = np.array(segment.get_array_of_samples())
    t = np.linspace(0, len(samples) / segment.frame_rate, num=len(samples))
    fm = depth * np.sin(2 * np.pi * rate * t)
    samples_fm = (samples * np.sin(fm)).astype(np.int16)
    return segment._spawn(samples_fm.tobytes())

# Split the audio into 300 parts
slices_count = 300
slice_length = len(audio) // slices_count

a = 1
b = np.log(500/a) / slices_count  # we're setting it up so at the last step, y ~= 500

modulated_audio = AudioSegment.empty()
for i in range(slices_count):
    slice_start = i * slice_length
    slice_end = (i + 1) * slice_length
    audio_slice = audio[slice_start:slice_end]
    depth = a * np.exp(b * i)
    modulated_slice = apply_fm_modulation(audio_slice, rate=5, depth=depth)
    modulated_audio += modulated_slice

# Play the final audio
play(modulated_audio)

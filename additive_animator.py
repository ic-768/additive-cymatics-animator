import numpy as np
from components import wave_audio, wave_video

directory = "./media"

FPS = 5  # How many sine waves added per second
harmonic_series = "EVEN"  # either "ODD" (square wave) or "EVEN"(saw-tooth)
num_harms = 30  # Includes Fundamental
freq = 50  # Fundamental Frequency

FS = 44100
seconds = 1 / FPS  # Changes length of each individual makeSineSound()
data = np.linspace(0.0, seconds, int(FS * seconds))

wave_video.wave_animation(directory, harmonic_series, num_harms, FPS)
wave_audio.wave_sound(directory, freq, data, harmonic_series, num_harms, FS)
wave_audio.add_audio_to_video(directory)

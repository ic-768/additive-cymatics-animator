import subprocess
import soundfile as sf
import numpy as np
from itertools import zip_longest


def make_sine_sound(linear_number_list, order, freq):  # Data for single sine audio
    """Takes linear data, Nth harmonic order, and base frequency.
    Produces list of sineWave samples for audio"""
    return np.sin(2 * np.pi * order * freq * linear_number_list) / order


def wave_sound(directory, freq, data, harmonic_series, num_harms, FS):
    """Builds audio file and writes to memory when finished"""

    def waveform(
        target_harm, harm_multiplier
    ):  # Returns signal that gradually morphs final form
        output = []
        next_full = (
            []
        )  # 1 segment of full sine waves. e.g. at 8th iter. data will be 8 sine waves simultaneously
        for i in range(target_harm):
            sine = make_sine_sound(  # Make a wave for either odd values of i or all values of i
                data, i * harm_multiplier + 1, freq
            )
            next_full = [
                x + y
                for x, y in zip_longest(
                    next_full, sine, fillvalue=0
                )  # 3rd iter= 1st+2nd+3rd sine
            ]
            output += next_full  # building on output with more sine waves
            i += 1
        return output

    harmonicVec = waveform(num_harms, 2 if harmonic_series == "ODD" else 1)

    sf.write(f"{directory}/waves.wav", harmonicVec, FS)
    print("WRITING AUDIO")


def add_audio_to_video(directory):
    cmd = f"ffmpeg -y -i {directory}/waves.wav -r 30 -i {directory}/waves.mp4 -filter:a aresample=async=1 -c:a libvorbis -c:v copy {directory}/output.mp4"
    subprocess.call(cmd, shell=True)
    print("Muxing Done")

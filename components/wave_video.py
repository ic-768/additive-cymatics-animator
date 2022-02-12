import math
import matplotlib
from matplotlib import animation, rc
import moviepy.editor as mp
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")


def make_sine_animation(
    linear_number_list, order
):  # Data used for video segment of a single sine wave
    """Takes linear list of values, and Nth harmonic order.
    Performs sine transformation on each value of list, to create sample data for Nth harmonic.
    For use in matplotlib video creation
    """
    sin_list = []
    for num in linear_number_list:
        # divide by order so that volume declines steadily with each harmonic. Vital for correct shape of wave
        sin_list.append(math.sin(order * num) / order)
    return sin_list


def wave_animation(directory, harmonic_series, num_harms, FPS):
    """Builds animation of gradual harmonic summation, and writes .gif and .mp4 files to target directory. (Audio is added to mp4 file at a later stage).
    Harmonic series is either "ODD" (square wave) or "BOTH" (sawtooth).
    FPS (frames/second) dictates how many sine waves will be added per second
    """

    def init():
        for each in lines:
            each.set_data([], [])
        line.set_data([], [])
        return lines, line

    def animate(i):
        i %= num_harms
        lines[i].set_data(time, harmonics[i])
        harm_num_text.set_text(f"Harmonics: {i}")
        line.set_data(time, additions[i])
        if i == 0:
            for harmonic in lines:
                harmonic.set_data([], [])
            lines[0].set_data(
                time, harmonics[i]
            )  # Comment this to remove central frequency
        return lines

    animation_speed = 300
    resolution = 0.01
    rc("animation", html="html5")

    x_zoom = 25
    y_zoom = 1.01 if harmonic_series == "ODD" else 2

    time = np.arange(0, x_zoom, resolution)
    fig = plt.figure(figsize=(12, 6))  # Animation details

    ax1 = fig.add_subplot(
        211, xlim=(0, x_zoom), ylim=(-y_zoom, y_zoom), facecolor="black"
    )
    ax2 = fig.add_subplot(
        212, xlim=(0, x_zoom), ylim=(-y_zoom, y_zoom), facecolor="black"
    )

    harmonics = []  # values of harmonic
    additions = []  # sums
    lines = [ax2.plot([], [])[0] for _ in range(num_harms + 1)]

    # Central Frequency (initial render)
    harmonics.append(make_sine_animation(time, 1))
    additions.append(harmonics[0])  # No previous iterations to add to
    (a,) = ax1.plot([], [], lw=2)
    a.set_data(time, harmonics[0])
    lines.append(a)

    for i in range(2, num_harms + 2):
        harmonics.append(
            make_sine_animation(time, i if harmonic_series == "EVEN" else i * 2 - 1)
        )
        additions.append(list(np.array(additions[i - 2] + np.array(harmonics[i - 1]))))

        a.set_data(time, harmonics[i - 1])
        lines.append(a)

    harm_num_text = ax1.text(
        0.0, 1.11, "", transform=ax1.transAxes, fontsize=20
    )  # Text
    (line,) = ax1.plot([], [], lw=2)
    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=num_harms,
        interval=animation_speed,
        blit=False,
        repeat=True,
    )
    print(
        "finished animation, now writing gif and mp4 to media directory. Depending on number of harmonics this might take a while"
    )
    anim.save(f"{directory}/waves.gif", writer="imagemagick", fps=FPS)
    clip = mp.VideoFileClip(f"{directory}/waves.gif")
    clip.write_videofile(f"{directory}/waves.mp4")
    print("finished writing mp4, now producing audio")
    # plt.show(anim)

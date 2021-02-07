import matplotlib
from matplotlib import animation,rc
import moviepy.editor as mp
import matplotlib.pyplot as plt
import numpy as np

directory = "./media"
matplotlib.use("Agg") 

def makeSineAnimation(list, order):     #Data used for video segment of a single sine wave
    sinList = []
    for num in list:
        # divide by order so that volume declines steadily with each harmonic. Vital for correct shape of wave
        sinList.append(np.sin(order * num) / order)
    return sinList


def waveAnimation(harmonicSeries,numHarms,xZoom,yZoom,FPS):
    def init():
        for each in lines:
            each.set_data([], [])
        line.set_data([], [])

        return lines,line
    def animate(i):
        i = i % numHarms
        lines[i].set_data(time,harmonics[i])
        harmNumText.set_text(f"Harmonics: {i}")
        line.set_data(time, additions[i])  # Prints sum
        if i==0:
            for harmonic in lines:
                harmonic.set_data([],[])
            lines[0].set_data(time,harmonics[i]) #Comment this to remove base frequency
        return lines

    animationSpeed = 300
    resolution=0.01
    rc('animation', html='html5')

    time = np.arange(0, xZoom, resolution)
    fig = plt.figure(figsize=(12, 6))  # Animation details


    if harmonicSeries=="ODD":
        yZoom = 1.01

    ax1 = fig.add_subplot(211, xlim=(0, xZoom), ylim=(-yZoom, yZoom),facecolor="black")
    ax2 = fig.add_subplot(212, xlim=(0, xZoom), ylim=(-yZoom, yZoom),facecolor="black")

    harmonics = []  # values of harmonic
    additions = []  # sums
    lines = [ax2.plot([],[])[0] for _ in range(numHarms+1)]

    for i in range(1, numHarms + 2):  # Create fundamental and harmonics
        if i == 1:
            harmonics.append(makeSineAnimation(time, i))
            additions.append(harmonics[0])  # No previous iterations to add to
            a, = ax1.plot([], [], lw=2)
            a.set_data(time, harmonics[0])
            lines.append(a)
        else:
            if harmonicSeries == "ODD":
                harmonics.append(makeSineAnimation(time, i * 2 - 1))
                additions.append(
                        list(np.array(additions[i - 2] + np.array(harmonics[i - 1]))))  # addition[1]=addition[0]+harmonics[1]
            else:
                harmonics.append(makeSineAnimation(time, i))
                additions.append(list(np.array(additions[i - 2] + np.array(harmonics[i - 1]))))
            a.set_data(time, harmonics[i - 1])
            lines.append(a)

    harmNumText = ax1.text(0.0, 1.11, '', transform=ax1.transAxes, fontsize=20)  # Text
    line, = ax1.plot([], [], lw=2)
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=numHarms, interval=animationSpeed, blit=False,repeat= True)
    anim.save(f"{directory}/waves.gif", writer='imagemagick', fps=FPS)
    clip = mp.VideoFileClip(f"{directory}/waves.gif")
    clip.write_videofile(f"{directory}/waves.mp4")
    # plt.show(anim)

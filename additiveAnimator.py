import matplotlib
matplotlib.use("Agg")
import math as m
import subprocess
import numpy as np
import scipy as sp
from enum import Enum
import soundfile as sf
import moviepy.editor as mp
import matplotlib.pyplot as plt
from playsound import playsound
from itertools import zip_longest
from matplotlib import animation,rc
from IPython.display import HTML, Image

directory = '/home/ic768/Desktop/Code/PyStuff/Cymatics/media'

class Parity(Enum):
    EVEN = 2
    ODD = 1
    BOTH = 0
def makeSineAnimation(list, order):     #different for audio and different for video
    sinList = []
    for num in list:
        sinList.append(m.sin(order * num) / order)
    return sinList
def makeSineSound(list,order):
    sinList = []
    for num in list:
        sinList.append(np.sin(order * num*freq*2*np.pi) / order)
    return sinList
def waveAnimation():
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
    global xZoom,yZoom
    animationSpeed = 300
    resolution=0.01
    rc('animation', html='html5')

    time = np.arange(0, xZoom, resolution)
    fig = plt.figure(figsize=(12, 6))  # Animation details

    if harmonicSeries==Parity.ODD:
        yZoom = 1.01
    elif harmonicSeries==Parity.EVEN:
        yZoom =1.2

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
            if harmonicSeries == Parity.ODD:
                harmonics.append(makeSineAnimation(time, i * 2 - 1))
                additions.append(
                    list(np.array(additions[i - 2] + np.array(harmonics[i - 1]))))  # addition[1]=addition[0]+harmonics[1]
            elif harmonicSeries == Parity.EVEN:
                harmonics.append(makeSineAnimation(time, i * 2))
                additions.append(list(np.array(additions[i - 2] + np.array(harmonics[i - 1]))))
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
def waveSound():
    def sawIt(list,targetHarm):     #Return signal that gradually morphs into a sawTooth
        i=1
        output=[] 
        nextFull=[]    #1 second of full sine waves. e.g. 8th iter. = 8 sine waves simultaneously
        while i<targetHarm+1:
            sine=makeSineSound(data,i)
            nextFull=[x + y for x, y in zip_longest(nextFull,sine,fillvalue=0)]    #3rd iter.= 1st+2nd+3rd sine
            output=output+nextFull    #building up output with more added sine waves
            i=i+1    
        return output
    def squareIt(list,targetHarm):    #Return signal that gradually morphs into a square
        i=0
        output=[] 
        nextFull=[]    
        while i<targetHarm:    
            sine=makeSineSound(data,i*2+1)
            nextFull=[x + y for x, y in zip_longest(nextFull,sine,fillvalue=0)]    #3rd iter.= 1st+2nd+3rd sine
            output=output+nextFull    #building up output with more added sine waves
            i=i+1    
        return output
    def evenIt(list,targetHarm):
        i=0
        output=[] 
        nextFull=[]    
        while i<targetHarm:    
            if i==0:
                sine=makeSineSound(data,1)
            else:    
                sine=makeSineSound(data,i*2)
                nextFull=[x + y for x, y in zip_longest(nextFull,sine,fillvalue=0)]    #3rd iter.= 1st+2nd+3rd sine
                output=output+nextFull    #building up output with more added sine waves
            i=i+1    
        return output
    if harmonicSeries==Parity.ODD:
        harmonicVec=squareIt(data,numHarms)
        print('ODD')
    elif harmonicSeries==Parity.BOTH:
        harmonicVec=sawIt(data,numHarms)
        print('BOTH')
    else:
        harmonicVec=evenIt(data,numHarms)

    sf.write(f'{directory}/waves.wav', harmonicVec, FS)
    print('WRITING')
def addAudio2Video():
    cmd = f'ffmpeg -y -i {directory}/waves.wav -r 30 -i {directory}/waves.mp4 -filter:a aresample=async=1 -c:a libvorbis -c:v copy {directory}/output.mp4'
    subprocess.call(cmd, shell=True)                                     # "Muxing Done
    print('Muxing Done')

FPS=1  #How fast to transition
harmonicSeries = Parity.BOTH
numHarms=10  #Includes Fundamental
freq=200   #Fundamental Frequency

FS=44100
amplitude=1.
seconds=1/FPS    #Changes length of each individual makeSineSound()
data=np.linspace(0.,seconds,int(FS*seconds))

xZoom = 25
yZoom = 2.0

waveAnimation()
waveSound()
addAudio2Video()
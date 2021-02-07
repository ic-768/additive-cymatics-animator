import numpy as np

from components import waveAudio
from components import waveVideo

directory = "./media"

# list of linear nums is transformed with sine function to fluctuate between 1 and -1. 
# order refers to Nth harmonic

FPS=3  #How fast to transition
harmonicSeries = "ODD"
numHarms=20  #Includes Fundamental
freq=150   #Fundamental Frequency

FS=44100
amplitude=1.
seconds=1/FPS    #Changes length of each individual makeSineSound()
data=np.linspace(0.,seconds,int(FS*seconds))

xZoom = 25
yZoom = 2.0

waveVideo.waveAnimation(harmonicSeries,numHarms,xZoom,yZoom,FPS) #TODO how to skip making different waves for audio and video and just pass data from one to the other?
waveAudio.waveSound(freq,data,numHarms,harmonicSeries,FS)
waveAudio.addAudio2Video()

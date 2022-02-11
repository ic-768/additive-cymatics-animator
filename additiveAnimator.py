import numpy as np
from components import waveAudio, waveVideo

directory = "./media"

FPS=3  #How many sine waves added per second
harmonicSeries = "ODD" #either "ODD" (square wave) or "EVEN"(saw-tooth)
numHarms=30  #Includes Fundamental
freq=50   #Fundamental Frequency

FS=44100
seconds=1/FPS    #Changes length of each individual makeSineSound()
data=np.linspace(0.,seconds,int(FS*seconds))

xZoom = 25
yZoom = 2.0

waveVideo.waveAnimation(directory,harmonicSeries,numHarms,FPS) 
waveAudio.waveSound(directory,freq,data,harmonicSeries,numHarms,FS)
waveAudio.addAudio2Video(directory)

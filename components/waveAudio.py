import soundfile as sf
import subprocess
import numpy as np
from itertools import zip_longest

directory = "./media"

def makeSineSound(list,order,freq):  #Data for single sine audio
    '''Takes linear data, Nth harmonic order, and base frequency. 
    Produces list of sineWave samples for audio'''
    sinList = []
    for num in list:
        sinList.append(np.sin(order * num*freq*2*np.pi) / order)
        # audio needs 2*freq*pi to be correct. This breaks video
    return sinList

def waveSound(freq,data,harmonicSeries,numHarms,FS): 
    '''Builds audio file and writes to memory when finished''' 
    def waveform(list,targetHarm,harmMultiplier): #Returns signal that gradually morphs final form
        i=0
        output=[] 
        nextFull=[]    #1 segment of full sine waves. e.g. at 8th iter. data will be 8 sine waves simultaneously
        while i<targetHarm:
            sine=makeSineSound(data,i*harmMultiplier+1,freq) # Make a wave for either odd values of i or all values of i
            nextFull=[x + y for x, y in zip_longest(nextFull,sine,fillvalue=0)]    #3rd iter.= 1st+2nd+3rd sine
            output=output+nextFull    #building on output with more sine waves
            i=i+1    
        return output 

    if harmonicSeries=="ODD":
        harmonicVec=waveform(data,numHarms,2) #i takes odd values of 1,3,5
    else:
        harmonicVec=waveform(data,numHarms,1) #i takes all values

    sf.write(f'{directory}/waves.wav', harmonicVec, FS)
    print('WRITING AUDIO')

def addAudio2Video():
    cmd = f'ffmpeg -y -i {directory}/waves.wav -r 30 -i {directory}/waves.mp4 -filter:a aresample=async=1 -c:a libvorbis -c:v copy {directory}/output.mp4'
    subprocess.call(cmd, shell=True)                         
    print('Muxing Done')

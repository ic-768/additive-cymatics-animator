import soundfile as sf
import subprocess
import math
from itertools import zip_longest


def makeSineSound(list,order,freq):  #Data for single sine audio
    '''Takes linear data, Nth harmonic order, and base frequency. 
    Produces list of sineWave samples for audio'''
    sinList = []
    for num in list:
        sinList.append(math.sin(order * num*freq*2*math.pi) / order)
        # audio needs 2*freq*pi to be correct. This breaks video
    return sinList

def waveSound(directory,freq,data,harmonicSeries,numHarms,FS): 
    '''Builds audio file and writes to memory when finished''' 
    def waveform(targetHarm,harmMultiplier): #Returns signal that gradually morphs final form
        i=0
        output=[] 
        nextFull=[]    #1 segment of full sine waves. e.g. at 8th iter. data will be 8 sine waves simultaneously
        while i<targetHarm:
            sine=makeSineSound(data,i*harmMultiplier+1,freq) # Make a wave for either odd values of i or all values of i
            nextFull=[x + y for x, y in zip_longest(nextFull,sine,fillvalue=0)]    #3rd iter.= 1st+2nd+3rd sine
            output+=nextFull    #building on output with more sine waves
            i+=1    
        return output 

    harmonicVec=waveform(numHarms,2 if harmonicSeries=="ODD" else 1) #i takes odd values of 1,3,5

    sf.write(f'{directory}/waves.wav', harmonicVec, FS)
    print('WRITING AUDIO')

def addAudio2Video(directory):
    cmd = f'ffmpeg -y -i {directory}/waves.wav -r 30 -i {directory}/waves.mp4 -filter:a aresample=async=1 -c:a libvorbis -c:v copy {directory}/output.mp4'
    subprocess.call(cmd, shell=True)                         
    print('Muxing Done')

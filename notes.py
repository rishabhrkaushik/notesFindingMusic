import scipy.io.wavfile as wavfile
import numpy as np
import wave
import struct
from scipy.fftpack import fft 

#open file
wave_read= wave.open("audioFiles/Audio_1.wav",'r')

#number of readings in file
file_length = wave_read.getnframes()

#sampling frequency
fs = 44100

#dividing complete sound into windows
frames_per_window = int(fs*0.05)
no_of_windows = int(np.ceil(file_length/frames_per_window))

print "Read Sound\n", "Number of frames: ", file_length, "\nFrames per window: ", frames_per_window, "\nNumber of windows: ", no_of_windows
import scipy.io.wavfile as wavfile
import numpy as np
import wave
import struct
from scipy.fftpack import fft 

#open file
wave_read= wave.open("audioFiles/Audio_1.wav",'r')

#number of frames in file
file_length = wave_read.getnframes()

#sampling frequency
fs = 44100

#dividing complete sound into windows
frames_per_window = int(fs*0.05)
no_of_windows = int(np.ceil(file_length/frames_per_window))

print "Read Sound\n", "Number of frames: ", file_length, "\nFrames per window: ", frames_per_window, "\nNumber of windows: ", no_of_windows

#read sound
sound=np.zeros(file_length)
for i in range(file_length):
	data = wave_read.readframes(1)
	data = struct.unpack("<h", data)
	sound[i]=int(data[0])

#normalize the amplitude from 16 bit to range -1 to 1
sound = np.divide(sound,float(2**15))

#distribute unpacked sound in windows
windows = []

for i in range(0, no_of_windows):
	this_window = np.zeros(frames_per_window)
	for j in range(0, frames_per_window):
		this_window[j] = sound[(i * frames_per_window) + j]
	windows.append(this_window)

#calculate rms of amplitude
Arms = []

for window in range(0, no_of_windows):
	rms = 0
	for frame in windows[window]:
		rms = rms + frame**2
	rms = np.sqrt(rms/frames_per_window)
	if rms < 0.6:
		rms = 0
	Arms.append(rms)
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
	if rms < 0.7:
		rms = 0
	Arms.append(rms)

#reference http://www.liutaiomottola.com/formulae/freqtab.htm
notesDict = {
	"C":  [16.351, 32.703, 65.406, 130.813, 261.626, 523.251, 1046.502, 2093, 4186, 8372],
	"C#": [17.324, 34.648, 69.296, 138.591, 277.183, 554.365, 1108.731, 2217, 4434, 8869],
	"D":  [18.354, 36.708, 73.416, 146.832, 293.665, 587.330, 1174.659, 2349, 4698, 9397],
	"D#": [19.445, 38.891, 77.782, 155.563, 311.127, 622.254, 1244.508, 2489, 4978, 9956],
	"E":  [20.601, 41.203, 82.407, 164.814, 329.628, 659.255, 1318.510, 2637, 5274, 10548],
	"F":  [21.827, 43.654, 87.307, 174.614, 349.228, 698.456, 1396.913, 2793, 5587, 11175],
	"F#": [23.124, 46.249, 92.499, 184.997, 369.994, 739.989, 1479.978, 2959, 5919, 11839],
	"G":  [24.499, 48.999, 097.999, 195.998, 391.995, 783.991, 1567.982, 3135, 6271, 12543],
	"G#": [25.956, 51.913, 103.826, 207.652, 415.305, 830.609, 1661.219, 3322, 6644, 13289],
	"A":  [27.500, 55.000, 110.000, 220.000, 440.000, 880.000, 1769.000, 3520, 7040, 14080],
	"A#": [29.135, 58.270, 116.541, 233.082, 466.164, 932.328, 1864.655, 3729, 7458, 14917],
	"B":  [30.868, 61.735, 123.471, 246.942, 493.883, 987.767, 1975.533, 3951, 7902, 15804]
}
#join consequtive windows if Arms != 0 toghether to form a note 
notes = []
this_note = []
for i in range(0, no_of_windows):
	if Arms[i] == 0:
		if len(this_note) != 0:
			notes.append(this_note)
			this_note = []
	if Arms[i] != 0:
		for frame in windows[i]:
			this_note.append(frame)

#calculate frequency of notes````````
notesFound = []
for note in notes:
	# print "New", len(note)
	fft_note = np.zeros(len(note))
	fft_magnitude = np.zeros(len(note))
	fft_note = fft(note)
	for i in range(0, len(note)):
		fft_magnitude[i] = np.absolute(fft_note[i])

	maximum_fft = np.amax(fft_magnitude)
	# print "Max_fft", maximum_fft

	
	for i in range(0, len(note)):
		found = False
		if fft_magnitude[i] == maximum_fft:
			frequency = i*44100/len(note)
			for key in notesDict:
				for value in notesDict[key]:
					if value - 2 < frequency < value + 2:
						notesFound.append(key)
						found = True
						break
				if(found):
					break

print notesFound
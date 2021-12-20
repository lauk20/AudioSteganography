import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile

Fs, aud = wavfile.read('xxx.wav')
aud = aud[:,0]

powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(aud, Fs=Fs)
plt.xlabel("bruh")
plt.ylabel("bruh.2")
plt.show()

from PIL import Image, ImageOps
import wave, struct, math, random
import array
from scipy.io import wavfile
import numpy as np

def main():
    sampleRate = 44100; #sampling rate
    audioLength = 60 * 2; #seconds
    totalSamples = sampleRate * audioLength;

    image = Image.open('lambo.jpg');
    pixels = image.load();
    width, height = image.size;

    print(width, height);

    audio = wave.open("spectro.wav", "w");
    audio.setnchannels(1);
    audio.setsampwidth(2); #2 bytes, 16 bit-depth
    audio.setframerate(sampleRate);

    maxFreq = 17000;
    minFreq = 7000;
    freqRange = maxFreq - minFreq;
    samplesPerXPixel = math.floor(totalSamples / width);

    allsamples = []
    #np.append(allsamples, 0);
    for x in range(width):
        #print(x);
        for y in range(height):
            r, g, b = image.getpixel((x,y));
            amplitude = (r + g + b)/3;
            frequency = maxFreq - (freqRange / (y + 1));
            values = np.linspace(0, samplesPerXPixel, sampleRate);
            result = np.sin(frequency * 2 * np.pi * values);
            #allsamples.append(result)
        #print(result);
        audio.writeframes(result);

    #wavfile.write('Spectro.wav', sampleRate, allsamples);

    #print(counter);
    print("DONE");
    audio.close();
main();

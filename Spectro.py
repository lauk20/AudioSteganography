from PIL import Image, ImageOps
import wave, struct, math, random
import array
from scipy.io import wavfile
import numpy as np

def newMain():
    sampleRate = 44100;
    audioLength = 15; #seconds
    totalSamples = sampleRate * audioLength;

    image = Image.open("lambo.jpg").convert("L");
    pixels = image.load();
    width, height = image.size;

    audio = wave.open("newSpectro.wav", "w");
    audio.setnchannels(1);
    audio.setsampwidth(2); #2 bytes, 16 bit-depth
    audio.setframerate(sampleRate);

    maxFreq = 17000;
    minFreq = 7000;
    freqRange = maxFreq - minFreq;
    samplesPerColumn = math.floor(totalSamples / width);
    samplesPerPixel = math.floor(samplesPerColumn / height);

    result = array.array('h');
    print(samplesPerColumn);
    print(samplesPerPixel);

    for x in range(width):
        print(x);
        for y in range(height):
            temp = [];
            intensity = image.getpixel((x,y));
            #print(intensity, frequency, freqRange);
            for i in range(samplesPerPixel):
                #print(i);
                sample = intensity * math.sin(((freqRange/height) * (height - y) + minFreq) * 2 * math.pi * i);
                result.append(int(math.floor(sample)));
                #print(int(math.floor(sample)));
            #result.append(temp);
    audio.writeframes(result);


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
    samples = np.array((0))
    finalsamples = np.array((0));
    newresult = 0;
    for x in range(width):
        print(x);
        #array = np.array();
        result = 0;
        for y in range(height):
            r, g, b = image.getpixel((x,y));
            amplitude = (r + g + b)/3;
            frequency = maxFreq - (freqRange / (y + 1));
            values = np.linspace(0, audioLength // width // height, sampleRate * (audioLength // width // height));
            result = np.sin(frequency * 2 * np.pi * values);
            #samples = np.append(samples, result);
            newresult = np.append(samples, result);
            samples = newresult;
            #array.append(result);
            #allsamples.append(result)
        wavfile.write('stest.wav', 44100, samples);
        continue; #here temporarily
        print("wrote something to file");
        #print(result);
        #audio.writeframes(array);

    wavfile.write("stest.wav", 44100, samples);

    #wavfile.write('Spectro.wav', sampleRate, allsamples);

    #print(counter);
    print("DONE");
    audio.close();
newMain();

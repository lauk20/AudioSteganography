from PIL import Image, ImageOps
import wave, struct, math, random
import array
from scipy.io import wavfile
import numpy as np

def method2():
    sampleRate = 44100; #audio sampling rate
    audioLength = 5; #seconds
    totalSamples = sampleRate * audioLength; #total samples in audio

    image = Image.open("lambo.jpg").convert("L"); #open image and convert to grayscale image
    pixels = image.load(); #load the pixels into an array
    width, height = image.size; #dimensions of the image

    maxFreq = 17000; #high end of human hearing frequency at 20kHz
    minFreq = 200; #low end of human hearing frequency at 20Hz
    freqRange = maxFreq - minFreq; #frequency range we are writing to
    samplesPerColumn = totalSamples // width; #how many samples each column in the image will need to meet the audio length;

    superimposed = [];
    for row in range(height):
        samples = np.linspace(0, audioLength, totalSamples);
        intensityArray = [];
        lastIntensity = 0;
        frequency = (freqRange / height) * (height - row) + minFreq;
        #print(frequency);
        for col in range(width):
            intensity = image.getpixel((col, row));
            for i in range(samplesPerColumn):
                intensityArray.append(intensity);
                lastIntensity = intensity;

        result = np.sin(frequency * 2 * np.pi * samples);
        while (len(intensityArray) < len(result)):
            intensityArray.append(lastIntensity);
        toWrite = result * intensityArray;

        if (len(superimposed) == 0):
            superimposed = toWrite;
        else:
            superimposed = superimposed + toWrite;

    for i in range(len(superimposed)):
        if superimposed[i] > 32767:
            superimposed[i] = 32767;
        elif superimposed[i] < -32768:
            superimposed[i] = -32768;
    superimposed = np.int16(superimposed);
    wavfile.write("testingmethod2.wav", sampleRate, superimposed);

def newMain():
    sampleRate = 44100; #audio sampling rate
    audioLength = 5; #seconds
    totalSamples = sampleRate * audioLength; #total samples in audio

    image = Image.open("lambo.jpg").convert("L"); #open image and convert to grayscale image
    pixels = image.load(); #load the pixels into an array
    width, height = image.size; #dimensions of the image

    audio = wave.open("newSpectro.wav", "w"); #open audio file we're writing to
    audio.setnchannels(1); #set number of channels (mono)
    audio.setsampwidth(2); #2 bytes, 16 bit-depth
    audio.setframerate(sampleRate); #set sampling rate

    maxFreq = 17000; #high end of human hearing frequency at 20kHz
    minFreq = 200; #low end of human hearing frequency at 20Hz
    freqRange = maxFreq - minFreq; #frequency range we are writing to
    samplesPerColumn = totalSamples // width; #how many samples each column in the image will need to meet the audio length;

    for sample in range(totalSamples):
        #print(sample);
        superimposed = 0;
        for row in range(height):
            col = sample // samplesPerColumn;
            if (col >= width):
                continue
            intensity = image.getpixel((col, row))
            #print(intensity)
            frequency = (freqRange / height) * (height - row) + minFreq;
            #print(frequency);

            #print(math.sin(frequency * 2 * math.pi * sample / sampleRate), frequency * 2 * math.pi * sample / sampleRate, frequency / sampleRate * 2 * math.pi * sample, frequency / sampleRate);
            superimposed = superimposed + intensity * math.sin(frequency * 2 * math.pi * sample / sampleRate);

        superimposedbytelike = array.array('h'); #'h' indicates signed short (2 bytes), which is what we need since bit-depth is 16 bits
        if (superimposed > 32767):
            superimposed = 32767; #max for signed short
        elif (superimposed < -32768):
            superimposed = -32767; #min for signed short
        superimposedbytelike.append(int(superimposed));
        audio.writeframes(superimposedbytelike); #we needed the array.array() since writeframes() only takes in a byte-like object

    audio.close();

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
#newMain();
method2();

from PIL import Image, ImageOps
import wave, struct, math, random
import array
from scipy.io import wavfile
import numpy as np

def newMain():
    sampleRate = 44100;
    audioLength = 5; #seconds
    totalSamples = sampleRate * audioLength;

    image = Image.open("lambo.jpg").convert("L");
    pixels = image.load();
    width, height = image.size;

    audio = wave.open("newSpectro.wav", "w");
    audio.setnchannels(1);
    audio.setsampwidth(2); #2 bytes, 16 bit-depth
    audio.setframerate(sampleRate);

    maxFreq = 17000;
    minFreq = 200;
    freqRange = maxFreq - minFreq;
    samplesPerColumn = math.floor(totalSamples / width);
    freqPerPixel = math.floor(freqRange / height);

    result = array.array('h');
    print(samplesPerColumn);
    print(freqPerPixel);

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

            superimposed = superimposed + intensity * math.sin(frequency * 2 * math.pi * sample / sampleRate);

        superimposedbytelike = array.array('h');
        if (superimposed > 32767):
            superimposed = 32767;
        elif (superimposed < -32768):
            superimposed = -32767;
        superimposedbytelike.append(int(superimposed));
        audio.writeframes(superimposedbytelike);

    audio.close();

    """
    for x in range(width):
        print(x);
        sample = 0;
        for y in range(height):
            #sample = 0;
            intensity = image.getpixel((x,y));
            #print(intensity);
            #print(intensity, frequency, freqRange);
            for i in range(0, freqPerPixel):
                #print(i);
                sample = sample + intensity * math.sin(x * 2 * math.pi * i/sampleRate);
                #print(intensity * math.sin(x * 2 * math.pi * i/sampleRate));
                #result.append(int(math.floor(sample)));
                #print(int(math.floor(sample)));
                #print(sample);
                if (sample > 32767 or sample < -32767):
                    sample = 32767;
                    samples = struct.pack("<h", int(sample));
                    audio.writeframesraw(samples);
                    sample = 0;
            #result.append(temp);
        #print(sample);
        samples = struct.pack("<h", int(sample));
        audio.writeframesraw(samples);

    #audio.writeframes(result);
    """

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

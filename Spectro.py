from PIL import Image, ImageOps
from scipy.io import wavfile
import math
import numpy as np
import sys

#this function converts an image into audio.
#in-depth and detailed explanation is present in the Google Doc listed in the README
#General Algorithm/Concept:
"""
DETAILED EXPLANATION OF HOW THIS WORKS IS IN THE README GOOGLE DOCS LINK!!
(but here's the general concept):

Every row on the image represents a frequency in the spectrogram.
The brightness of a pixel represents the brightness on the spectrogram.
We create a set of points that represents a sine wave of a specific frequency
that represents a row on the image
(and thus a specific frequency on the spectrogram),
with each point having its own amplitude,
then we smash the sine waves of each row together to form a superimposed wave.
Because a fourier transform can break the complex wave back into its individual
frequencies, the spectrogram can show us the frequencies we created and the
brightness of the pixels used (amplitude of the wave).
"""
def convert():
    sampleRate = 44100; #audio sampling rate
    audioLength = 5; #seconds
    totalSamples = sampleRate * audioLength; #total samples in audio

    if(sys.argv[2] != None):
        image = Image.open(sys.argv[2]).convert("L"); #open image and convert to grayscale image
    else:
         image = Image.open("lambo.jpg").convert("L"); #open image and convert to grayscale image
    pixels = image.load(); #load the pixels into an array
    width, height = image.size; #dimensions of the image

    maxFreq = 17000; #high end of human hearing frequency at 20kHz
    minFreq = 200; #low end of human hearing frequency at 20Hz
    freqRange = maxFreq - minFreq; #frequency range we are writing to
    samplesPerColumn = totalSamples // width; #how many samples each column in the image will need to meet the audio length;

    superimposed = []; #this will be the final complex sound wave
    for row in range(height): #we are looping through the image row by row
        samples = np.linspace(0, audioLength, totalSamples); #this creates an np array of [totalSamples] elements
        intensityArray = []; #this is the array that will hold amplitude values
        lastIntensity = 0; #this is the last intensity/amplitude value that was written
        frequency = (freqRange / height) * (height - row) + minFreq; #the frequency that we are writing to. scaled by the range and added to the min. higher frequency = higher row of image
        #print(frequency);
        for col in range(width): #loop through each column of the row in the image
            intensity = image.getpixel((col, row)); #get the color intensity/"brightness" of the image
            for i in range(samplesPerColumn): #we need to repeat this [samplesPerColumn] number of times in order to meet the audioLength and correct number of samples once we are done
                intensityArray.append(intensity); #append the intensity to intensity array
                lastIntensity = intensity; #assign lastIntensity to the appended intensity

        result = np.sin(frequency * 2 * np.pi * samples); #here are a finding the values for the samples in order to get a sine curve of the correct frequency. the return will be a np array.
        while (len(intensityArray) < len(result)): #sometimes the intensity array isn't long enough to use np.multiply, so we append the last intensity to it.
            intensityArray.append(lastIntensity);
        toWrite = result * intensityArray; #we multiply the intensity array with the array with sample values that form a sine curve. (amplitude * sine value)

        if (len(superimposed) == 0): #adding to the resulting complex wave, if it has no elements yet, we assign it to the current wave we have
            superimposed = toWrite;
        else: #if there are elements, we add the array together (think of it as superimposing the wave/smashing two waves together to form a complex wave).
            superimposed = superimposed + toWrite;

    for i in range(len(superimposed)): #16-bit depth audio, values should be limited.
        if superimposed[i] > 32767:
            superimposed[i] = 32767;
        elif superimposed[i] < -32768:
            superimposed[i] = -32768;
    superimposed = np.int16(superimposed);
    wavfile.write("image.wav", sampleRate, superimposed); #write to the audio file

convert();

"""
Code above is current functioning code/method used to convert
Code below was code used when trying to figure out/learn/experiment
"""


"""
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
"""

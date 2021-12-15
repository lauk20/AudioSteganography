from PIL import Image, ImageOps
import wave, struct, math, random

def main():
    sampleRate = 44100; #sampling rate
    audioLength = 60 * 2; #seconds
    totalSamples = sampleRate * audioLength;

    image = ImageOps.grayscale(Image.open('lambo.jpg'));
    pixels = image.load();
    width, height = image.size;

    print(width, height);

    audio = wave.open("spectro.wav", "w");
    audio.setnchannels(1);
    audio.setsampwidth(2); #2 bytes, 16 bit-depth
    audio.setframerate(sampleRate);

    pixelWidth = totalSamples // width;
    maxFreq = 17000;
    minFreq = 7000;
    freqRange = maxFreq - minFreq;

    counter = 0;

    for x in range(width):
        volume = 0;
        for p in range(pixelWidth):
            for y in range(height):
                intensity = image.getpixel((x, y));
                #print(intensity);
                frequency = maxFreq - y;

                volume = math.floor(freqRange * math.sin(intensity * math.pi * frequency / sampleRate));
                #print(volume);
                counter = counter + 1;

        data = struct.pack('<h', volume); # < is little endian and h is 2 bytes
        audio.writeframesraw(data);
    print(counter);

main();

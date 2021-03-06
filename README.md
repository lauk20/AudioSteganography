# AudioSteganography

**Team Name:** Konstant Koders

**Team Members:** Kenny Lau, David Chong

**Project Description:** Audio Steganography (Main techniques: LSB Encoding and Image to Audio).

**Project Write-Up:** https://docs.google.com/document/d/1MVSCTSzuoAy4WSOHk-gu4xDhxMN5YxmC2fnSQmBmudE/edit?usp=sharing (Must use .edu address)

**Project Slides:** https://docs.google.com/presentation/d/1BeWU55k3sHakokKTNy1mZbwtRkcCIMDxmrGGU48ltVA/edit?usp=sharing (Must use .edu address)

## Files
1. main.c : The C code that does LSB encoding/decoding.
2. Spectro.py : The Python code that writes an image into wav file.
3. alternate.c : The C code that appends a wav chunk that contains a raw message. (This was something extra we did).
4. furelise.wav : Fur Elise by Beethoven audio in wav format.
5.

## Dependencies Instructions
1. To compile the C programs run ```make```.
2. Install, if you don't already have, PIL for Python (pip install Pillow). More installation support here: https://pillow.readthedocs.io/en/stable/installation.html
3. Install, if you don't already have, scipy.io for Python (pip install scipy). More installation support here: https://scipy.org/install/
4. Install, if you don't already have, numpy for Python (pip install np). More installation support here: https://numpy.org/install/.
5. It is recommended you install Audacity to have the full experience: https://manual.audacityteam.org/index.html
6. We are assuming you have the math library in Python and can run ```import math```.

NOTE: THESE INSTALLATIONS WORKED FOR US BUT IT WAS NEVER EXTENSIVELY TESTED. They seem to be already installed on the cs-lab machines though.

## Run Instructions
If you want Least Significant Bit encoding: (Refer to limitations section too)
1. Encoding a message: "./main encode lsb [AudioFileName.wav] [OPTIONAL: message (will read from stdin if not given)]"
2. Decoding a message "./main decode lsb [AudioFileName.wav]"

To convert image to audio:
1. python3 Spectro.py [ImageFileNameHere.png]
2. "python3 Spectro.py" will use the image in the repo: lambo.jpg

To view converted image:
1. Audacity is recommended, use the spectrogram viewer in the program. Support: https://manual.audacityteam.org/man/spectrogram_view.html
2. Any spectrogram viewer that works as well as Audacity (a good audio editing software).

Tips: Using linear for Scale and greyscale for Scheme spectrogram settings seems to produce a nice looking image!

If you want to append a raw message chunk directly to the wav file (this is something extra we did):
1. "./alternate [encode/decode] [filename] [OPTIONAL for decode: message]"

## Limitations
1. The limit for the size of Least Significant Bit encoding is 1000 bytes. It is a hard-coded limit. It is currently built for text-based encoding (it reads for a null byte (00000000) and stops reading once it finds it)
2. There is currently a hard-coded audio duration of 5 seconds, max frequency of 17 kHz, min frequency of 200 Hz, for the image to audio converter.

## Development Log

### 1/2/22
**David Chong** Worked on revising slides, added introduction, edited readme
### 1/1/22

**Kenny Lau:** Worked on math explanation for slides and updated README documentation
### 12/29/21

**David Chong** Added Command line input for the spectrogram image, allowed for base image to be used as well as an image that the user can choose.  Have not tested for images other than jgps I think.

### 12/28/21
**Kenny Lau:** Finished up image to audio section of write-up (may need some editing later). Worked on documentation for README.

### 12/27/21
**Kenny Lau:** Added comments to code and made formatting better. Started the image to spectrogram section of write-up.

### 12/26/21
**Kenny Lau:** Worked on write-up/explanation of concepts (LSB explanation).

### 12/23/21
**Kenny Lau:** Worked on presentation/slides.

**David Chong** Worked on presentation/slides.

### 12/22/21
**Kenny Lau:** Worked on the method where WAV chunks are added at the end of an audio file. (Raw message added to end of file but enclosed in WAV chunk so that it does not break audio playing programs).

**David Chong** Worked with Kenny on completing the file

### 12/21/21
**Kenny Lau:** Worked on write-up and presentation. Tested the programs we have made so far.

**David Chong** Created file for alternate encoding portion of sound file.  Very basic, adds plaintext to the end of the wav file.

### 12/20/21
**Kenny Lau:** Worked detailed write-up on project to explain what we learned while working on this project. Started on slides for presentation.

**David Chong** Started on slides for presentation.

### 12/19/21
**Kenny Lau:** Fixed LSB encoding. Before it was altering the LSB of every byte in the file. However, since we are using 16-bit audio files, this meant that not every LSB is truly insignificant. So, made it so that it only altered the LSB of the 2 bytes (i.e. the LSB of the 1st byte in the 2 byte series).

### 12/17/21
**Kenny Lau:** Finally got image to spectrogram program working. Needs to improve/learn how to take in command line arguments for Python. (Used Audacity to view the spectrogram created from image).

**David Chong** Researched matplotlib's documentation for ways to make image shown more presentable


### 12/16/21
**Kenny Lau:** Continued working on the image to spectrogram program. Started write-up for project. Getting closer with image to spectrogram, but still does not work properly.

**David Chong:** Created basic spectrogram using numpy, matplotlib, and scipy.  Still need to work on creating a better looking graph with more discernable features.

### 12/15/21
**Kenny Lau:** Learned/explored necessary Python libraries in order to convert image to audio (PIL/Pillow and scipy). Tried to make the program (Spectro.py) that converts an image into an audio file. Better understanding of how the program is *supposed* to work. It seems to crash now because the list holding the samples is huge. Need to find a better method of appending samples to a WAV file (maybe one that doesn't store a lot of samples in memory).

### 12/14/21
**Kenny Lau:** Did research on how to write WAV files from a given frequency and volume (etc.) (Need to download something for Java, maybe need to look into another language.) Started working on image to spectrogram program in Python. Needed to learn how to handle/write WAV files in Python along with how to process images in Python. Spent ~1 hr on image to spectrogram with little success towards the end goal.

**David Chong:** Filled out Google forms and worked on creating slides to present project.  Researching how spectrogramming would work in Python, and other languages where it would be possible, little success so far.

### Before 12/14/21 (before logging)
We completed our base code for least significant bit encoding and decoding and learned/researched how WAV files are structured/work (researched).

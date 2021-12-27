# AudioSteganography

**Team Name:** Konstant Koders

**Team Members:** Kenny Lau, David Chong

**Project Description:** Audio Steganography (Main techniques: LSB Encoding and Image to Audio).

## Run Instructions
1. To compile the C programs run ```make```.
2. 


## Development Log
### 12/27/21
**Kenny Lau:** Added comments to code and made formatting better.

### 12/26/21
**Kenny Lau:** Worked on write-up/explanation of concepts.

### 12/23/21
**Kenny Lau:** Worked on presentation/slides.

### 12/22/21
**Kenny Lau:** Worked on the method where WAV chunks are added at the end of an audio file. (Raw message added to end of file but enclosed in WAV chunk so that it does not break audio playing programs).

### 12/21/21
**Kenny Lau:** Worked on write-up and presentation. Tested the programs we have made so far.

### 12/20/21
**Kenny Lau:** Worked detailed write-up on project to explain what we learned while working on this project. Started on slides for presentation.

### 12/19/21
**Kenny Lau:** Fixed LSB encoding. Before it was altering the LSB of every byte in the file. However, since we are using 16-bit audio files, this meant that not every LSB is truly insignificant. So, made it so that it only altered the LSB of the 2 bytes (i.e. the LSB of the 1st byte in the 2 byte series).

### 12/17/21
**Kenny Lau:** Finally got image to spectrogram program working. Needs to improve/learn how to take in command line arguments for Python. (Used Audacity to view the spectrogram created from image).

### 12/16/21
**Kenny Lau:** Continued working on the image to spectrogram program. Started write-up for project. Getting closer with image to spectrogram, but still does not work properly.

**David Chong:** Created basic spectrogram using numpy, matplotlib, and scipy.  Still need to work on creating a better looking graph with more discernable features.

### 12/15/21
**Kenny Lau:** Learned/explored necessary Python libraries in order to convert image to audio (PIL/Pillow and scipy). Tried to make the program (Spectro.py) that converts an image into an audio file. Better understanding of how the program is *supposed* to work. It seems to crash now because the list holding the samples is huge. Need to find a better method of appending samples to a WAV file (maybe one that doesn't store a lot of samples in memory).

### 12/14/21
**Kenny Lau:** Did research on how to write WAV files from a given frequency and volume (etc.) (Need to download something for Java, maybe need to look into another language.) Started working on image to spectrogram program in Python. Needed to learn how to handle/write WAV files in Python along with how to process images in Python. Spent ~1 hr on image to spectrogram with little success towards the end goal.

**David Chong:** Filled out Google forms and worked on creating slides to present project.  Researching how spectrogramming would work in Python, and other languages where it would be possible, little success so far.

## Before 12/14/21 (before logging)
We completed our base code for least significant bit encoding and decoding and learned/researched how WAV files are structured/work (researched).

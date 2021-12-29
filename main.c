#include <stdio.h>

#include <stdlib.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

void decode(char * filename) {
  int fd = open(filename, O_RDONLY, 0644);
  char riff_header[36];
  read(fd, riff_header, 36);

  int found_data = 1; // 0 means "data" chunk has been found.
  int datachunk_size = 0;
  while (found_data) {
    char chunk_descriptor[5];
    read(fd, chunk_descriptor, 4);

    if (strcmp(chunk_descriptor, "data") == 0) {
      found_data = 0;
      int data_size;
      read(fd, & data_size, 4);
      //printf("Data_Size: %d\n", data_size);
      datachunk_size = data_size;
    } else {
      int size;
      read(fd, & size, 4); //gets subchunk size

      char * ignored_chunk_data = calloc(size, 1);
      read(fd, ignored_chunk_data, size); //ignores the unecessary chunk (skips it);
    }
  }

  char * message = calloc(datachunk_size / 8, 1);
  int i;
  int bytesread = 0;
  int skip = 0;
  int bit = 0;
  int nextbyte = 0;
  int consecutive_zero_bit_count = 0; //if it reaches 8 then null byte, so can stop
  char currentbyte = * (message + nextbyte);
  for (i = 0; i < datachunk_size && consecutive_zero_bit_count < 8; i++) {
    //printf("%d\n", i);
    char character_to_add;

    while (bit < 8) {
      char abyte;
      read(fd, & abyte, 1);
      bytesread = bytesread + 1;

      if (skip){
        read(fd, & abyte, 1);
        bytesread = bytesread + 1;
        skip = 0;
      } else {
        skip = 1;
      }

      if ((abyte & (1 << 0)) != 0) { //bit is 1
        //printf("1\n");
        character_to_add = character_to_add | (1 << bit);
      } else {
        //printf("0\n");
        character_to_add = character_to_add & ~(1 << bit);
      }

      bit = bit + 1;
    }

    strncat(message, & character_to_add, 1);

    if (character_to_add == 0) {
      consecutive_zero_bit_count = 8;
    }

    bit = 0;
  }

  //printf("bytesread: %d\n", bytesread);
  printf("%s\n", message);
}

int encode_from_message(char * filename, char * message, int bytestoread){
  int fd = open(filename, O_RDONLY, 0644);
  char riff_header[36];
  read(fd, riff_header, 36);

  int fdwrite = open("audio.wav", O_WRONLY | O_CREAT, 0644);
  write(fdwrite, riff_header, 36);

  int found_data = 1; // 0 means "data" chunk has been found.
  int datachunk_size = 0;
  while (found_data) {
    char chunk_descriptor[5];
    read(fd, chunk_descriptor, 4);

    if (strcmp(chunk_descriptor, "data") == 0) {
      write(fdwrite, chunk_descriptor, 4);
      found_data = 0;
      int data_size;
      read(fd, & data_size, 4);
      //printf("Data_Size: %d\n", data_size);
      datachunk_size = data_size;
      write(fdwrite, & data_size, 4);
    } else {
      int size;
      read(fd, & size, 4); //gets subchunk size

      char * ignored_chunk_data = calloc(size, 1);
      read(fd, ignored_chunk_data, size); //ignores the unecessary chunk (skips it);
    }
  }

  //char * message = "once upon a time.";
  //char * message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Enim facilisis gravida neque convallis a. Tellus in metus vulputate eu. Arcu odio ut sem nulla pharetra diam. Posuere sollicitudin aliquam ultrices sagittis orci a. Imperdiet proin fermentum leo vel. Maecenas pharetra convallis posuere morbi leo. Nulla pellentesque dignissim enim sit amet venenatis urna. Velit ut tortor pretium viverra. Nulla facilisi nullam vehicula ipsum a arcu. Vitae suscipit tellus mauris a diam maecenas sed. Pellentesque habitant morbi tristique senectus et netus et malesuada fames. Consequat interdum varius sit amet mattis vulputate enim nulla aliquet. Libero volutpat sed cras ornare arcu dui. Donec ac odio tempor orci dapibus ultrices. Libero id faucibus nisl tincidunt eget.";
  int i;
  int bytesread = 0;
  int skip = 0;
  int bit = 0;
  int nextbyte = 0;
  char currentbyte = * (message + nextbyte);
  for (i = 0; i <= bytestoread; i++) {
    //printf("%c\n", currentbyte);
    //printf("%d\n", i);
    nextbyte = nextbyte + 1;
    while (bit < 8) {
      //printf("bit%d\n", bit);
      if ((currentbyte & (1 << bit)) != 0) { //bit is 1
        char abyte;
        read(fd, & abyte, 1);
        bytesread = bytesread + 1;

        if (skip){
          write(fdwrite, & abyte, sizeof(abyte));
          read(fd, & abyte, 1);
          bytesread = bytesread + 1;
          skip = 0;
        } else {
          skip = 1;
        }

        abyte = abyte | (1 << 0);

        write(fdwrite, & abyte, sizeof(abyte));
      } else {
        char abyte;
        read(fd, & abyte, 1);
        bytesread = bytesread + 1;

        if (skip){
          write(fdwrite, & abyte, sizeof(abyte));
          read(fd, & abyte, 1);
          bytesread = bytesread + 1;
          skip = 0;
        } else {
          skip = 1;
        }

        abyte = abyte & ~(1 << 0);

        write(fdwrite, & abyte, sizeof(abyte));
      }

      bit = bit + 1;
    }

    bit = 0;
    currentbyte = * (message + nextbyte);
  }

  //printf("bytesread: %d\n", bytesread);

  char * remainingbytes = calloc(datachunk_size - bytesread, 1);
  read(fd, remainingbytes, datachunk_size - bytesread);
  write(fdwrite, remainingbytes, datachunk_size - bytesread);

  return 0;
}

int encode(char * filename){
  char * message = calloc(1000, 1);

  int bytestoread = read(STDIN_FILENO, message, 1000);
  //fgets(message, 1000, stdin);

  encode_from_message(filename, message, bytestoread);

  return 0;
}

int main(int argc, char ** args) {
  if (argc < 4){
    printf("TO RUN: ./main [decode/encode] [method: lsb/parity] [filename.wav] [OPTIONAL: message (will read from stdin if not given)]\n");
    return 1;
  }

  if (strcmp(args[1], "encode") == 0){
    if (strcmp(args[2], "lsb") == 0){
      if (argc > 4){
        printf("Warning: if message is longer than 1000 bytes, behavior will be undefined\n");
        encode_from_message(args[3], args[4], strlen(args[4]));
        printf("MESSAGE HAS BEEN ENCODED TO audio.wav. RUN \"./main decode lsb audio.wav\" TO DECODE IT\n");
      } else {
        printf("Warning: if message is longer than 1000 bytes, behavior will be undefined\n");
        encode(args[3]);
        printf("MESSAGE HAS BEEN ENCODED TO audio.wav. RUN \"./main decode lsb audio.wav\" TO DECODE IT\n");
      }
    } else if (strcmp(args[2], "parity") == 0){
      if (argc > 4){
        //encode_from_message(args[3], args[4], strlen(args[4]));
      } else {
        //encode(args[3]);
      }
    }
  } else if (strcmp(args[1], "decode") == 0) {
    if (argc > 2){
      decode(args[3]);
    }
  }

  return 0;
}

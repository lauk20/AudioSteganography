#include <stdio.h>
#include <stdlib.h>

#include <fcntl.h>
#include <unistd.h>

#include <string.h>

void decode(){
  int fd = open("audio.wav", O_RDONLY, 0644);
  char riff_header[36];
  read(fd, riff_header, 36);

  int fdwrite = open("audio.wav", O_WRONLY | O_CREAT, 0644);
  write(fdwrite, riff_header, 36);

  char data_header[8];

  int found_data = 1; // 0 means "data" chunk has been found.
  int datachunk_size = 0;
  while (found_data) {
    char chunk_descriptor[5];
  	read(fd, chunk_descriptor, 4);

  	if (strcmp(chunk_descriptor, "data") == 0){
    	write(fdwrite, chunk_descriptor, 4);
    	found_data = 0;
    	int data_size;
    	read(fd, &data_size, 4);
    	printf("Data_Size: %d\n", data_size);
    	datachunk_size = data_size;
    	write(fdwrite, &data_size, 4);
  	} else {
    	int size;
    	read(fd, &size, 4); //gets subchunk size

    	char * ignored_chunk_data = calloc(size, 1);
    	read(fd, ignored_chunk_data, size); //ignores the unecessary chunk (skips it);
  	}
  }

  char * message = calloc(datachunk_size/8, 1);
  int i;
  int bytesread = 0;
  int skip = 0;
  int bit = 0;
  int nextbyte = 0;
  int consecutive_zero_bit_count = 0; //if it reaches 8 then null byte, so can stop
  char currentbyte = *(message + nextbyte);
  for (i = 0; i < datachunk_size && consecutive_zero_bit_count < 8; i++){
    //printf("%d\n", i);
    if (!skip){
      char character_to_add;

      while (bit < 8){
        char abyte;
        read(fd, &abyte, 1);
        bytesread = bytesread + 1;

        if ((abyte & (1 << 0)) != 0){ //bit is 1
          //printf("1\n");
          character_to_add = character_to_add | (1 << bit);
      	} else {
          //printf("0\n");
        	character_to_add = character_to_add & ~(1 << bit);
      	}

      	bit = bit + 1;
    	}

      strncat(message, &character_to_add, 1);

      if (character_to_add == 0){
        consecutive_zero_bit_count = 8;
      }

      bit = 0;
    }
  }

  //printf("bytesread: %d\n", bytesread);
  printf("Decoded message: %s\n", message);
}

int main(){
  int fd = open("furelise.wav", O_RDONLY, 0644);
  char riff_header[36];
  read(fd, riff_header, 36);

  int fdwrite = open("audio.wav", O_WRONLY | O_CREAT, 0644);
  write(fdwrite, riff_header, 36);

  char data_header[8];

  int found_data = 1; // 0 means "data" chunk has been found.
  int datachunk_size = 0;
  while (found_data) {
    char chunk_descriptor[5];
  	read(fd, chunk_descriptor, 4);

  	if (strcmp(chunk_descriptor, "data") == 0){
    	write(fdwrite, chunk_descriptor, 4);
    	found_data = 0;
    	int data_size;
    	read(fd, &data_size, 4);
    	printf("Data_Size: %d\n", data_size);
    	datachunk_size = data_size;
    	write(fdwrite, &data_size, 4);
  	} else {
    	int size;
    	read(fd, &size, 4); //gets subchunk size

    	char * ignored_chunk_data = calloc(size, 1);
    	read(fd, ignored_chunk_data, size); //ignores the unecessary chunk (skips it);
  	}
  }

  //char * message = "once upon a time.";
  char * message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Enim facilisis gravida neque convallis a. Tellus in metus vulputate eu. Arcu odio ut sem nulla pharetra diam. Posuere sollicitudin aliquam ultrices sagittis orci a. Imperdiet proin fermentum leo vel. Maecenas pharetra convallis posuere morbi leo. Nulla pellentesque dignissim enim sit amet venenatis urna. Velit ut tortor pretium viverra. Nulla facilisi nullam vehicula ipsum a arcu. Vitae suscipit tellus mauris a diam maecenas sed. Pellentesque habitant morbi tristique senectus et netus et malesuada fames. Consequat interdum varius sit amet mattis vulputate enim nulla aliquet. Libero volutpat sed cras ornare arcu dui. Donec ac odio tempor orci dapibus ultrices. Libero id faucibus nisl tincidunt eget.";
  int i;
  int bytesread = 0;
  int skip = 0;
  int bit = 0;
  int nextbyte = 0;
  char currentbyte = *(message + nextbyte);
  for (i = 0; i <= strlen(message); i++){
    //printf("%d\n", i);
    if (!skip){
      nextbyte = nextbyte + 1;
      while (bit < 8){
        //printf("bit%d\n", bit);
        if ((currentbyte & (1 << bit)) != 0){ //bit is 1
          char abyte;
        	read(fd, &abyte, 1);
        	bytesread = bytesread + 1;

        	abyte = abyte | (1 << 0);

        	write(fdwrite, &abyte, sizeof(abyte));
      	} else {
        	char abyte;
        	read(fd, &abyte, 1);
        	bytesread = bytesread + 1;

        	abyte = abyte & ~(1 << 0);

        	write(fdwrite, &abyte, sizeof(abyte));
      	}

      	bit = bit + 1;
    	}

      bit = 0;
      currentbyte = *(message + nextbyte);
    }
  }

  //printf("bytesread: %d\n", bytesread);

  int x;
  char * remainingbytes = calloc(datachunk_size - bytesread, 1);
  read(fd, remainingbytes, datachunk_size - bytesread);
  write(fdwrite, remainingbytes, datachunk_size - bytesread);

  decode();

  return 0;
}

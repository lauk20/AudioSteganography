#include <stdio.h>

#include <stdlib.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

void encode(char * filename, char * message){
    int fd = open(filename, O_WRONLY | O_APPEND, 0644);
    char var[5] = "LENO";
    write(fd, var, 4);

    //char message[1000] = "Greed will be the death of us all.";
    int size = strlen(message) + 1;
    write(fd, &size, 4);
    write(fd, message, size);
}

void decode(char * filename){
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
      free(ignored_chunk_data);
    }
  }
  //char data[datachunk_size]; //breaks with this for some reason. (segfault)
  char * data = calloc(datachunk_size, 1);
  read(fd, data, datachunk_size);

  char var[5];
  int chunksize = 0;
  read(fd, var, 4);
  read(fd, &chunksize, 4);

  char * message = calloc(chunksize, 1);
  strcpy(message, "");
  read(fd, message, chunksize);

  printf("%s\n", message);

  free(message);
  free(data);
}

int main(int argc, char ** args){
  if (argc < 3){
    printf("./alternate [encode/decode] [filename] [OPTIONAL for decode: message]\n");
    return -1;
  }
  if (strcmp(args[1], "encode") == 0){
    if (argc < 4){
      printf("./alternate [encode] [filename] [message]\n");
      return -1;
    }
    encode(args[2], args[3]);
  } else if (strcmp(args[1], "decode") == 0){
    if (argc < 3){
      printf("./alternate [decode] [filename]\n");
      return -1;
    }
    decode(args[2]);
  }

  return 0;
}

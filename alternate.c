#include <stdio.h>

#include <stdlib.h>

#include <fcntl.h>

#include <unistd.h>

#include <string.h>

void encode(char * filename){
    int fd = open(filename, O_WRONLY | O_APPEND, 0644);
    char var[5] = "LENO";
    write(fd, var, 4);

    char message[1000] = "Greed will be the death of us all.";
    int size = strlen(message + 1)
    write(fd, size, 4);
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
    }
  }
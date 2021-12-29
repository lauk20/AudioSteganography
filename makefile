default: main.o alternate.o
	gcc -o main main.o
	gcc -o alternate alternate.o
main.o: main.c
	gcc -c main.c
alternate.o: alternate.c
	gcc -c alternate.c

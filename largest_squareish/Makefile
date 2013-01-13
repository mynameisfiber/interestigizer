
CC = /usr/bin/gcc
CFLAGS = -Wall -g -m64 -shared -fPIC

largest_squareish.so:
	$(CC) $(CFLAGS) -Wl,-install_name,largest_squareish.so -o largest_squareish.so largest_squareish.c 

%.so : %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -rf *.o *.so largest_squareish_test *.dSYM

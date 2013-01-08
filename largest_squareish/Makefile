
CC = /usr/bin/gcc
CFLAGS = -Wall -g

largest_squareish.so:
	$(CC) $(CFLAGS) -DTEST -m64 -shared -Wl,-install_name,largest_squareish.so -o largest_squareish.so -fPIC largest_squareish.c 

test: largest_squareish.c largest_squareish_test.c
	$(CC) $(CFLAGS) -DTEST -o largest_squareish_test largest_squareish_test.c largest_squareish.c

%.o : %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -rf *.o largest_squareish_test largest_squareish_test.dSYM

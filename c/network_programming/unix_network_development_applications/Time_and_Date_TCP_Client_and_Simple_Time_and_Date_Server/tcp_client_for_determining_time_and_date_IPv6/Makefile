CC = gcc
CFLAGS = -Wall -Werror
LDFLAGS =

SRCS = main.c error.c timeutil.c

my_program: $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $@ $(LDFLAGS)

clean:
	rm -f my_program

.PHONY: clean

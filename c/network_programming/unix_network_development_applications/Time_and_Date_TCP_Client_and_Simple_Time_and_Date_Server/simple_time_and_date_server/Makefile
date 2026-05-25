# Makefile для MacOS

CC = gcc
CFLAGS = -Wall -g

SOURCES = main.c utils.c 
OBJECTS = $(SOURCES:.c=.o)
EXECUTABLE = server

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(OBJECTS) -o $(EXECUTABLE)

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@
	
clean:
	rm -f $(EXECUTABLE) $(OBJECTS)
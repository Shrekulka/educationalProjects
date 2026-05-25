**The code represents a time and date server that listens for incoming connections on port 13 (daytime) and responds to 
clients with the current time in the format "Day, Month DD YYYY HH:MM:SS\r\n". The code performs the following tasks:**

1. Creates a socket to listen for incoming connections on port 13 (daytime).
2. Binds the socket to an address and port.
3. Sets the socket to listen for connections with a maximum queue of pending connections (LISTENQ).
4. In an infinite loop, it waits for incoming connections from clients.
5. Upon accepting a connection from a client, it retrieves the current time and sends it to the client as a time string.
6. Closes the socket to terminate the connection with the client.
7. The entire code is organized in the main function, which starts the server and runs indefinitely, serving clients.

**To use this code:**

1. Compile it using the provided 'Makefile.'
2. Start the server by running './server' in the console.

After starting the server, it will begin listening on port 13, and clients can connect to it to retrieve the current 
time and date. Note that the server will run indefinitely and respond to client requests until you manually stop it.

This code also includes a modular structure with functionality separated into different files (common.h, config.h, 
error.h, utils.h) to improve code readability and maintainability. Additionally, it incorporates error handling to 
ensure the server's reliability.

1. To compile this code on macOS, you can use the following 'Makefile':
    ```
    # Makefile for macOS
    
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
    ```
2. Run the 'make' command in the console to compile.
3. Start the application with the './server' command.
4. Use 'make clean' to clean up.

This Makefile:
- Compiles each .c file into a .o file.
- Links the objects into the server executable.
- Has 'all' and 'clean' targets and a compilation rule %.
- Allows you to compile this sample code using 'make'.




**Код представляет собой сервер времени и даты, который слушает входящие соединения на порту 13 (daytime) и отвечает 
клиентам текущим временем в формате "День, Месяц ДД ГГГГ ЧЧ:ММ:СС\r\n". Код выполняет следующие задачи:**

1. Создает соксет для прослушивания входящих соединений на порту 13 (daytime).
2. Привязывает соксет к адресу и порту.
3. Переводит соксет в режим прослушивания соединений с максимальной очередью ожидающих соединений (LISTENQ).
4. В бесконечном цикле ожидает входящие соединения от клиентов.
5. При принятии соединения с клиентом, получает текущее время и отправляет его клиенту в виде строки с временем.
6. Закрывает соксет для завершения соединения с клиентом.
7. Весь код организован в функции main, которая запускает сервер и работает бесконечно, обслуживая клиентов.

**Чтобы использовать этот код:**

1. Скомпилируйте его с помощью предложенного 'Makefile'.
2. Запустите сервер, выполнив './server' в консоли.

После запуска сервер начнет прослушивать на порту 13, и клиенты смогут подключаться к нему, чтобы получить текущее время
и дату. Обратите внимание, что сервер будет работать бесконечно и будет отвечать на запросы от клиентов до тех пор, пока
вы не остановите его вручную.

Этот код также включает в себя модульную структуру с разделением функциональности на различные файлы (common.h, config.h,
error.h, utils.h) для улучшения читаемости и обслуживаемости кода. Кроме того, он содержит обработку ошибок для 
обеспечения надежности работы сервера.


1. Для компиляции этого кода на MacOS можно использовать следующий 'Makefile':
    ```
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
    ```
2. В консоли выполнить команду make для компиляции
3. Запустить приложение командой './server'
4. 'make clean' для очистки

   Этот Makefile:
   - Компилирует каждый .c файл в .o
   - Связывает объекты в исполняемый файл server
   - Имеет цели 'all', 'clean' и правило компиляции %:
   - Позволяет компилировать этот пример кода с помощью 'make'.
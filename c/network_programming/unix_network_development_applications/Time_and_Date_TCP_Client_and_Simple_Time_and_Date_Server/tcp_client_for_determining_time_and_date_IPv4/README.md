**This program is a client-server application that establishes a connection with a remote server using the TCP/IP 
protocol, reads data from the server, and outputs them, adjusting the time according to the time zone.**

**Here is a description of each file in your project:**

1. 'common.h': This header file includes common libraries and header files for the entire program. It also contains 
   definitions of constants, structures, and enumerations used in other parts of the program.
2. 'config.h': This header file contains configuration settings such as buffer size, port addresses, date and time 
   formats. It also contains the definition of the TimeZoneInfo structure, which stores information about the time zone.
3. 'timeutil.h': This header file contains prototypes of functions correctTimezone and incrementDate, used to adjust 
   time and increment the date according to the time zone.
4. 'timeutil.c': This file implements the correctTimezone and incrementDate functions, which perform time adjustment and
   date incrementation, respectively.
5. 'error.h': This header file contains prototypes of functions err_quit and err_sys, used for error handling and 
   displaying error messages.
6. 'error.c': This file implements the err_quit and err_sys functions, which exit the program with an error message and 
   handle system errors.
7. 'main.c': This is the main program file, which contains the main function. It performs the following actions:
    - Creates a socket and establishes a connection with the server using the IP address passed as a command-line argument.
    - Initializes the TimeZoneInfo structure for the Kyiv time zone.
    - Reads data from the socket and adjusts the time according to the time zone.
    - Outputs the adjusted time to the screen.

**Settings and Compilation:**

1. Server IP Address: Ensure that the server's IP address is passed to the program as a command-line argument when 
   running it. This means that when starting the program, you need to specify the IP address as an argument. For example:
    ```
    ./main 132.163.97.4
    ```
   Where 'main' is the name of the executable file of your program, and '132.163.97.4' is the IP address of the remote 
   server.
2. C Compiler: Your program should be compiled using a C compiler such as GCC. Make sure you have a C compiler installed
   and accessible from the command line.
3. Integrated Development Environment (e.g., CLion): If you are using an integrated development environment like CLion,
   you can create a project in this environment and set it up to build your program. In CLion, you can follow these steps:
   a) Open your project in CLion.
   b) Create a run configuration for your program and specify command-line arguments, including the server's IP address:
        - Go to the run/debug configuration settings (Run/Debug Configurations).
        - Find your program in the configurations list and ensure that the "Program arguments" field contains the 
          server's IP address. For example: `132.163.97.4`.
        - Save the settings and try running the program.
   c) Ensure that CLion is properly configured to use a C compiler (e.g., GCC).

** The conclusion is this:**
```
60234 23-10-17 10:27:18 20 0 0 879.4 UTC(NIST) *
Year: 23
Month: 10
Day: 17
Hour: 13
Minute: 27
Second: 18

Process finished with exit code 0
```

**Running a Program via Terminal:**

Make sure you are in the correct directory where the compiled program file is located. You can use the cd command to 
navigate to the directory containing the executable file named main. Then, run the program as follows:
```
cd /path/to/directory/with/executable/file
./my_program 132.163.97.4
```

**The output will be as follows:**
```
makefile
Copy code
60234 23-10-17 11:05:40 20 0 0 81.3 UTC(NIST) *
Year: 23
Month: 10
Day: 17
Hour: 14
Minute: 5
Second: 40
```




**Данная программа представляет собой клиент-серверное приложение, которое устанавливает соединение с удаленным сервером 
по протоколу TCP/IP, читает данные с сервера и выводит их, корректируя время согласно часовому поясу.**

**Вот описание каждого файла в вашем проекте:**


1. 'common.h': Этот заголовочный файл включает общие библиотеки и заголовочные файлы для всей программы. Он также 
   содержит определения констант, структур и перечислений, используемых в других частях программы.
2. 'config.h': Этот заголовочный файл содержит конфигурационные настройки, такие как размер буфера, адреса порта, 
   форматы даты и времени. Он также содержит определение структуры 'TimeZoneInfo', которая хранит информацию о часовом 
   поясе.
3. 'timeutil.h': Этот заголовочный файл содержит прототипы функций 'correctTimezone' и 'incrementDate', которые 
   используются для коррекции времени и инкрементирования даты согласно часовому поясу.
4. 'timeutil.c': В этом файле реализованы функции 'correctTimezone' и 'incrementDate', которые выполняют коррекцию 
   времени и инкрементацию даты, соответственно.
5. 'error.h': Этот заголовочный файл содержит прототипы функций 'err_quit' и 'err_sys', используемых для обработки 
   ошибок и вывода сообщений об ошибках.
6. 'error.c': В этом файле реализованы функции 'err_quit' и 'err_sys', которые выполняют выход из программы с сообщением
   об ошибке и обработку системных ошибок.
7. 'main.c': Это главный файл программы, который содержит функцию main. Он выполняет следующие действия:
    - Создание сокета и установка соединения с сервером с использованием IP-адреса, переданного в аргументе командной 
      строки.
    - Инициализация структуры 'TimeZoneInfo' для часового пояса Киева.
    - Чтение данных из сокета и коррекция времени согласно часовому поясу.
    - Вывод скорректированного времени на экран.
   
**Настройки и сборка:**

1. IP-адрес сервера: Убедитесь, что IP-адрес сервера передается в программу в качестве аргумента командной строки при 
   запуске. Это означает, что при запуске программы необходимо указать IP-адрес в качестве аргумента. Например:
    ```
    ./main 132.163.97.4
    ```
   Где main - это имя исполняемого файла вашей программы, а ```132.163.97.4``` - IP-адрес удаленного сервера.
2. Компилятор C: Ваша программа должна быть собрана с использованием компилятора C, такого как GCC. Убедитесь, что у вас
   установлен компилятор C и он доступен в командной строке.
3. Среда разработки (например, CLion): Если вы используете среду разработки, такую как CLion, вы можете создать проект в
   этой среде и настроить его для сборки вашей программы. В CLion, это можно сделать, следуя следующим шагам:
   a) Откройте проект в CLion.
   b) Создайте конфигурацию запуска для вашей программы и укажите аргументы командной строки, включая IP-адрес сервера:
      - Перейдите в раздел настройки запуска (Run/Debug Configurations).
      - В списке конфигураций найдите вашу программу и убедитесь, что в поле "Program arguments" установлен IP-адрес 
        сервера. Например: ```132.163.97.4```
      - Сохраните настройки и попробуйте запустить программу.
   c) Убедитесь, что CLion правильно настроен на использование компилятора C (например, GCC).

**Вывод такой:**
```
60234 23-10-17 10:27:18 20 0 0 879.4 UTC(NIST) *
Year: 23
Month: 10
Day: 17
Hour: 13
Minute: 27
Second: 18

Process finished with exit code 0
```

**Запуск программы через терминал:**

Убедитесь, что вы находитесь в правильном каталоге, где находится скомпилированный файл программы. Вы можете 
использовать команду cd для перехода в каталог, где находится исполняемый файл main. Затем запустите программу следующим
образом:
```
cd /путь/к/каталогу/с/исполняемым/файлом
./my_program 132.163.97.4
```
**Вывод такой:**
```
60234 23-10-17 11:05:40 20 0 0  81.3 UTC(NIST) *
Year: 23
Month: 10
Day: 17
Hour: 14
Minute: 5
Second: 40
```
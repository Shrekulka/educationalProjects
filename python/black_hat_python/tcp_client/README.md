The provided code is a Python script that establishes a TCP connection to a server, sends data to the server, receives 
a response, and then prints the received data.

Here's a breakdown of how the code works:

1. The `connect_to_server` function is defined, which takes `target_host` and `target_port` as input parameters. This 
   function handles the connection to the server and sending/receiving data.

2. Inside the `connect_to_server` function:
   - A socket object named `client` is created using `socket.socket`.
   - The client socket is connected to the target host and port using `client.connect((target_host, target_port))`.
   - User input is taken to get data to send to the server.
   - The input data is encoded as bytes using `data_to_send.encode()` and sent to the server using `client.send()`.
   - A byte object named `data` is created to store the received data.
   - The function enters a loop where it receives data from the server in chunks of up to 4096 bytes using 
     `client.recv(4096)`. The received data is added to the `data` object.
   - The loop continues until there is no more data to receive (when `response` is empty).
   - Finally, the received data is returned after decoding it from bytes to a UTF-8 encoded string using 
     `data.decode("utf-8")`.

3. The `main` function is defined, which serves as the entry point of the script.
   - The `target_host` is set to `"localhost"` and the `target_port` is set to `5050`.
   - The `connect_to_server` function is called with the target host and port as arguments, and the received data is 
     stored in the `received_data` variable.
   - The received data is printed.

4. The `main` function is called only if the script is run directly (not imported as a module).

To use this code, you need to provide the appropriate `target_host` and `target_port` values. The `target_host` should 
be the hostname or IP address of the server you want to connect to, and the `target_port` should be the port number on 
which the server is listening for connections.


To use this code, you will need to complete the following steps:

1. Set target host and port: The target_host and target_port variables are defined in the code. Replace the values of 
   these with the appropriate host and port that you want to connect to.
2. Run the script: Save the file and run it using a Python interpreter. The script will establish a connection to the 
   specified host and port, send data to the server, accept the response, and display it on the screen.
3. Enter data to send: After running the script you will be prompted to enter the data that will be sent to the 
   server. Enter the required data and press Enter.
4. Wait for response: After sending the data, the script will wait for a response from the server. When the response is 
   received, it will be displayed.

Important: 
Make sure that the target server is available and running on the specified host and port. Otherwise, the script may not 
establish a connection or get an error when sending data.

This is the basic process of using this code. You can customize the code and make changes to fit your needs and 
requirements for communicating with the server.




Предоставленный код является скриптом на языке Python, который устанавливает TCP-соединение с сервером, отправляет 
данные на сервер, принимает ответ и затем выводит принятые данные.

Вот пошаговое описание того, как работает код:

1. Определена функция `connect_to_server`, которая принимает входные параметры `target_host` и `target_port`. Эта 
   функция отвечает за установку соединения с сервером и отправку/прием данных.

2. Внутри функции `connect_to_server`:
   - Создается объект сокета с именем `client` с помощью `socket.socket`.
   - Сокет клиента подключается к указанному хосту и порту с помощью `client.connect((target_host, target_port))`.
   - Пользовательский ввод используется для получения данных, которые будут отправлены на сервер.
   - Входные данные кодируются в байты с помощью `data_to_send.encode()` и отправляются на сервер с использованием 
     `client.send()`.
   - Создается объект байтов `data`, который будет использоваться для сохранения принятых данных.
   - Функция входит в цикл, в котором она получает данные от сервера порциями до 4096 байт с помощью `client.recv(4096)`.
     Полученные данные добавляются в объект `data`.
   - Цикл продолжается до тех пор, пока нет больше данных для получения (когда `response` пустой).
   - В конечном итоге принятые данные декодируются из байтов в строку с использованием `data.decode("utf-8")` и 
     возвращаются.

3. Определена функция `main`, которая является точкой входа в скрипт.
   - `target_host` устанавливается как `"localhost"`, а `target_port` - как `5050`.
   - Вызывается функция `connect_to_server` с указанным хостом и портом в качестве аргументов, а принятые данные 
     сохраняются в переменной `received_data`.
   - Принятые данные выводятся на экран.

4. Функция `main` вызывается только в случае, если скрипт запущен напрямую (а не импортирован как модуль).

Для использования этого кода вам необходимо предоставить правильные значения `target_host` и `target_port`. `target_host`
должен быть именем хоста или IP-адресом сервера, к которому вы хотите подключиться, а `target_port` - номером порта, на 
котором сервер ожидает соединений.


Чтобы использовать данный код, вам потребуется выполнить следующие шаги:

1. Установите целевой хост и порт: В коде определены переменные target_host и target_port. Замените значения этих 
   переменных на соответствующие хост и порт, к которым вы хотите подключиться.
2. Запустите скрипт: Сохраните файл и запустите его с помощью интерпретатора Python. Скрипт установит соединение с 
   указанным хостом и портом, отправит данные на сервер, примет ответ и выведет его на экран.
3. Введите данные для отправки: После запуска скрипта вы будете приглашены ввести данные, которые будут отправлены на 
   сервер. Введите необходимые данные и нажмите Enter.
4. Дождитесь ответа: После отправки данных скрипт будет ожидать ответа от сервера. Когда ответ будет получен, он будет 
   выведен на экран.

Важно: 
Убедитесь, что целевой сервер доступен и запущен на указанном хосте и порту. В противном случае скрипт может не 
установить соединение или получить ошибку при отправке данных.

Это основной процесс использования данного кода. Вы можете настроить код и вносить изменения, чтобы соответствовать 
вашим потребностям и требованиям взаимодействия с сервером.
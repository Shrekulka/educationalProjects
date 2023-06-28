import socket
import threading

# Насчет хоста (IP)— мы оставим строку пустой, чтобы наш сервер был доступен для всех интерфейсов.
# IP = "127.0.0.1" - localhost
# можно и так - IP = ""
IP = "0.0.0.0"
# В большинстве операционных систем прослушивание портов с номерами 0 — 1023 требует особых привилегий.
PORT = 5056


# Функция handle_client выполняет вызов recv(), после чего возвращает клиенту простое сообщение.
def handle_client(client_socket):
    """
        Функция для обработки входящего клиентского соединения.

        Parameters:
            client_socket (socket.socket): Сокет клиента, представляющий входящее соединение.

        Returns:
            None
    """
    try:
        request = client_socket.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        if not request:
            return

        # для некоторых программ передаем ответ, как HTML информацию - для того, чтоб корректно отображалось
        # HDRS = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        # content = "Hello buddy...".encode('utf-8')
        # client_socket.send(HDRS.encode('utf-8') + content)
        # или
        client_socket.send(b'ACK')
    finally:
        client_socket.close()


def main():
    """
       Основная функция для запуска TCP-сервера.

       Returns:
           None
    """
    # Свяжем наш сокет с данными хостом и портом с помощью метода bind, которому передается кортеж, первый элемент
    # (или нулевой, если считать от нуля) которого — хост, а второй — порт
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Вначале мы передаем IP-адрес и порт, который должен прослушивать наш сервер
    server.bind((IP, PORT))

    # или можем заменить эти две строчки:
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((IP, PORT))
    # на
    # server = socket.create_server(IP, PORT)

    # Затем просим сервер начать прослушивание, указав, что отложенных соединений должно быть не больше пяти.
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    # Затем сервер входит в свой главный цикл, в котором ждет входящее соединение.
    while True:
        # При подключении клиента мы получаем клиентский сокет в переменной client и подробности об удаленном
        # соединении в переменной address.
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        # Затем создаем объект нового потока, который указывает на нашу функцию handle_client, и передаем этой функции
        # клиентское соединение.
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
        # В этот момент главный цикл сервера освобождается для обработки следующего входящего соединения.


if __name__ == '__main__':
    main()

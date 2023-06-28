import socket


def connect_to_server(target_host, target_port):
    """
    Функция для подключения к серверу и отправки данных.

    Parameters:
        target_host (str): Целевой хост для подключения.
        target_port (int): Целевой порт для подключения.

    Returns:
        str: Принятые данные от сервера.
    """
    # создаем объект сокета
    # Параметр AF_INET говорит о том, что мы будем использовать стандартный адрес IPv4 или сетевое имя, а SOCK_STREAM
    # означает, что клиент будет работать по TCP.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # подключаем клиент
        client.connect((target_host, target_port))

        # запрашиваем данные у пользователя
        data_to_send = input("Введите данные для отправки: ")

        # отправляем данные в виде байтов
        client.send(data_to_send.encode())

        # Создаем пустой байтовый объект для сохранения принятых данных
        data = b""

        # Получаем данные от сервера, максимум 4096 байт за один раз
        response = client.recv(4096)

        # Проверяем, получены ли данные
        while response:
            data += response  # Добавляем полученные данные к общим принятым данным
            response = client.recv(4096)  # Продолжаем получение данных от сервера

        # Возвращаем принятые данные, декодируя их из байтового представления в строку
        return data.decode("utf-8")

    finally:
        client.close()  # В любом случае, даже при возникновении исключения, закрываем клиентский сокет


def main():
    """
           Основная функция для запуска TCP-сервера.

           Returns:
               None
    """
    # target_host = "www.google.com" или ip - "127.0.0.1"
    target_host = "localhost"
    target_port = 5050

    received_data = connect_to_server(target_host, target_port)
    print(received_data)


if __name__ == '__main__':
    main()

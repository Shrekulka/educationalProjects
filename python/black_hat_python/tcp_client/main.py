import socket
import traceback

from logger_config import logger


def connect_to_server(target_host: str, target_port: int) -> str:
    """
        Функция для подключения к серверу и отправки данных.

        Parameters:
            target_host (str): Целевой хост для подключения.
            target_port (int): Целевой порт для подключения.

        Returns:
            str: Принятые данные от сервера.
    """
    # Создаем объект сокета
    # Параметр AF_INET говорит о том, что мы будем использовать стандартный адрес IPv4 или сетевое имя, а SOCK_STREAM
    # означает, что клиент будет работать по TCP.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        logger.info(f"Attempting to connect to {target_host}:{target_port}")
        # Подключаем клиент
        client.connect((target_host, target_port))
        logger.info(f"Connected to {target_host}:{target_port}")

        # Запрашиваем данные у пользователя
        data_to_send = input("Введите данные для отправки: ")

        # Отправляем данные в виде байтов
        client.send(data_to_send.encode())
        logger.info(f"Sent data: {data_to_send}")

        # Создаем пустой байтовый объект для сохранения принятых данных
        data = b""

        # Получаем данные от сервера, максимум 4096 байт за один раз
        response = client.recv(4096)
        logger.info("Receiving data from server")

        # Проверяем, получены ли данные
        while response:
            data += response  # Добавляем полученные данные к общим принятым данным
            response = client.recv(4096)  # Продолжаем получение данных от сервера

        # Возвращаем принятые данные, декодируя их из байтового представления в строку
        received_data = data.decode("utf-8")
        logger.info(f"Received data: {received_data}")
        return received_data

    except Exception as e:
        error_message = traceback.format_exc()
        logger.error(f"Error in connection: {e}\n{error_message}")
        raise

    finally:
        client.close()  # В любом случае, даже при возникновении исключения, закрываем клиентский сокет
        logger.info("Closed the client socket")


def main() -> None:
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
    try:
        # Запускаем основную функцию
        main()

    except KeyboardInterrupt:
        # Обрабатываем прерывание пользователем
        logger.warning("Application terminated by user")

    except Exception as error:
        # Логируем неожиданные исключения во время выполнения
        detailed_error_message = traceback.format_exc()
        logger.error(f"Unexpected error in the application: {error}\n{detailed_error_message}")

    finally:
        # Логируем завершение работы приложения
        logger.info("Application finished")

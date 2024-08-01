# tcp_client/simple_tcp_client.py

import socket
import traceback

from logger_config import logger


def main() -> None:
    """
       Основная функция для запуска TCP-сервера.

       Returns:
           None
    """
    # Указываем целевой хост и порт для подключения
    # target_host = "www.google.com" или ip - "127.0.0.1"
    target_host = "localhost"
    target_port = 5050

    # Создаем объект сокета с использованием IPv4 и TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключаемся к указанному хосту и порту
    client.connect((target_host, target_port))

    # Отправляем сообщение серверу
    client.send(b"Hello, world!")

    # Получаем ответ от сервера
    responce = client.recv(4096)

    # Декодируем и выводим ответ на экран
    print(responce.decode("utf-8"))

    # Закрываем сокет
    client.close()


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

# bidirectional_streaming_chat_service/bidirectional_streaming_server.py

import threading
import time
import traceback
import typing
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

import bidirectional_streaming_pb2
import bidirectional_streaming_pb2_grpc
from logger_config import logger


class ChatServicer(bidirectional_streaming_pb2_grpc.ChatServiceServicer):
    """
    Реализация сервиса ChatService для обмена сообщениями в реальном времени.

    Этот класс реализует метод Chat, который обеспечивает двунаправленный
    потоковый обмен сообщениями между клиентами и сервером.

    Наследует:
        bidirectional_streaming_pb2_grpc.ChatServiceServicer: Базовый класс для реализации
        двунаправленного потокового gRPC сервиса.
    """

    def __init__(self):
        self.messages: typing.List[bidirectional_streaming_pb2.ChatMessage] = []
        self.lock = threading.Lock()

    def Chat(self, request_iterator: typing.Iterator[bidirectional_streaming_pb2.ChatMessage],
             context: grpc.ServicerContext) -> typing.Iterator[bidirectional_streaming_pb2.ChatMessage]:
        """
        Метод Chat обеспечивает двунаправленный обмен сообщениями.

        Args:
            request_iterator (typing.Iterator[bidirectional_streaming_pb2.ChatMessage]):
                Итератор входящих сообщений чата.
            context (grpc.ServicerContext): Контекст gRPC, предоставляющий метаданные о вызове.

        Yields:
            bidirectional_streaming_pb2.ChatMessage: Исходящие сообщения чата.
        """

        def listen_for_messages() -> typing.Iterator[bidirectional_streaming_pb2.ChatMessage]:
            """
            Внутренняя функция для прослушивания и сохранения входящих сообщений.

            Yields:
                bidirectional_streaming_pb2.ChatMessage: Новые входящие сообщения.
            """
            # Итерируемся по входящим сообщениям из request_iterator
            for new_message in request_iterator:
                # Используем блокировку для безопасного доступа к общему ресурсу (списку сообщений)
                with self.lock:
                    # Добавляем новое сообщение в общий список сообщений
                    self.messages.append(new_message)
                # Возвращаем новое сообщение в поток
                yield new_message

        # Создаем новый поток для прослушивания входящих сообщений
        # lambda: list(...) используется для преобразования генератора в список,
        # что заставляет функцию выполняться до конца
        message_thread = threading.Thread(target=lambda: list(listen_for_messages()))
        # Запускаем поток прослушивания
        message_thread.start()

        # Инициализируем индекс последнего отправленного сообщения
        last_index: int = 0
        # Бесконечный цикл для постоянной отправки новых сообщений клиенту
        while True:
            # Используем блокировку для безопасного доступа к общему списку сообщений
            with self.lock:
                # Проверяем, есть ли новые сообщения для отправки
                while last_index < len(self.messages):
                    # Отправляем клиенту новое сообщение
                    yield self.messages[last_index]
                    # Увеличиваем индекс последнего отправленного сообщения
                    last_index += 1
            # Добавляем небольшую задержку, чтобы не перегружать процессор
            # постоянными проверками на наличие новых сообщений
            time.sleep(0.1)


def serve() -> None:
    """
    Инициализирует и запускает gRPC сервер для обработки запросов к сервису ChatService.

    Эта функция:
    1. Создает и настраивает gRPC сервер.
    2. Регистрирует реализацию сервиса ChatServicer.
    3. Включает поддержку рефлексии для упрощения взаимодействия с сервисом.
    4. Запускает сервер и ожидает его завершения.

    Важно:
    - Сервер будет слушать входящие соединения на порту 50054.
    - Рефлексия позволяет клиентам запрашивать метаданные о сервисах и методах.
    """
    # Создание gRPC сервера с пулом потоков для обработки входящих запросов.
    # Пул потоков позволяет одновременно обрабатывать несколько запросов.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрация сервиса ChatServiceServicer на сервере.
    # Это связывает реализацию сервиса с сервером, чтобы он мог обрабатывать запросы к этому сервису.
    bidirectional_streaming_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServicer(), server
    )

    # Определение списка имен сервисов, которые будут поддерживать рефлексию.
    # Включает имя зарегистрированного сервиса и имя встроенного сервиса рефлексии.
    SERVICE_NAMES = (
        # Имя зарегистрированного сервиса
        bidirectional_streaming_pb2.DESCRIPTOR.services_by_name['ChatService'].full_name,
        reflection.SERVICE_NAME,
    )

    # Включение поддержки рефлексии на сервере.
    # Это позволяет клиентам запрашивать информацию о сервисах и методах на сервере.
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Настройка сервера на прослушивание входящих соединений на порту 50054.
    # '[::]:50054' означает, что сервер будет слушать на всех сетевых интерфейсах на этом порту.
    server.add_insecure_port('[::]:50054')

    # Запуск сервера. После запуска сервер начнет принимать и обрабатывать входящие запросы.
    server.start()

    print("Сервер двунаправленного потокового RPC запущен на порту 50054")

    # Ожидание завершения работы сервера
    server.wait_for_termination()


# Точка входа в программу, запускаем сервер при выполнении скрипта.
if __name__ == '__main__':
    try:
        serve()
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Неожиданная ошибка приложения: {error}\n{detailed_error}")

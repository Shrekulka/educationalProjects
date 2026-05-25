# streaming_grpc_string_analyzer/streaming_server.py

import traceback
import typing
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

import streaming_pb2
import streaming_pb2_grpc
from logger_config import logger


class StringAnalyzerStreamingServicer(streaming_pb2_grpc.StreamingServiceServicer):
    """
    Реализация сервиса StreamingService для анализа строки.

    Этот класс реализует метод StreamData, который принимает строку в запросе и возвращает поток результатов,
    включая анализ палиндромов, подсчет слов, букв, пробелов, спецсимволов, а также заглавных и строчных букв.

    Наследует:
        streaming_pb2_grpc.StreamingServiceServicer: Базовый класс для реализации потокового gRPC сервиса.
    """

    def StreamData(self, request: streaming_pb2.StreamDataRequest, context: grpc.ServicerContext) -> typing.Iterator[
        streaming_pb2.StreamDataResponse]:
        """
        Метод StreamData анализирует входную строку и отправляет результаты в потоке.

        Args:
            request (streaming_pb2.StreamDataRequest): Запрос, содержащий строку для анализа.
            context (grpc.ServicerContext): Контекст gRPC, который предоставляет метаинформацию о вызове.

        Yields:
            streaming_pb2.StreamDataResponse: Поток сообщений с результатами анализа строки, такими как проверка палиндрома,
            подсчет слов, букв, пробелов, спецсимволов, а также заглавных и строчных букв.
        """
        # Получаем строку из запроса.
        text = request.input_text

        # Проверка палиндрома
        ################################################################################################################
        if text == text[::-1]:
            yield streaming_pb2.StreamDataResponse(type="palindrome", result="Yes, it is a palindrome!")
        else:
            yield streaming_pb2.StreamDataResponse(type="palindrome", result="No, it is not a palindrome!")
        ################################################################################################################

        # Подсчет слов
        ################################################################################################################
        word_count = len(text.split())
        yield streaming_pb2.StreamDataResponse(type="word_count", result=f"Word count: {word_count}")
        ################################################################################################################

        # Подсчет букв, пробелов и спецсимволов
        ################################################################################################################
        letter_count = sum(c.isalpha() for c in text)  # Подсчитываем количество букв.
        space_count = text.count(' ')  # Подсчитываем количество пробелов.
        special_count = len(text) - letter_count - space_count  # Вычисляем количество спецсимволов.
        yield streaming_pb2.StreamDataResponse(type="letter_count", result=f"Letters: {letter_count}")
        yield streaming_pb2.StreamDataResponse(type="space_count", result=f"Spaces: {space_count}")
        yield streaming_pb2.StreamDataResponse(type="special_count", result=f"Special characters: {special_count}")
        ################################################################################################################

        # Подсчет заглавных и строчных букв
        ################################################################################################################
        upper_count = sum(c.isupper() for c in text)  # Подсчитываем количество заглавных букв.
        lower_count = sum(c.islower() for c in text)  # Подсчитываем количество строчных букв.
        yield streaming_pb2.StreamDataResponse(type="upper_count", result=f"Uppercase letters: {upper_count}")
        yield streaming_pb2.StreamDataResponse(type="lower_count", result=f"Lowercase letters: {lower_count}")
        ################################################################################################################


def serve() -> None:
    """
    Инициализирует и запускает gRPC сервер для обработки запросов к сервису StringAnalyzerStreamingServicer.

    Эта функция:
    1. Создает и настраивает gRPC сервер.
    2. Регистрирует реализацию сервиса StringAnalyzerStreamingServicer.
    3. Включает поддержку рефлексии, что позволяет клиентам запрашивать метаданные о сервисах и методах.
    4. Запускает сервер и ожидает его завершения.

    Важно:
    - Сервер будет слушать входящие соединения на порту 50052.
    - Рефлексия используется для упрощения работы с gRPC сервисами через инструменты, такие как `grpcurl` и Postman.
    """
    # Создание gRPC сервера с пулом потоков для обработки входящих запросов.
    # Пул потоков позволяет одновременно обрабатывать несколько запросов.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрация сервиса StringAnalyzerStreamingServicer на сервере.
    # Это связывает реализацию сервиса с сервером, чтобы он мог обрабатывать запросы к этому сервису.
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StringAnalyzerStreamingServicer(), server)

    # Определение списка имен сервисов, которые будут поддерживать рефлексию.
    # Включает имя зарегистрированного сервиса и имя встроенного сервиса рефлексии.
    SERVICE_NAMES = (
        streaming_pb2.DESCRIPTOR.services_by_name['StreamingService'].full_name,  # Имя зарегистрированного сервиса
        reflection.SERVICE_NAME,  # Имя сервиса рефлексии
    )

    # Включение поддержки рефлексии на сервере.
    # Это позволяет клиентам запрашивать информацию о сервисах и методах на сервере.
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Настройка сервера на прослушивание входящих соединений на порту 50052.
    # '[::]:50052' означает, что сервер будет слушать на всех сетевых интерфейсах на этом порту.
    server.add_insecure_port('[::]:50052')

    # Запуск сервера. После запуска сервер начнет принимать и обрабатывать входящие запросы.
    server.start()

    print("Сервер потокового RPC запущен на порту 50052")

    # Ожидание завершения работы сервера. Функция будет блокировать выполнение до тех пор,
    # пока сервер не будет остановлен, что позволяет серверу продолжать работу и принимать запросы.
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

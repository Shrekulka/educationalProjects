# client_streaming_average_calculator/client_streaming_server.py

import traceback
import typing
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

import client_streaming_pb2
import client_streaming_pb2_grpc
from logger_config import logger


class AverageCalculatorServicer(client_streaming_pb2_grpc.AverageCalculatorServicer):
    """
    Реализация сервиса AverageCalculator для вычисления среднего значения.

    Этот класс реализует метод CalculateAverage, который принимает поток чисел
    и возвращает их среднее значение.

    Наследует:
        client_streaming_pb2_grpc.AverageCalculatorServicer: Базовый класс для реализации
        клиентского потокового gRPC сервиса.
    """

    def CalculateAverage(self, request_iterator: typing.Iterator[client_streaming_pb2.NumberRequest],
                         context: grpc.ServicerContext) -> client_streaming_pb2.AverageResponse:
        """
        Метод CalculateAverage вычисляет среднее значение из входящего потока чисел.

        Args:
            request_iterator (typing.Iterator[client_streaming_pb2.NumberRequest]):
                Итератор входящих запросов, содержащих числа.
            context (grpc.ServicerContext): Контекст gRPC, предоставляющий метаданные о вызове.

        Returns:
            client_streaming_pb2.AverageResponse: Ответ, содержащий вычисленное среднее значение.
        """
        total: float = 0
        count: int = 0

        # Итерируемся по входящему потоку чисел
        for request in request_iterator:
            total += request.number
            count += 1

        # Проверка на случай, если не было получено ни одного числа
        if count == 0:
            return client_streaming_pb2.AverageResponse(average=0)

        # Вычисление среднего значения
        average: float = total / count
        return client_streaming_pb2.AverageResponse(average=average)


def serve() -> None:
    """
    Инициализирует и запускает gRPC сервер для обработки запросов к сервису AverageCalculator.

    Эта функция:
    1. Создает и настраивает gRPC сервер.
    2. Регистрирует реализацию сервиса AverageCalculatorServicer.
    3. Включает поддержку рефлексии для упрощения взаимодействия с сервисом.
    4. Запускает сервер и ожидает его завершения.

    Важно:
    - Сервер будет слушать входящие соединения на порту 50053.
    - Рефлексия позволяет клиентам запрашивать метаданные о сервисах и методах.
    """
    # Создание gRPC сервера с пулом потоков для обработки входящих запросов.
    # Пул потоков позволяет одновременно обрабатывать несколько запросов.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрация сервиса AverageCalculatorServicer на сервере.
    # Это связывает реализацию сервиса с сервером, чтобы он мог обрабатывать запросы к этому сервису.
    client_streaming_pb2_grpc.add_AverageCalculatorServicer_to_server(
        AverageCalculatorServicer(), server
    )

    # Определение списка имен сервисов, которые будут поддерживать рефлексию.
    # Включает имя зарегистрированного сервиса и имя встроенного сервиса рефлексии.
    SERVICE_NAMES = (
        # Имя зарегистрированного сервиса
        client_streaming_pb2.DESCRIPTOR.services_by_name['AverageCalculator'].full_name,
        reflection.SERVICE_NAME,
    )

    # Включение поддержки рефлексии на сервере.
    # Это позволяет клиентам запрашивать информацию о сервисах и методах на сервере.
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Настройка сервера на прослушивание входящих соединений на порту 50053.
    # '[::]:50053' означает, что сервер будет слушать на всех сетевых интерфейсах на этом порту.
    server.add_insecure_port('[::]:50053')

    # Запуск сервера. После запуска сервер начнет принимать и обрабатывать входящие запросы.
    server.start()

    print("Сервер клиентского потокового RPC запущен на порту 50053")

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

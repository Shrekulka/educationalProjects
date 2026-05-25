# unary_grpc_calculator/unary_server.py

import traceback
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

import unary_pb2
import unary_pb2_grpc
from logger_config import logger


class CalculatorServicer(unary_pb2_grpc.CalculatorServicer):
    """
    CalculatorServicer предоставляет реализацию сервиса Calculator, определенного в unary.proto.

    Этот класс реализует метод Calculate, который принимает два числа и тип операции,
    и возвращает результат выполнения математической операции или сообщение об ошибке.
    """

    def Calculate(self, request: unary_pb2.CalculationRequest,
                  context: grpc.ServicerContext) -> unary_pb2.CalculationResponse:
        """
        Реализация метода Calculate для выполнения математических операций.

        Args:
            request (unary_pb2.CalculationRequest): Запрос, содержащий два числа (num1, num2) и операцию (operation).
            context (grpc.ServicerContext): Контекст gRPC, который предоставляет метаинформацию о вызове.

        Returns:
            unary_pb2.CalculationResponse: Ответ, содержащий результат операции или сообщение об ошибке.
        """
        num1 = request.num1                                     # Получаем первое число из запроса.
        num2 = request.num2                                     # Получаем второе число из запроса.
        operation = request.operation                           # Получаем тип операции из запроса.

        # Используем оператор match для выбора операции на основе значения operation.
        match operation:
            case unary_pb2.Operation.ADD:                       # Если операция сложения
                result = num1 + num2                            # Выполняем сложение.
                error_message = ""                              # Сообщение об ошибке пустое.

            case unary_pb2.Operation.SUBTRACT:                  # Если операция вычитания
                result = num1 - num2                            # Выполняем вычитание.
                error_message = ""                              # Сообщение об ошибке пустое.

            case unary_pb2.Operation.MULTIPLY:                  # Если операция умножения
                result = num1 * num2                            # Выполняем умножение.
                error_message = ""                              # Сообщение об ошибке пустое.

            case unary_pb2.Operation.DIVIDE:                    # Если операция деления
                if num2 == 0:                                   # Проверяем деление на ноль.
                    result = 0                                  # Результат деления на ноль не определен, возвращаем 0.
                    error_message = "Ошибка: Деление на ноль!"  # Устанавливаем сообщение об ошибке.
                else:
                    result = num1 / num2                        # Выполняем деление.
                    error_message = ""                          # Сообщение об ошибке пустое.

            case _:                                             # Если операция не распознана
                result = 0                                      # Устанавливаем результат в 0.
                error_message = "Неверная операция!"            # Устанавливаем сообщение об ошибке.

        # Возвращаем результат выполнения операции или сообщение об ошибке в виде ответа.
        return unary_pb2.CalculationResponse(result=result, error_message=error_message)


def serve() -> None:
    """
    Инициализирует и запускает gRPC сервер для сервиса Calculator.

    Эта функция:
    1. Создает и настраивает gRPC сервер.
    2. Регистрирует реализацию сервиса CalculatorServicer.
    3. Включает поддержку рефлексии для динамического обнаружения доступных сервисов и их методов.
    4. Запускает сервер на порту 50051 и ожидает его завершения.

    Важно:
    - Сервер будет слушать входящие соединения на порту 50051.
    - Рефлексия позволяет клиентам запрашивать информацию о сервисах и методах на сервере,
      что упрощает взаимодействие с сервисом через инструменты для тестирования и отладки.
    """
    # Создание gRPC сервера с использованием пула потоков для обработки входящих запросов.
    # Пул потоков позволяет одновременно обрабатывать до 10 запросов.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрация реализации сервиса CalculatorServicer на сервере.
    # Это связывает ваш реализационный класс с сервером, чтобы он мог обрабатывать запросы к этому сервису.
    unary_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)

    # Определение списка имен сервисов, которые будут поддерживать рефлексию.
    # Включает имя зарегистрированного сервиса и имя встроенного сервиса рефлексии.
    SERVICE_NAMES = (
        unary_pb2.DESCRIPTOR.services_by_name['Calculator'].full_name,  # Полное имя зарегистрированного сервиса Calculator
        reflection.SERVICE_NAME,  # Имя встроенного сервиса рефлексии
    )

    # Включение поддержки рефлексии на сервере.
    # Это позволяет клиентам получать информацию о доступных сервисах и методах.
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Настройка сервера на прослушивание входящих соединений на порту 50051.
    # '[::]:50051' означает, что сервер будет слушать на всех сетевых интерфейсах на этом порту.
    server.add_insecure_port('[::]:50051')

    # Запуск сервера. После запуска сервер начнет принимать и обрабатывать входящие запросы.
    server.start()

    # Вывод сообщения в консоль о том, что сервер успешно запущен и слушает порт 50051.
    print("Сервер калькулятора запущен на порту 50051")

    # Ожидание завершения работы сервера. Функция блокирует выполнение текущего потока до тех пор,
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

# book_shop_grpc/recommendations.py
import random
import traceback
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from logger_config import logger
import recommendations_pb2 as pb2
import recommendations_pb2_grpc as pb2_grpc

books_by_category = {
    pb2.BookCategory.MYSTERY: [
        pb2.BookRecommendation(id=1, title="The Maltese Falcon"),
        pb2.BookRecommendation(id=2, title="Murder on the Orient Express"),
        pb2.BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],

    pb2.BookCategory.SCIENCE_FICTION: [
        pb2.BookRecommendation(
            id=4, title="The Hitchhiker's Guide to the Galaxy"
        ),
        pb2.BookRecommendation(id=5, title="Ender's Game"),
        pb2.BookRecommendation(id=6, title="The Dune Chronicles"),
    ],

    pb2.BookCategory.SELF_HELP: [
        pb2.BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),

        pb2.BookRecommendation(
            id=8, title="How to Win Friends and Influence People"
        ),

        pb2.BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}


class RecommendationService(pb2_grpc.RecommendationsServicer):

    # Метод 'Recommend' должен иметь то же имя, что и RPC, который мы определяем в своем файле Protobuf.
    # Параметр context позволяет установить код состояния для response.
    def Recommend(self, request, context):
        # Метод abort() для завершения запроса и устанавливается код состояния NOT_FOUND, если вы получаете
        # неожиданную категорию.
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]

        num_results = min(request.max_results, len(books_for_category))

        books_to_recommend = random.sample(books_for_category, num_results)

        # Возвращается RecommendationResponse со списком рекомендаций книг.
        return pb2_grpc.RecommendationResponse(recommendations=books_to_recommend)


def serve():
    # Создание gRPC сервера с использованием пула потоков для обработки входящих запросов.
    # Пул потоков позволяет одновременно обрабатывать до 10 запросов.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрация реализации сервиса RecommendationService на сервере.
    # Это связывает ваш реализационный класс с сервером, чтобы он мог обрабатывать запросы к этому сервису.
    pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)

    # Определение списка имен сервисов, которые будут поддерживать рефлексию.
    # Включает имя зарегистрированного сервиса и имя встроенного сервиса рефлексии.
    SERVICE_NAMES = (
        pb2.DESCRIPTOR.services_by_name['Recommendations'].full_name,
        # Полное имя зарегистрированного сервиса Recommendations
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
    print("Сервер рекомендаций запущен на порту 50051")

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


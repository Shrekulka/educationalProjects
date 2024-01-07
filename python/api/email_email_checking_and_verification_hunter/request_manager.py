# email_email_checking_and_verification_hunter/request_manager.py

# email_email_checking_and_verification_hunter/request_manager.py

import time
import requests


class RequestManager:
    """
    Класс RequestManager для управления HTTP-запросами в программе email_email_checking_and_verification_hunter.

    Методы:
        make_request(url: str, params: dict) -> requests.Response or dict:
            Выполняет GET-запрос по указанному URL с параметрами.

    """

    @staticmethod
    def make_request(url: str, params: dict) -> requests.Response or dict:
        """
        Выполняет GET-запрос по указанному URL с параметрами.

        Параметры:
            url (str): URL для выполнения запроса.
            params (dict): Параметры запроса.

        Возвращает:
            requests.Response or dict: Объект Response в случае успешного запроса,
            словарь с ключами 'error' и 'response' в случае ошибки.

        """
        try:
            # Выполняем GET-запрос по указанному URL с параметрами
            response = requests.get(url, params=params)

            # Проверяем статус код ответа, если не 200, вызываем исключение для обработки ошибки
            if response.status_code != 200:
                response.raise_for_status()

            time.sleep(0.15)  # Пауза между запросами для соблюдения лимитов

            return response   # Возвращаем успешный ответ

        except requests.exceptions.RequestException as error:
            # В случае исключения RequestException формируем словарь с ошибкой и объектом response (если есть)
            return {"error": str(error), "response": getattr(error, 'response', None)}


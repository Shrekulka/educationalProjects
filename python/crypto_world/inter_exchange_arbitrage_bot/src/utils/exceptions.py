# inter_exchange_arbitrage_bot/src/utils/exceptions.py
from typing import Optional


class APINotReadyError(Exception):
    """Исключение, которое выбрасывается, когда API еще не готово к приему запросов."""
    def __init__(self, message: str = "API инициализируется, пожалуйста, подождите.", progress_details: Optional[dict] = None):
        self.message = message
        # Формально объявляем атрибут в конструкторе класса
        self.progress_details = progress_details
        super().__init__(self.message)

class APIConnectionError(Exception):
    """Исключение для общих ошибок подключения к API."""
    def __init__(self, message: str = "Не удалось подключиться к серверу API.", progress_details: Optional[dict] = None):
        self.message = message
        self.progress_details = progress_details
        super().__init__(self.message)

class APIHealthCheckError(Exception):
    """Исключение для ошибок при проверке здоровья API."""
    pass

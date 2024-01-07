# email_email_checking_and_verification_hunter/local_storage_service.py

from logger import Logger


class LocalStorageService:
    """
    Класс LocalStorageService для управления локальным хранилищем результатов верификации в программе email_email_checking_and_verification_hunter.

    Методы:
        save_verification(key: str, result: dict) -> None:
            Сохраняет результат верификации в локальном хранилище.

        get_verification(key: str) -> dict or None:
            Получает результат верификации из локального хранилища.

    Атрибуты:
        verifications (dict): Словарь для хранения результатов верификации.
        logger (Logger): Логгер для записи событий.

    """

    def __init__(self):
        """
        Инициализирует объект LocalStorageService.

        """
        self.verifications = {}
        self.logger = Logger("LocalStorageService")

    def save_verification(self, key: str, result: dict) -> None:
        """
        Сохраняет результат верификации в локальном хранилище.

        Параметры:
            key (str): Ключ для идентификации результата верификации.
            result (dict): Результат верификации для сохранения.

        Возвращает:
            None

        """
        self.verifications[key] = result

    def get_verification(self, key: str) -> dict or None:
        """
        Получает результат верификации из локального хранилища.

        Параметры:
            key (str): Ключ для идентификации результата верификации.

        Возвращает:
            dict or None: Результат верификации, если найден, в противном случае None.

        """
        return self.verifications.get(key, None)

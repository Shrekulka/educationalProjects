# email_email_checking_and_verification_hunter/logger.py


import logging


class Logger:
    """
    Класс Logger для обработки логирования в программе email_email_checking_and_verification_hunter.

    Атрибуты:
        logger (logging.Logger): Экземпляр логгера.

    Методы:
        __init__(self, name: str) -> None:
            Инициализирует Logger с указанным именем.

        debug(self, msg: str) -> None:
            Записывает сообщение с уровнем DEBUG.

        info(self, msg: str) -> None:
            Записывает сообщение с уровнем INFO.

        warning(self, msg: str) -> None:
            Записывает сообщение с уровнем WARNING.

    """

    def __init__(self, name: str) -> None:
        """
        Инициализирует Logger с указанным именем.

        Параметры:
            name (str): Имя, которое будет ассоциировано с логгером.

        Возвращает:
            None

        """
        # Создание логгера с указанным именем
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Создание обработчиков для вывода в консоль и в файл
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('app.log')

        # Установка формата вывода
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Добавление обработчиков к логгеру
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, msg: str) -> None:
        """
        Записывает сообщение с уровнем DEBUG.

        Параметры:
            msg (str): Сообщение для записи.

        Возвращает:
            None

        """
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """
        Записывает сообщение с уровнем INFO.

        Параметры:
            msg (str): Сообщение для записи.

        Возвращает:
            None

        """
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """
        Записывает сообщение с уровнем WARNING.

        Параметры:
            msg (str): Сообщение для записи.

        Возвращает:
            None

        """
        self.logger.warning(msg)

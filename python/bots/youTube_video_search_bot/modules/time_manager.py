import datetime


class TimeManager:
    """Класс TimeManager для управления временем.

    Этот класс содержит статический метод is_within_time_range(), который используется для проверки,
    находится ли текущее время в разрешенном временном диапазоне.

    Атрибуты:
        Нет атрибутов.

    Методы:
        is_within_time_range(): Возвращает True, если текущее время находится в разрешенном диапазоне,
                               иначе возвращает False.
    """

    @staticmethod
    def is_within_time_range() -> bool:
        """Проверяет, находится ли текущее время в разрешенном временном диапазоне.

        Возвращает:
            bool: True, если текущее время находится в разрешенном диапазоне (с 7 утра до 10 вечера),
                  иначе False.
        """

        # Получаем текущий час из объекта datetime.datetime
        current_hour = datetime.datetime.now().hour

        # Проверяем, находится ли текущий час в разрешенном диапазоне (от 7 до 21)
        return 7 <= current_hour < 22
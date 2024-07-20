# zodiac_portal/horoscope/apps.py

from django.apps import AppConfig


class HoroscopeConfig(AppConfig):
    """
       Конфигурационный класс для приложения 'Horoscope'.

       Этот класс настраивает приложение 'Horoscope' и предоставляет метаданные,
       такие как название и человекочитаемое имя.

       Атрибуты:
           default_auto_field (str): Тип поля по умолчанию для автоинкрементных полей модели.
           name (str): Полное имя приложения, используемое внутри папки 'modules'.
           verbose_name (str): Человекочитаемое имя приложения на русском языке.
    """
    # Устанавливаем тип поля по умолчанию для автоинкрементных полей.
    default_auto_field = 'django.db.models.BigAutoField'

    # Полное имя приложения, указывающее на его расположение в папке 'modules'.
    name = 'horoscope'

    # Человекочитаемое имя приложения на русском языке.
    verbose_name = 'Гороскоп'

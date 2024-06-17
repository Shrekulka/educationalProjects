# backend/modules/system/apps.py

from django.apps import AppConfig


class SystemConfig(AppConfig):
    """
        Конфигурационный класс для приложения 'System'.

        Этот класс настраивает приложение 'System' и предоставляет метаданные,
        такие как название и человекочитаемое имя.

        Атрибуты:
            default_auto_field (str): Тип поля по умолчанию для автоинкрементных полей модели.
            name (str): Полное имя приложения, используемое внутри папки 'modules'.
            verbose_name (str): Человекочитаемое имя приложения на русском языке.
    """
    # Устанавливаем тип поля по умолчанию для автоинкрементных полей.
    default_auto_field = 'django.db.models.BigAutoField'

    # Полное имя приложения, указывающее на его расположение в папке 'modules'.
    name = 'modules.system'

    # Человекочитаемое имя приложения на русском языке.
    verbose_name = 'Система'

# restful_text_processing_with_nltk/src/nlp/utils.py

import traceback

import nltk

from src.logger_config import logger


def download_nltk_resources() -> None:
    """
        Загружает необходимые ресурсы NLTK для работы с текстом.

        Функция загружает следующие NLTK пакеты:
        - 'punkt': для токенизации текста.
        - 'averaged_perceptron_tagger': для частеречной разметки текста.
        - 'maxent_ne_chunker': для распознавания именованных сущностей.
        - 'words': словарь слов для поддержки других моделей и компонент NLTK.

        Логирует любые ошибки, возникающие при загрузке ресурсов NLTK.

        Примечание:
        Функция не возвращает значений. Она выполняет загрузку ресурсов при каждом вызове.

        Raises:
            Exception: Если происходит ошибка при загрузке любого из ресурсов, ошибка логируется с помощью модуля logger.
    """
    # Загрузка необходимых ресурсов NLTK для работы с текстом
    try:
        nltk.download('punkt')  # Загрузка пакета для токенизации
        nltk.download('averaged_perceptron_tagger')  # Загрузка пакета для частеречной разметки
        nltk.download('maxent_ne_chunker')  # Загрузка пакета для распознавания именованных сущностей
        nltk.download('words')  # Загрузка словаря слов для поддержки других моделей
    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Error downloading NLTK resources: {e}\n{detailed_error_message}")


# Вызов этой функции при запуске приложения, чтобы загрузить все необходимые ресурсы
download_nltk_resources()

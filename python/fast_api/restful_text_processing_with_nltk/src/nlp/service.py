# restful_text_processing_with_nltk/src/nlp/service.py

import asyncio

from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

from src.logger_config import logger


async def tokenize_text(text: str) -> list[str]:
    """
        Асинхронно токенизирует входной текст.

        Args:
            text (str): Входной текст для токенизации.

        Returns:
            list[str]: Список токенов.
    """
    logger.debug(f"Начало токенизации текста длиной {len(text)} символов")

    # Асинхронно запускаем функцию word_tokenize из библиотеки NLTK в отдельном потоке с помощью asyncio.to_thread.
    # Эта функция возвращает список токенов (слов и пунктуации).
    tokens = await asyncio.to_thread(word_tokenize, text)

    logger.debug(f"Токенизация завершена. Получено {len(tokens)} токенов")

    # Возвращаем список токенов
    return tokens


async def pos_tag_text(text: str) -> list[tuple[str, str]]:
    """
        Асинхронно выполняет частеречную разметку входного текста.

        Args:
            text (str): Входной текст для разметки.

        Returns:
            list[tuple[str, str]]: Список пар (токен, тег).
    """
    logger.debug(f"Начало частеречной разметки текста длиной {len(text)} символов")

    # Асинхронно токенизируем входной текст с помощью функции tokenize_text
    tokens = await tokenize_text(text)

    # Асинхронно запускаем частеречную разметку на полученных токенах
    tagged = await asyncio.to_thread(pos_tag, tokens)

    logger.debug(f"Частеречная разметка завершена. Получено {len(tagged)} тегов")

    # Возвращаем список пар (токен, тег)
    return tagged


async def ner_text(text: str) -> list[tuple[str, str]]:
    """
        Асинхронно выполняет распознавание именованных сущностей во входном тексте.

        Args:
            text (str): Входной текст для распознавания сущностей.

        Returns:
            list[tuple[str, str]]: Список пар (сущность, тип).
    """
    logger.debug(f"Начало распознавания именованных сущностей в тексте длиной {len(text)} символов")

    # Асинхронно токенизируем входной текст с помощью функции tokenize_text
    tokens = await tokenize_text(text)

    # Асинхронно выполняем частеречную разметку на полученных токенах
    pos_tags = await asyncio.to_thread(pos_tag, tokens)

    # Асинхронно выполняем распознавание именованных сущностей на размеченных данных
    ne_tree = await asyncio.to_thread(ne_chunk, pos_tags)

    # Формируем список именованных сущностей, убирая сущности с меткой 'O'
    entities = [(entity[0], entity[1]) for entity in tree2conlltags(ne_tree) if entity[2] != 'O']

    logger.debug(f"Распознавание именованных сущностей завершено. Найдено {len(entities)} сущностей")

    # Возвращаем список пар (сущность, тип)
    return entities

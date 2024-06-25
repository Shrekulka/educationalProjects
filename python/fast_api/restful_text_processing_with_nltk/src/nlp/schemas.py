# restful_text_processing_with_nltk/src/nlp/schemas.py

from typing import Tuple, List

from pydantic import BaseModel, constr


class TextInput(BaseModel):
    """
        Модель для входного текста.

        Attributes:
            text (str): Текст для обработки. Длина текста должна быть от 1 до 1000 символов.
    """
    # Поле text типа str с ограничением длины текста
    text: constr(min_length=1, max_length=1000)


class TokenizeResponse(BaseModel):
    """
        Модель для ответа на запрос токенизации.

        Attributes:
            tokens (List[str]): Список токенов (слов), полученных из текста.
    """
    # Список токенов
    tokens: List[str]


class POSTagResponse(BaseModel):
    """
        Модель для ответа на запрос частеречной разметки.

        Attributes:
            pos_tags (List[Tuple[str, str]]): Список кортежей, где каждый кортеж содержит токен и его часть речи.
    """
    # Список токенов с их частями речи
    pos_tags: List[Tuple[str, str]]


class NERResponse(BaseModel):
    """
        Модель для ответа на запрос распознавания именованных сущностей.

        Attributes:
            entities (List[Tuple[str, str]]): Список кортежей, где каждый кортеж содержит сущность и её тип.
    """
    # Список именованных сущностей с их типами
    entities: List[Tuple[str, str]]

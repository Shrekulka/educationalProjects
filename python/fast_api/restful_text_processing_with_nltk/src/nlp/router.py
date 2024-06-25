# restful_text_processing_with_nltk/src/nlp/router.py

from fastapi import APIRouter, HTTPException
from src.nlp.schemas import TextInput, TokenizeResponse, POSTagResponse, NERResponse
from src.nlp.service import tokenize_text, pos_tag_text, ner_text

# Создаем экземпляр APIRouter для объявления маршрутов
router = APIRouter()


@router.post("/tokenize", response_model=TokenizeResponse)
async def tokenize(text_input: TextInput) -> TokenizeResponse:
    """
        Обработчик POST-запроса для API endpoint /tokenize.
        Принимает входные данные text_input типа TextInput, содержащие текст для токенизации.
        Возвращает объект TokenizeResponse с токенами, полученными из текста.

        Args:
            text_input (TextInput): Входные данные для токенизации, содержащие текст.

        Returns:
            TokenizeResponse: Объект, содержащий список токенов.

        Raises:
            HTTPException: Если возникает ошибка при обработке запроса.
    """
    try:
        # Вызываем функцию tokenize_text для выполнения токенизации асинхронно
        tokens = await tokenize_text(text_input.text)

        # Возвращаем объект TokenizeResponse с полученными токенами
        return TokenizeResponse(tokens=tokens)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pos_tag", response_model=POSTagResponse)
async def pos_tag(text_input: TextInput) -> POSTagResponse:
    """
        Обработчик POST-запроса для API endpoint /pos_tag.
        Принимает входные данные text_input типа TextInput, содержащие текст для частеречной разметки.
        Возвращает объект POSTagResponse с кортежами (токен, часть речи), полученными из текста.

        Args:
            text_input (TextInput): Входные данные для частеречной разметки, содержащие текст.

        Returns:
            POSTagResponse: Объект, содержащий список кортежей (токен, часть речи).

        Raises:
            HTTPException: Если возникает ошибка при обработке запроса.
    """
    try:
        # Вызываем функцию pos_tag_text для выполнения частеречной разметки асинхронно
        pos_tags = await pos_tag_text(text_input.text)

        # Возвращаем объект POSTagResponse с полученными кортежами (токен, часть речи)
        return POSTagResponse(pos_tags=pos_tags)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ner", response_model=NERResponse)
async def ner(text_input: TextInput) -> NERResponse:
    """
        Обработчик POST-запроса для API endpoint /ner.
        Принимает входные данные text_input типа TextInput, содержащие текст для распознавания сущностей.
        Возвращает объект NERResponse с именованными сущностями и их типами, полученными из текста.

        Args:
            text_input (TextInput): Входные данные для распознавания сущностей, содержащие текст.

        Returns:
            NERResponse: Объект, содержащий список кортежей (сущность, тип).

        Raises:
            HTTPException: Если возникает ошибка при обработке запроса.
    """
    try:
        # Вызываем функцию ner_text для выполнения распознавания сущностей асинхронно
        entities = await ner_text(text_input.text)

        # Возвращаем объект NERResponse с полученными именованными сущностями и их типами
        return NERResponse(entities=entities)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

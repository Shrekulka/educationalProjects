# web_crawler_ads_generator/summary_generator.py


import os
import traceback

from openai import AsyncOpenAI

from config import GPT_MODEL, MAX_TOKENS
from logger_config import logger


async def generate_summary(pages: list) -> str:
    """
        Асинхронно генерирует краткое описание сайта на основе HTML-контента страниц с помощью модели GPT.

        Args:
            pages (list): Список словарей, каждый из которых содержит ключи 'html' (строка HTML-контента страницы).

        Returns:
            str: Краткое описание сайта, сгенерированное на основе объединенного HTML-контента всех страниц.
                 В случае ошибки возвращает пустую строку.
    """
    try:
        logger.debug("########## generate_summary function works! ##########")

        if not pages:
            # Проверяем, если список страниц пуст, то возвращаем пустую строку, так как нет страниц для обработки
            logger.warning("Список страниц пуст. Прекращение работы generate_summary.")
            return ""

        # Объединяем HTML-контент всех страниц
        all_html = ' '.join([page['html'] for page in pages])

        # Создаем клиент OpenAI
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Запрашиваем у OpenAI генерацию краткого описания сайта на основе предоставленного HTML-контента
        response = await client.completions.create(
            # Используем модель GPT для генерации текста
            model=GPT_MODEL,
            # Передаем HTML-контент для генерации описания
            prompt=f"Создайте краткое описание сайта на основе следующего HTML-контента: {all_html[:1000]}...",
            # Устанавливаем максимальное количество токенов для генерации описания
            max_tokens=MAX_TOKENS
        )
        # Извлекаем текст сгенерированного описания, если оно доступно, иначе оставляем строку пустой
        summary = response.choices[0].text.strip() if response.choices else ""

        logger.debug(f"Создана сводка: {summary}")

        logger.debug("########## Завершение работы функции generate_summary ##########")

        # Возвращаем сгенерированное краткое описание сайта
        return summary

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла ошибка при создании сводки: {e}\n{detailed_error_message}")
        return ""


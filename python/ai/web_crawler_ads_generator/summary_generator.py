# web_crawler_ads_generator/summary_generator.py
import os
import traceback

from openai import AsyncOpenAI

from logger_config import logger


async def generate_summary(pages):
    try:
        if not pages:
            logger.warning("Список страниц пуст. Прекращение работы generate_summary.")
            return ""

        logger.debug("########## generate_summary function works! ##########")

        # Объединяем HTML-контент всех страниц
        all_html = ' '.join([page['html'] for page in pages])

        # Создаем клиент OpenAI
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Генерируем краткое описание с помощью GPT
        response = await client.completions.create(
            model="gpt-3.5-turbo",
            prompt=f"Создайте краткое описание сайта на основе следующего HTML-контента: {all_html[:1000]}...",
            max_tokens=200
        )

        summary = response.choices[0].text.strip() if response.choices else ""
        logger.debug(f"Создана сводка: {summary}")

        logger.debug("########## Завершение работы функции generate_summary ##########")
        return summary

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла ошибка при создании сводки: {e}\n{detailed_error_message}")
        return ""

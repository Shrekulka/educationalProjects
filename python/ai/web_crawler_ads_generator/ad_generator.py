# web_crawler_ads_generator/ad_generator.py

import asyncio
import traceback
from typing import Dict, Union

import openai
from bs4 import BeautifulSoup
from openai import AsyncOpenAI

from config import RETRY_ATTEMPTS, RETRY_DELAY_SECONDS, GPT_MODEL, DEFAULT_AD_LENGTH
from logger_config import logger


def extract_meta_tags(html: str) -> Dict[str, Union[str, None]]:
    """
        Извлекает мета-теги из HTML-страницы.

        Args:
            html (str): Строка с HTML-кодом страницы.

        Returns:
            dict: Словарь с извлеченными мета-тегами, где ключи - атрибуты 'name' или 'property',
                  значения - содержимое 'content' мета-тега. Если мета-тегов нет, возвращается пустой словарь.

        Raises:
            Exception: Если происходит ошибка при парсинге HTML или извлечении мета-тегов, логируется сообщение об ошибке.
    """
    try:
        logger.debug("########## extract_meta_tags function works! ##########")

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Инициализация пустого словаря для хранения мета-тегов
        meta_tags = {}

        # Итерируемся по всем тегам <meta> и извлекаем атрибуты 'name' или 'property' и их содержимое 'content'
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            if name:
                meta_tags[name] = meta.get('content')

        logger.debug(f"Extracted meta tags: {meta_tags}")

        # Возвращаем словарь с мета-тегами
        return meta_tags

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(
            f"Error occurred while extracting meta tags: {e}\n{detailed_error_message}")
        return {}


async def generate_ads(pages: list, client: AsyncOpenAI, ad_length: int = DEFAULT_AD_LENGTH,
                       keywords: list = None) -> list:
    """
        Асинхронная функция для генерации рекламных объявлений на основе содержимого веб-страниц.

        Args:
            pages (list): Список словарей, каждый из которых представляет страницу с ключами 'url' и другими данными.
            client (AsyncOpenAI): Асинхронный клиент OpenAI для взаимодействия с API.
            ad_length (int, optional): Максимальная длина генерируемого объявления (по умолчанию DEFAULT_AD_LENGTH).
            keywords (list, optional): Список ключевых слов для генерации объявления (по умолчанию None).

        Returns:
            list: Список словарей с сгенерированными объявлениями. Каждое объявление содержит ключи 'url' и 'ad_text'.

        Raises:
            Exception: В случае любой ошибки при генерации объявлений.
    """
    try:
        logger.debug("########## generate_ads function works! ##########")

        # Возвращаем пустой список, так как нет страниц для обработки
        if not pages:
            logger.warning("Pages list is empty. Terminating generate_ads.")
            return []

        # Инициализируем список для хранения сгенерированных объявлений
        ads = []

        # Формируем текст запроса для генерации объявления на основе описания веб-страницы и ключевых слов
        for page in pages:
            prompt = f"Based on this website description, create an ad no longer than {ad_length} characters"
            if keywords:
                prompt += f" using the following keywords: {', '.join(keywords)}"
            prompt += f" for the page: {page['url']}"

            # Перебираем попытки отправки запроса в цикле, заданном количеством RETRY_ATTEMPTS
            for attempt in range(RETRY_ATTEMPTS):
                try:
                    # Пытаемся отправить запрос на генерацию объявления с использованием модели
                    response = await client.completions.create(
                        model=GPT_MODEL,  # Указываем модель GPT для генерации текста
                        prompt=prompt,  # Передаем текст-подсказку для генерации объявления
                        max_tokens=ad_length  # Ограничиваем количество символов в сгенерированном объявлении
                    )

                    # Извлекаем сгенерированный текст объявления из ответа
                    ad_text = response.choices[0].text.strip() if response.choices else ""

                    # Добавляем сгенерированное объявление в список ads в формате {'url': URL_страницы, 'ad_text':
                    # сгенерированный текст}
                    ads.append({
                        'url': page['url'],
                        'ad_text': ad_text
                    })

                    logger.debug(f"Generated ad for URL {page['url']}: {ad_text}")

                    # Добавляем задержку между запросами
                    await asyncio.sleep(RETRY_DELAY_SECONDS)

                    # Выходим из цикла попыток при успешной генерации объявления
                    break

                except openai.RateLimitError as err:
                    # Проверяем, не достигнут ли лимит попыток (RETRY_ATTEMPTS)
                    if attempt < RETRY_ATTEMPTS - 1:
                        logger.warning(f"Attempt {attempt + 1} of {RETRY_ATTEMPTS}: "
                                       f"RateLimitError occurred. Retrying after a few seconds.")

                        # Увеличиваем время ожидания перед следующей попыткой
                        await asyncio.sleep(RETRY_DELAY_SECONDS)
                    else:
                        logger.error(f"Exceeded retry limit for URL {page['url']}. Error: {err}")
                        raise

        logger.debug("########## generate_ads function finished ##########")

        # Возвращаем список сгенерированных объявлений
        return ads

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Error occurred while generating ads: {e}\n{detailed_error_message}")
        return []

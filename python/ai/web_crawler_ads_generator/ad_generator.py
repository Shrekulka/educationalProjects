# web_crawler_ads_generator/ad_generator.py

import asyncio
import traceback

import openai
from bs4 import BeautifulSoup

from logger_config import logger


# Функция для извлечения мета-тегов из HTML
def extract_meta_tags(html):
    try:
        logger.debug("########## extract_meta_tags function works! ##########")  # Записываем отладочное сообщение
        soup = BeautifulSoup(html, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML
        meta_tags = {}
        # Итерируемся по всем тегам <meta> и извлекаем их атрибуты name или property и content
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            if name:
                meta_tags[name] = meta.get('content')
        logger.debug(f"Extracted meta tags: {meta_tags}")  # Записываем извлеченные мета-теги в лог
        return meta_tags  # Возвращаем словарь с мета-тегами

    except Exception as e:
        detailed_error_message = traceback.format_exc()  # Получаем подробное сообщение об ошибке
        logger.error(
            f"Error occurred while extracting meta tags: {e}\n{detailed_error_message}")  # Записываем ошибку в лог
        return {}  # Возвращаем пустой словарь в случае ошибки


# Асинхронная функция для генерации рекламных объявлений на основе содержимого веб-страниц
async def generate_ads(pages, client, ad_length=50, keywords=None):
    try:
        logger.debug("########## generate_ads function works! ##########")  # Записываем отладочное сообщение

        if not pages:
            logger.warning("Pages list is empty. Terminating generate_ads.")  # Предупреждаем, если список страниц пуст
            return []  # Возвращаем пустой список объявлений

        ads = []  # Инициализируем список для хранения сгенерированных объявлений
        for page in pages:
            prompt = f"Based on this website description, create an ad no longer than {ad_length} characters"
            if keywords:
                prompt += f" using the following keywords: {', '.join(keywords)}"
            prompt += f" for the page: {page['url']}"

            retry_attempts = 5  # Максимальное количество попыток повтора запроса
            for attempt in range(retry_attempts):
                try:
                    response = await client.completions.create(
                        model="gpt-3.5-turbo",  # Используем модель GPT-3.5 Turbo для генерации текста
                        prompt=prompt,
                        max_tokens=ad_length  # Ограничиваем количество символов в объявлении
                    )
                    ad_text = response.choices[0].text.strip() if response.choices else ""
                    ads.append({
                        'url': page['url'],
                        'ad_text': ad_text
                    })
                    logger.debug(
                        f"Generated ad for URL {page['url']}: {ad_text}")  # Записываем сгенерированное объявление в лог
                    await asyncio.sleep(5)  # Добавляем задержку между запросами
                    break  # Выходим из цикла попыток при успешной генерации объявления

                except openai.RateLimitError as err:
                    if attempt < retry_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} of {retry_attempts}: RateLimitError occurred. Retrying after a few seconds.")
                        await asyncio.sleep(10)  # Увеличиваем время ожидания перед следующей попыткой
                    else:
                        logger.error(f"Exceeded retry limit for URL {page['url']}. Error: {err}")
                        raise  # Передаем ошибку дальше при достижении лимита попыток

        logger.debug("########## generate_ads function finished ##########")  # Записываем завершающее сообщение в лог
        return ads  # Возвращаем список сгенерированных объявлений

    except Exception as e:
        detailed_error_message = traceback.format_exc()  # Получаем подробное сообщение об ошибке
        logger.error(f"Error occurred while generating ads: {e}\n{detailed_error_message}")  # Записываем ошибку в лог
        return []  # Возвращаем пустой список в случае ошибки
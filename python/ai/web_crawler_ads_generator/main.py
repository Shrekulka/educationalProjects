# web_crawler_ads_generator/main.py

import asyncio
import os
import traceback

from dotenv import load_dotenv
from openai import AsyncOpenAI

from ad_generator import generate_ads
from crawler import crawl_site_async
from csv_writer import write_csv
from logger_config import logger
from summary_generator import generate_summary
from utils import parse_arguments


async def main():
    try:
        logger.debug("########## main function works! ##########")
        load_dotenv()

        args = parse_arguments()
        site_url = args.url
        max_pages = args.max_pages
        depth = args.depth
        ad_length = args.ad_length
        keywords = args.keywords

        logger.debug(f"URL сайта: {site_url}")
        logger.debug(f"Максимальна кількість сторінок: {max_pages}")
        logger.debug(f"Глибина краулінгу: {depth}")
        logger.debug(f"Максимальная длина объявления: {ad_length}")
        logger.debug(f"Ключевые слова: {keywords}")

        pages = await crawl_site_async(site_url, max_pages=max_pages, depth=depth)
        logger.debug(f"Количество собранных страниц: {len(pages)}")

        pages = list(pages)

        summary = await generate_summary(pages)
        logger.debug(f"Сгенерированное краткое описание: {summary}")

        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        ads = await generate_ads(pages, client, ad_length=ad_length, keywords=keywords)
        logger.debug(f"Количество сгенерированных объявлений: {len(ads)}")

        write_csv(ads, 'ads.csv')
        logger.debug("Запись в файл 'ads.csv' выполнена успешно")

        logger.debug("########## Terminating the crawl_site function ##########")

    except ValueError as e:
        logger.error(f"Помилка валідації URL: {e}")
    except Exception as error:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла неожиданная ошибка в приложении: {error}\n{detailed_error_message}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Application terminated by the user")
    except Exception as error:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Unexpected error in the application: {error}\n{detailed_send_message_error}")

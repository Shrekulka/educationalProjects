# web_crawler_ads_generator/crawler.py

import asyncio
import ssl
import traceback
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import certifi
import cloudscraper
import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError, RequestException

from checkpoint import save_checkpoint, load_checkpoint, clear_checkpoint
from config import DEFAULT_MAX_PAGES, DEFAULT_DEPTH, CRAWL_DELAY_SECONDS, SCRAPER_DELAY
from logger_config import logger


def can_fetch(url: str) -> bool:
    """
        Проверяет разрешено ли получение ресурса (URL) согласно файлу robots.txt.

        Args:
            url (str): URL для проверки.

        Returns:
            bool: True, если ресурс разрешен для получения согласно robots.txt, иначе False.
    """
    try:
        # Создаем объект для парсинга файла robots.txt
        rp = RobotFileParser()

        # Формируем URL для файла robots.txt
        robots_url = urljoin(url, "/robots.txt")

        # Устанавливаем URL файла robots.txt
        rp.set_url(robots_url)

        # Отключаем проверку SSL для запроса
        response = requests.get(robots_url, verify=False)

        # Парсим содержимое файла robots.txt
        rp.parse(response.text.splitlines())

        # Возвращаем результат проверки доступа к URL согласно robots.txt
        return rp.can_fetch("*", url)

    except SSLError:
        logger.warning(f"SSL ошибка при получении файла robots.txt для {url}. Продолжаем с осторожностью.")
        # Возвращаем True, чтобы показать, что можно продолжить выполнение операции
        return True

    except RequestException as e:
        logger.error(f"Ошибка при получении файла robots.txt для {url}: {e}")
        return False

    except Exception as e:
        logger.error(f"Неожиданная ошибка при проверке robots.txt для {url}: {e}")
        return False


async def crawl_site_async(site_url: str, max_pages: int = DEFAULT_MAX_PAGES, depth: int = DEFAULT_DEPTH) -> list:
    """
        Асинхронно краулит веб-сайт до заданной глубины и максимального количества страниц.

        Args:
            site_url (str): URL сайта для краулинга.
            max_pages (int): Максимальное количество страниц для сбора. По умолчанию DEFAULT_MAX_PAGES.
            depth (int): Максимальная глубина краулинга. По умолчанию DEFAULT_DEPTH.

        Returns:
            list: Список словарей, каждый словарь представляет собой страницу с ключами 'url' и 'html'.

        Raises:
            Exception: В случае любой неожиданной ошибки при краулинге.
    """
    try:
        logger.debug("########## crawl_site_async function works! ##########")

        # Загружаем сохраненное состояние краулинга (если есть)
        checkpoint = load_checkpoint()

        # Загружаем сохраненную контрольную точку, если она существует, иначе инициализируем пустым списком
        pages = checkpoint if checkpoint else []

        # Если контрольная точка существует, начинаем краулинг сначала URL из контрольной точки,
        # иначе начинаем с основного URL сайта с глубиной 0
        urls_to_crawl = [(site_url, 0)] if not checkpoint else []

        # Создаем множество для хранения URL, которые уже были обработаны (краулинг завершен)
        crawled_urls = set(page['url'] for page in pages)

        # Создаем экземпляр скрейпера для обхода защиты Cloudflare с настройками:
        # - задержка в секундах между запросами, указана в SCRAPER_DELAY,
        # - использованием браузера Chrome (эмуляция),
        # - SSL-контекстом по умолчанию с корневыми сертификатами, определенными в certifi
        scraper = cloudscraper.create_scraper(
            delay=SCRAPER_DELAY,
            browser='chrome',
            ssl_context=ssl.create_default_context(cafile=certifi.where())
        )

        # Основной цикл краулинга: продолжаем краулинг, пока есть ссылки для обработки и не достигнуто максимальное
        # число страниц
        while urls_to_crawl and len(pages) < max_pages:
            url, current_depth = urls_to_crawl.pop(0)

            # Проверяем, что URL еще не был обработан и не превышена максимальная глубина
            if url not in crawled_urls and current_depth <= depth:
                # Проверяем разрешение на получение URL согласно файлу robots.txt
                if can_fetch(url):
                    try:
                        # Получаем HTML страницы
                        response = scraper.get(url)
                        html = response.text

                        # Добавляем страницу в список pages
                        pages.append({'url': url, 'html': html})
                        logger.debug(f"Добавлена страница: {url}")

                        # Добавляем URL в множество обработанных
                        crawled_urls.add(url)
                        logger.debug(f"Добавлен URL {url} в множество обработанных")

                        # Если текущая глубина меньше максимальной, ищем новые ссылки на странице
                        if current_depth < depth:
                            soup = BeautifulSoup(html, 'html.parser')
                            for link in soup.find_all('a', href=True):
                                new_url = urljoin(site_url, link['href'])
                                # Проверяем условия для добавления новой ссылки в urls_to_crawl
                                if (new_url.startswith(site_url)
                                        and new_url not in crawled_urls
                                        and new_url not in [u[0] for u in urls_to_crawl]):
                                    urls_to_crawl.append((new_url, current_depth + 1))
                                    logger.debug(f"Найдена новая ссылка для обработки: {new_url}")

                        # Сохраняем контрольную точку после успешного добавления страницы
                        save_checkpoint(pages)

                        # Добавляем задержку между запросами
                        await asyncio.sleep(CRAWL_DELAY_SECONDS)

                    except cloudscraper.exceptions.CloudflareChallengeError as e:
                        detailed_error_message = traceback.format_exc()
                        logger.error(f"Ошибка вызова Cloudflare для {url}: {e}\n{detailed_error_message}")

                    except requests.exceptions.SSLError as e:
                        detailed_error_message = traceback.format_exc()
                        logger.error(f"SSL ошибка для {url}: {e}\n{detailed_error_message}")

                    except Exception as e:
                        detailed_error_message = traceback.format_exc()
                        logger.error(f"Ошибка при получении страницы {url}: {e}\n{detailed_error_message}")
                else:
                    logger.warning(f"Доступ к {url} запрещен по файлу robots.txt")

        logger.debug("########## Завершение работы функции crawl_site_async ##########")

        # Очищаем контрольную точку после успешного завершения краулинга
        clear_checkpoint()

        # Возвращаем список собранных страниц
        return pages

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла ошибка при асинхронном краулинге сайта: {e}\n{detailed_error_message}")
        return []

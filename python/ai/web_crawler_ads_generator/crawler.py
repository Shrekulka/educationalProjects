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

from checkpoint import save_checkpoint, load_checkpoint, clear_checkpoint
from logger_config import logger


def can_fetch(url):
    try:
        rp = RobotFileParser()
        robots_url = urljoin(url, "/robots.txt")
        rp.set_url(robots_url)

        response = requests.get(robots_url, verify=False)  # Отключаем проверку SSL
        rp.parse(response.text.splitlines())

        return rp.can_fetch("*", url)
    except requests.exceptions.SSLError:
        logger.warning(f"SSL error when fetching robots.txt for {url}. Proceeding with caution.")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching robots.txt for {url}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking robots.txt for {url}: {e}")
        return False


async def crawl_site_async(site_url, max_pages=10, depth=3):
    try:
        logger.debug("########## crawl_site_async function works! ##########")
        checkpoint = load_checkpoint()
        pages = checkpoint if checkpoint else []
        urls_to_crawl = [(site_url, 0)] if not checkpoint else []
        crawled_urls = set(page['url'] for page in pages)

        scraper = cloudscraper.create_scraper(delay=10, browser='chrome', ssl_context=ssl.create_default_context(cafile=certifi.where()))
        while urls_to_crawl and len(pages) < max_pages:
            url, current_depth = urls_to_crawl.pop(0)

            if url not in crawled_urls and current_depth <= depth:
                if can_fetch(url):
                    try:
                        response = scraper.get(url)
                        html = response.text

                        pages.append({'url': url, 'html': html})
                        logger.debug(f"Добавлена страница: {url}")

                        crawled_urls.add(url)
                        logger.debug(f"Добавлен URL {url} в множество обработанных")

                        if current_depth < depth:
                            soup = BeautifulSoup(html, 'html.parser')
                            for link in soup.find_all('a', href=True):
                                new_url = urljoin(site_url, link['href'])
                                if new_url.startswith(site_url) and new_url not in crawled_urls and new_url not in [u[0]
                                                                                                                    for
                                                                                                                    u in
                                                                                                                    urls_to_crawl]:
                                    urls_to_crawl.append((new_url, current_depth + 1))
                                    logger.debug(f"Найдена новая ссылка для обработки: {new_url}")

                        save_checkpoint(pages)
                        await asyncio.sleep(3)  # Добавляем небольшую задержку между запросами

                    except cloudscraper.exceptions.CloudflareChallengeError as e:
                        logger.error(f"Cloudflare challenge error for {url}: {e}")
                    except requests.exceptions.SSLError as e:
                        logger.error(f"SSL error for {url}: {e}")
                    except Exception as e:
                        logger.error(f"Ошибка при получении страницы {url}: {e}")
                else:
                    logger.warning(f"Доступ к {url} запрещен robots.txt")

        logger.debug("########## Завершение работы функции crawl_site_async ##########")
        clear_checkpoint()  # Очищаем контрольную точку после успешного завершения
        return pages

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла ошибка при асинхронном краулинге сайта: {e}\n{detailed_error_message}")
        return []

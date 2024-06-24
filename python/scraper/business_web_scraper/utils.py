# business_web_scraper/utils.py

import argparse
from typing import Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_URL, DEFAULT_OUTPUT_FILE
from logger_config import logger


def parse_arguments() -> argparse.Namespace:
    """
        Парсит аргументы командной строки для веб-скрапера.

        Returns:
            argparse.Namespace: Пространство имен с аргументами командной строки.
    """
    # Создание парсера аргументов командной строки с описанием
    parser = argparse.ArgumentParser(description='Web scraper for OLX business ads')

    # Добавление аргумента для URL категории бизнеса (по умолчанию DEFAULT_URL)
    parser.add_argument('--url', default=DEFAULT_URL, help='URL of the business category')

    # Добавление аргумента для пути выходного файла (по умолчанию DEFAULT_OUTPUT_FILE)
    parser.add_argument('--output', default=DEFAULT_OUTPUT_FILE, help='Output file path')

    # Парсинг аргументов командной строки и возврат Namespace с аргументами
    return parser.parse_args()


def accept_cookies(driver: WebDriver) -> None:
    """
        Принимает cookie-уведомление на веб-странице, если оно присутствует.

        Args:
            driver (WebDriver): Веб-драйвер для взаимодействия с браузером.
    """
    try:
        # Ожидание, пока кнопка cookie станет кликабельной
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )
        # Клик по кнопке cookie-уведомления
        cookie_button.click()
    except Exception:
        logger.info("Cookie-уведомление не найдено или уже закрыто")


def wait_for_element(driver: WebDriver, by: str, value: str, timeout: int = 10) -> Optional[WebElement] | None:
    """
        Ожидает появления элемента на веб-странице.

        Args:
            driver (WebDriver): Веб-драйвер для взаимодействия с браузером.
            by (str): Способ поиска элемента (например, 'By.CSS_SELECTOR').
            value (str): Значение для поиска элемента (например, '[data-cy="element-id"]').
            timeout (int, optional): Время ожидания элемента в секундах (по умолчанию 10).

        Returns:
            WebElement or None: Возвращает найденный элемент или None в случае таймаута.
    """
    try:
        # Ожидание появления элемента на странице
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        # Логирование предупреждения при таймауте ожидания элемента
        logger.warning(f"Таймаут ожидания элемента: {value}")
        return None

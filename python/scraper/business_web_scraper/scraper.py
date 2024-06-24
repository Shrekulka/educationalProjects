# business_web_scraper/scraper.py
import traceback
from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from logger_config import logger
from utils import accept_cookies


def initialize_driver() -> webdriver.Chrome:
    """
        Инициализирует и возвращает объект Chrome WebDriver с настроенными параметрами.

        WebDriver запускается в безголовом режиме, с отключенной графикой и другими
        оптимизациями для серверной среды. Язык интерфейса браузера установлен на украинский.

        Returns:
            webdriver.Chrome: Инициализированный объект Chrome WebDriver.
    """
    # Запись в лог о начале процесса инициализации WebDriver
    logger.info("Инициализация Chrome WebDriver")

    # Создание объекта настроек для Chrome
    options = webdriver.ChromeOptions()

    # Добавление параметров для запуска браузера в безголовом режиме (без интерфейса)
    options.add_argument('--headless')

    # Отключение использования графического процессора
    options.add_argument('--disable-gpu')

    # Отключение песочницы (sandbox), чтобы избежать потенциальных проблем с безопасностью
    options.add_argument('--no-sandbox')

    # Отключение использования общего дискового пространства для повышения производительности
    options.add_argument('--disable-dev-shm-usage')

    # Установка языка интерфейса браузера на украинский
    options.add_argument('--lang=uk')

    # Создание службы Chrome с использованием ChromeDriverManager для управления версией драйвера
    service = webdriver.ChromeService(ChromeDriverManager().install())

    # Возвращение инициализированного объекта Chrome WebDriver с заданными параметрами
    return webdriver.Chrome(service=service, options=options)


def navigate_to_page(driver: WebDriver, url: str) -> None:
    """
        Переходит по указанному URL и ожидает загрузки элемента с объявлениями,
        а также принимает cookie, если необходимо.

        Args:
            driver (WebDriver): Инициализированный объект Selenium WebDriver.
            url (str): URL-адрес страницы, на которую необходимо перейти.

        Raises:
            Exception: Если возникает ошибка при переходе на указанную страницу.
    """
    logger.info(f"Переход по URL: {url}")
    try:
        # Переход на указанный URL
        driver.get(url)

        # Ожидание загрузки элемента, содержащего список объявлений, в течение 20 секунд
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="listing-grid"]'))
        )

        # Принятие cookie, если появляется соответствующее уведомление
        accept_cookies(driver)

    # Обработка всех возможных исключений
    except Exception as e:
        detailed_error = traceback.format_exc()
        logger.error(f"Ошибка при переходе на {url}: {str(e)}\n{detailed_error}")

        # Повторное возбуждение исключения для обработки в вызывающем коде
        raise


def extract_ad_data(ad: WebElement) -> dict | None:
    """
        Извлекает данные из одного объявления на странице.

        Args:
            ad (WebElement): Веб-элемент, представляющий объявление.

        Returns:
            dict | None: Словарь с данными объявления ('Заголовок', 'Цена', 'Местоположение', 'URL')
                         или None, если произошла ошибка при извлечении данных.
    """
    try:
        # Извлечение заголовка объявления
        title = ad.find_element(By.CSS_SELECTOR, '[data-cy="l-card"] h6').text.strip()

        # Извлечение цены объявления
        price = ad.find_element(By.CSS_SELECTOR, '[data-testid="ad-price"]').text.strip()

        # Извлечение местоположения и даты объявления
        location = ad.find_element(By.CSS_SELECTOR, '[data-testid="location-date"]').text.strip()

        # Извлечение URL объявления
        ad_url = ad.find_element(By.CSS_SELECTOR, '[data-cy="l-card"] a').get_attribute('href')

        # Возврат данных объявления в виде словаря
        return {
            'Заголовок': title,
            'Цена': price,
            'Местоположение': location,
            'URL': ad_url
        }
    except NoSuchElementException as e:
        detailed_error = traceback.format_exc()
        logger.warning(f"Ошибка при извлечении данных объявления: {str(e)}\n{detailed_error}")
        return None


def scrape_page(driver: WebDriver) -> List[dict]:
    """
        Сбор данных объявлений с текущей страницы.

        Args:
            driver (WebDriver): Экземпляр веб-драйвера для управления браузером.

        Returns:
            List[dict]: Список словарей с данными объявлений. В случае ошибки возвращается пустой список.
    """
    logger.info("Сбор данных с текущей страницы")
    try:
        # Ожидание появления всех объявлений на странице (до 20 секунд)
        ads = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="l-card"]'))
        )
        logger.info(f"Найдено {len(ads)} объявлений")

        # Инициализация списка для хранения данных объявлений
        data = []

        # Цикл по всем найденным объявлениям
        for ad in ads:
            # Извлечение данных объявления
            ad_data = extract_ad_data(ad)

            # Если данные извлечены успешно, добавляем их в список
            if ad_data:
                data.append(ad_data)

        # Возврат собранных данных
        return data

    except TimeoutException:
        logger.error("Не удалось найти объявления на странице")
        return []


def get_next_page_url(driver: WebDriver) -> str | None:
    """
        Получает URL следующей страницы с объявлениями.

        Args:
            driver (WebDriver): Экземпляр веб-драйвера для управления браузером.

        Returns:
            str: URL следующей страницы с объявлениями, если она существует, иначе None.
    """
    try:
        # Поиск элемента ссылки на следующую страницу по XPath
        next_page = driver.find_element(By.XPATH, '//a[@data-cy="page-link-next"]')

        # Получение атрибута href у найденного элемента (URL следующей страницы)
        return next_page.get_attribute('href')

    except NoSuchElementException:
        logger.info("Больше страниц нет")
        return None

# selenium/infinite_scroll_scraper.py

import random
import time
import traceback
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import setup_driver
from config import config
from logger_config import logger


def get_random_pause_time(min_time: float, max_time: float) -> float:
    """
    Функция для получения случайного времени паузы в заданном диапазоне.

    Args:
        min_time (float): Минимальное время паузы в секундах.
        max_time (float): Максимальное время паузы в секундах.

    Returns:
        float: Случайное время паузы в секундах.
    """
    return random.uniform(min_time, max_time)


def main() -> None:
    """
    Основная функция для выполнения операций веб-скрапинга с бесконечной прокруткой.

    Эта функция выполняет следующие шаги:
    1. Инициализирует веб-драйвер
    2. Открывает страницу с бесконечной прокруткой
    3. Прокручивает страницу до тех пор, пока не будет достигнут конец контента
    4. Подсчитывает количество загруженных элементов
    5. Обрабатывает возможные исключения
    6. Закрывает веб-драйвер после завершения работы

    Raises:
        Exception: Любое исключение, возникшее в процессе выполнения функции
    """
    logger.info("Запуск основной функции")
    driver: Optional[WebDriver] = None
    try:
        # Инициализация веб-драйвера
        driver = setup_driver()

        # Открытие страницы с бесконечной прокруткой
        driver.get(config.infinite_scroll_url)

        # Ожидание загрузки первого элемента
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

        # Получение начальной высоты страницы
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Прокрутка страницы до конца
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Пауза для загрузки нового контента
            time.sleep(get_random_pause_time(config.min_pause_time, config.max_pause_time))

            # Получение новой высоты страницы
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Проверка, достигнут ли конец страницы
            if new_height == last_height:
                break

            last_height = new_height

        # Подсчет количества загруженных элементов
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        logger.info(f"Количество загруженных цитат: {len(quotes)}")

    except Exception as e:
        # Обработка и логирование ошибок
        detailed_error = traceback.format_exc()
        logger.error(f"Произошла ошибка в основной функции: {str(e)}\n{detailed_error}")
    finally:
        # Закрытие веб-драйвера
        if driver:
            logger.info("Закрытие веб-драйвера")
            driver.quit()
        logger.info("Процесс завершен")


if __name__ == "__main__":
    logger.info("Запуск приложения")
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Непредвиденная ошибка в приложении: {error}\n{detailed_error}")
    finally:
        logger.info("Завершение работы приложения")
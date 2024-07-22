# selenium/loging.py

import traceback
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import setup_driver
from config import config
from logger_config import logger


def main() -> None:
    """
    Основная функция для выполнения операций веб-скрапинга с логином на сайт.

    Эта функция выполняет следующие шаги:
    1. Инициализирует веб-драйвер
    2. Открывает страницу логина
    3. Вводит учетные данные и выполняет вход
    4. Ожидает загрузки страницы после входа
    5. Логирует исходный код страницы
    6. Обрабатывает возможные исключения
    7. Закрывает веб-драйвер после завершения работы

    Raises:
        Exception: Любое исключение, возникшее в процессе выполнения функции
    """
    logger.info("Запуск основной функции")
    driver: Optional[WebDriver] = None
    try:
        # Инициализация веб-драйвера
        driver = setup_driver()

        # Открытие страницы логина
        driver.get(config.login_url)

        # Ожидание загрузки элемента ввода имени пользователя
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))

        # Поиск элементов формы логина
        login = driver.find_element(By.XPATH, "//input[@id='username']")
        password = driver.find_element(By.XPATH, "//input[@id='password']")
        login_button = driver.find_element(By.XPATH, "//input[@value='Login']")

        # Ввод учетных данных
        login.send_keys(config.username)
        password.send_keys(config.password.get_secret_value())

        # Нажатие кнопки входа
        login_button.click()

        # Ожидание загрузки страницы после входа
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

        # Получение и логирование исходного кода страницы
        html = driver.page_source
        logger.info(html)

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

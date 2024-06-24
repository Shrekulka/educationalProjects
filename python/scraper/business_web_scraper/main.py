# business_web_scraper/main.py

import random
import time
import traceback
from typing import List, Dict, Union

import pandas as pd

from logger_config import logger
from scraper import initialize_driver, navigate_to_page, scrape_page, get_next_page_url
from utils import parse_arguments


def main() -> None:
    """
        Основная функция для веб-скрапинга данных с веб-страницы OLX.

        Функция инициализирует веб-драйвер, собирает данные со страниц,
        сохраняет их в CSV-файл и логирует процесс выполнения и ошибки.

        Raises:
            KeyboardInterrupt: Возникает при прерывании пользователем выполнения скрипта.
            Exception: Ловит все остальные исключения, которые могут возникнуть в процессе выполнения.
    """
    args = parse_arguments()  # Парсинг аргументов командной строки
    all_data: List[Dict[str, Union[str, int]]] = []  # Список для хранения всех собранных данных

    try:
        logger.info("Начало процесса веб-скрапинга")
        driver = initialize_driver()  # Инициализация веб-драйвера

        current_url: str = args.url  # Текущий URL для скрапинга
        page_count: int = 0  # Счётчик страниц
        max_pages: int = 5  # Максимальное количество страниц для скрапинга

        # Цикл скрапинга по страницам
        while current_url and page_count < max_pages:
            navigate_to_page(driver, current_url)  # Переход на текущую страницу

            page_data = scrape_page(driver)  # Сбор данных с текущей страницы
            logger.info(f"Собрано {len(page_data)} объявлений с текущей страницы")
            all_data.extend(page_data)  # Добавление данных текущей страницы в общий список

            current_url = get_next_page_url(driver)  # Получение URL следующей страницы
            if current_url:
                logger.info(f"Переход на следующую страницу: {current_url}")
                time.sleep(random.uniform(2, 5))  # Случайная задержка перед переходом

            page_count += 1  # Увеличение счётчика страниц

        logger.info(f"Всего собрано {len(all_data)} объявлений")

        if all_data:
            df = pd.DataFrame(all_data)  # Создание DataFrame из собранных данных
            df.to_csv(args.output, index=False, encoding='utf-8-sig')  # Запись данных в CSV-файл
            logger.info(f'Данные успешно сохранены в {args.output}')
        else:
            logger.warning("Нет данных для сохранения")

    except Exception as e:
        detailed_error = traceback.format_exc()
        logger.error(f"Ошибка: {str(e)}\n{detailed_error}")
    finally:
        if 'driver' in locals():
            driver.quit()  # Закрытие веб-драйвера в любом случае завершения работы
        logger.info("Процесс веб-скрапинга завершен")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Непредвиденная ошибка в приложении: {error}\n{detailed_error}")

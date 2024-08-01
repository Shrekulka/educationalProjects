# lego_scraper/src/thread_scraper/main_threads.py

import csv
import traceback
from concurrent.futures import ThreadPoolExecutor

from config.settings import config
from src.thread_scraper.extractors import extract_themes
from src.thread_scraper.processors import process_theme
from src.thread_scraper.scraper import get_soup
from utils.logger_config import logger


def main() -> None:
    """
    Основная функция для запуска веб-скрапинга с использованием многопоточности.

    1. Загружает страницу с темами и извлекает список тем.
    2. Использует многопоточность для параллельной обработки каждой темы.
    3. Сохраняет собранные данные об игрушках в CSV-файл.
    4. Логирует процесс выполнения и возможные ошибки.
    """
    try:
        logger.info("Начало процесса веб-скрапинга")

        # Получаем HTML-код страницы с темами
        themes_page_soup = get_soup(config.THEME_URL)

        # Извлекаем список тем из HTML-кода страницы с темами
        themes = extract_themes(themes_page_soup)

        # Создаем пустой список для хранения данных обо всех игрушках
        all_toy_data = []

        # Используем ThreadPoolExecutor для параллельной обработки тем
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Отправляем задачи на обработку каждой темы в отдельные потоки
            futures = [executor.submit(process_theme, theme) for theme in themes]

            # Сбор результатов из всех потоков
            for future in futures:
                # Расширяем общий список данными из текущего потока
                all_toy_data.extend(future.result())

        # Если есть данные об игрушках, записываем их в CSV-файл
        if all_toy_data:
            # Получаем названия столбцов из первого элемента данных
            keys = all_toy_data[0].keys()

            with open(config.CSV_FILE_PATH_THREADS, 'w', newline='', encoding='utf-8') as outfile:
                # Создаем объект DictWriter для записи данных в CSV
                dict_writer = csv.DictWriter(outfile, keys)
                # Записываем заголовок (названия столбцов)
                dict_writer.writeheader()
                # Записываем данные об игрушках
                dict_writer.writerows(all_toy_data)

            logger.info(f"Все данные об игрушках записаны в {config.CSV_FILE_PATH_THREADS}. "
                        f"Всего собрано {len(all_toy_data)} игрушек.")
        else:
            logger.warning("Данные об игрушках не собраны")

    except Exception as e:
        detailed_close_age_gate_error = traceback.format_exc()
        logger.error(f"Ошибка при выполнении: {str(e)}\n{detailed_close_age_gate_error}")
    finally:
        logger.info("Процесс веб-скрапинга завершен")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Неожиданная ошибка приложения: {error}\n{detailed_error}")

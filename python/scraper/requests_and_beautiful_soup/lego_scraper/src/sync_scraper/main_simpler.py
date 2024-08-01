# lego_scraper/src/sync_scraper/main_simpler.py

import csv
import traceback

from config.settings import config
from src.sync_scraper.extractors import get_themes, get_toys_page, get_toys_data
from src.sync_scraper.scraper import get_soup
from utils.logger_config import logger


def main() -> None:
    """
    Основная функция для выполнения процесса веб-скрапинга игрушек.

    В этой функции происходит:
    1. Логирование начала процесса.
    2. Получение и обработка HTML-страницы с темами.
    3. Извлечение и обработка данных о каждой теме и её страницах.
    4. Запись собранных данных в CSV-файл.
    5. Логирование успешного завершения или ошибок.

    Returns:
        None
    """
    try:
        logger.info("Начало процесса веб-скрапинга")

        # Получаем HTML-код страницы с темами и парсим его с помощью функции get_soup
        themes_page_soup = get_soup(config.THEME_URL)

        # Извлекаем список тем из полученного HTML-кода
        themes = get_themes(themes_page_soup)

        # Создаем пустой список для хранения данных обо всех игрушках
        all_toys = []

        # Проходимся по каждой теме
        for current_theme in themes:
            logger.info(f"\nОбработка темы: {current_theme['title']}\n")

            # Получаем HTML-код страницы с текущей темой и парсим его
            theme_page_soup = get_soup(current_theme['url'])

            # Получаем количество игрушек и страниц с игрушками для текущей темы
            total_toys, total_pages = get_toys_page(theme_page_soup)

            # Логируем количество найденных игрушек и страниц
            logger.info(f"\nНайдено {total_toys} игрушек на {total_pages} страницах")

            # Проходимся по каждой странице с игрушками
            for page_number in range(config.DEFAULT_PAGE, total_pages + 1):

                logger.info(f"\nОбработка №{page_number} страницы из {total_pages} для темы {current_theme['title']}\n")

                # Получаем HTML-код текущей страницы и парсим его
                toy_page_soup = get_soup(current_theme['url'], page_number)

                # Извлекаем данные об игрушках с текущей страницы
                toys_data_on_page = get_toys_data(toy_page_soup=toy_page_soup, theme_name=current_theme['title'])

                # Добавляем извлеченные данные к общему списку
                all_toys.extend(toys_data_on_page)

        # Если были собраны данные об игрушках, записываем их в CSV-файл
        if all_toys:
            # Получаем ключи (названия столбцов) из первого элемента данных
            keys = all_toys[0].keys()

            # Открываем CSV-файл для записи
            with open(config.CSV_FILE_PATH_SIMPLE, 'w', newline='', encoding='utf-8') as outfile:

                # Создаем объект DictWriter для записи данных в CSV
                dict_writer = csv.DictWriter(outfile, keys)

                # Записываем заголовок (названия столбцов) в CSV
                dict_writer.writeheader()

                # Записываем все данные об игрушках в CSV
                dict_writer.writerows(all_toys)

            # Логируем успешную запись данных в CSV-файл
            logger.info(f"Все данные об игрушках записаны в {config.CSV_FILE_PATH_SIMPLE}. "
                        f"Всего собрано {len(all_toys)} игрушек.")
        else:
            logger.warning("Данные об игрушках не собраны")

    except Exception as e:
        detailed_close_age_gate_error = traceback.format_exc()
        logger.error(f"Ошибка: {str(e)}\n{detailed_close_age_gate_error}")
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

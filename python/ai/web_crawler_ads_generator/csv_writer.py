# web_crawler_ads_generator/csv_writer.py

import csv
import traceback

from config import CSV_FILE_NAME
from logger_config import logger


def write_csv(ads: list, filename: str = CSV_FILE_NAME) -> None:
    """
        Записывает сгенерированные объявления в CSV файл.

        Args:
            ads (list): Список словарей с данными для записи в формате [{'url': str, 'ad_text': str}, ...].
            filename (str, optional): Имя файла CSV. По умолчанию используется значение из конфигурации CSV_FILE_NAME.

        Returns:
            None
    """
    try:
        logger.debug("########## write_csv function works! ##########")

        # Открываем файл для записи в режиме 'w' (запись), с указанием кодировки UTF-8 и без автоматической добавки
        # новой строки
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            # Создаем объект writer для записи данных в CSV формате
            writer = csv.writer(file)
            # Записываем заголовки в CSV файл
            writer.writerow(['URL', 'Ad Text'])
            # Итерируемся по списку объявлений и записываем каждое объявление в CSV файл
            for ad in ads:
                # Каждое объявление записывается как отдельная строка с двумя значениями: URL и текст объявления
                writer.writerow([ad['url'], ad['ad_text']])

        logger.debug(f"Запись в файл {filename} успешно завершена")

    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла ошибка при записи в CSV файл {filename}: {e}\n{detailed_error_message}")

# csv_writer.py

import csv
import traceback

from logger_config import logger


def write_csv(ads, filename):
    try:
        logger.debug("########## write_csv function works! ##########")
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Ad Text'])  # Запись заголовков в CSV файл
            for ad in ads:
                writer.writerow([ad['url'], ad['ad_text']])  # Запись сгенерированных объявлений в CSV файл
        logger.debug(f"Запись в файл {filename} успешно завершена")
    except Exception as e:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла ошибка при записи в CSV файл {filename}: {e}\n{detailed_error_message}")

# Instagram_scraper_instaloader/config.py

import csv
import json
from typing import List, Dict, Any

from logger_config import logger


def save_to_json(data: List[Dict[str, Any]], filename: str) -> None:
    """
    Сохраняет данные в JSON файл.

    Args:
        data: Список словарей с данными профилей.
        filename: Имя файла для сохранения.
    """
    # Открываем файл с указанным именем для записи в формате JSON
    with open(f"{filename}.json", "w", encoding="utf-8") as f:

        # Записываем данные в файл в формате JSON
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info(f"Данные сохранены в файл {filename}.json")


def save_to_csv(data: List[Dict[str, Any]], filename: str) -> None:
    """
    Сохраняет данные в CSV файл.

    Args:
        data: Список словарей с данными профилей.
        filename: Имя файла для сохранения.
    """
    # Проверяем, есть ли данные для сохранения
    if not data:
        logger.error("Нет данных для сохранения в CSV.")
        return

    # Получаем имена полей из первого словаря в списке данных
    fieldnames = data[0].keys()

    # Открываем файл с указанным именем для записи в формате CSV
    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as f:
        # Создаем объект writer для записи данных в формате CSV
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # Записываем заголовки в CSV файл
        writer.writeheader()
        # Записываем строки данных в CSV файл
        writer.writerows(data)

    logger.info(f"Данные сохранены в файл {filename}.csv")

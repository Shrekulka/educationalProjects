# web_crawler_ads_generator/checkpoint.py

import json
import os

from config import CHECKPOINT_FILE_PATH


def save_checkpoint(pages) -> None:
    """
        Сохраняет текущее состояние краулинга в файл.

        Args:
            pages (list): Список страниц, для которых необходимо сохранить URL.

        Returns:
            None
    """
    # Открываем файл для записи контрольной точки
    with open(CHECKPOINT_FILE_PATH, 'w', encoding='utf-8') as f:
        # Записываем в файл список словарей с URL каждой страницы из переданного списка
        json.dump([{'url': page['url']} for page in pages], f)


def load_checkpoint() -> list or None:
    """
        Загружает сохраненное состояние краулинга из файла.

        Returns:
            list or None: Список URL страниц из сохраненной контрольной точки или None, если файл не существует.
    """
    # Проверяем наличие файла контрольной точки
    if os.path.exists(CHECKPOINT_FILE_PATH):
        # Открываем файл для чтения
        with open(CHECKPOINT_FILE_PATH, 'r', encoding='utf-8') as f:
            # Возвращаем список URL страниц из загруженной контрольной точки
            return json.load(f)
    # Если файл не существует, возвращаем None
    return None


def clear_checkpoint() -> None:
    """
        Удаляет файл с контрольной точкой.

        Returns:
            None
    """
    # Проверяем наличие файла контрольной точки
    if os.path.exists(CHECKPOINT_FILE_PATH):
        # Удаляем файл, если он существует
        os.remove(CHECKPOINT_FILE_PATH)


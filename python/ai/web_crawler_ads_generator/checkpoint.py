# web_crawler_ads_generator/checkpoint.py

import json
import os

CHECKPOINT_FILE = 'crawler_checkpoint.json'


def save_checkpoint(pages):
    """Сохраняет текущее состояние краулинга в файл."""
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump([{'url': page['url']} for page in pages], f)


def load_checkpoint():
    """Загружает сохраненное состояние краулинга из файла."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def clear_checkpoint():
    """Удаляет файл с контрольной точкой."""
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)

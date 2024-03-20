# fast_blog/utils/cache.py

import time
import traceback
from typing import Dict, List, Optional

from schemas.posts import Post
from utils.logger_config import logger

# Словарь для хранения кэшированных данных
# Ключ - email пользователя, значение - список постов и время кэширования
cache: Dict[str, tuple[List[Post], float]] = {}

# Время жизни кэша в секундах (5 минут)
CACHE_EXPIRATION_TIME = 300


def get_from_cache(user_email: str) -> Optional[List[Post]]:
    """
    Извлекает кэшированные посты для указанного пользователя.

    Args:
        user_email (str): Email пользователя.

    Returns:
        Optional[List[Post]]: Список кэшированных постов или None, если кэш истек или отсутствует.
    """
    try:
        # Проверяем наличие данных в кэше для указанного пользователя
        if user_email in cache:
            # Извлекаем список постов и время кэширования из кэша
            cached_posts, cached_time = cache[user_email]

            # Проверяем, не истек ли кэш
            if time.time() - cached_time < CACHE_EXPIRATION_TIME:
                return cached_posts
    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        # Обработка ошибок доступа к кэшу
        logger.error(f"Error accessing cache: {e}\n{detailed_error_traceback}")

    # Если кэш отсутствует, истек или возникла ошибка, возвращаем None
    return None


def set_in_cache(user_email: str, posts: Optional[List[Post]]) -> None:
    """
    Сохраняет посты в кэше для указанного пользователя.

    Args:
        user_email (str): Email пользователя.
        posts (Optional[List[Post]]): Список постов для кэширования или None для удаления кэша.
    """
    try:
        # Если посты не заданы, удаляем данные из кэша для указанного пользователя
        if posts is None:
            clear_cache(user_email)
            return

        # Сохраняем посты и текущее время в кэше для указанного пользователя
        cache[user_email] = (posts, time.time())
    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        # Обработка ошибок доступа к кэшу
        logger.error(f"Error setting cache: {e}\n{detailed_error_traceback}")


def clear_cache(user_email: str) -> None:
    """
    Удаляет кэш для указанного пользователя.

    Args:
        user_email (str): Email пользователя.
    """
    try:
        # Проверяем, существует ли кэш для указанного пользователя
        if user_email in cache:
            # Удаляем кэш для указанного пользователя
            del cache[user_email]
    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        # Обработка ошибок доступа к кэшу
        logger.error(f"Error clearing cache: {e}\n{detailed_error_traceback}")

# fast_api_post_manager/utils/cache_utils.py

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# Кеш для хранения результатов запросов
_cache: Dict[str, Dict[str, Any]] = {}


def get_cache_key(user_id: str, endpoint: str) -> str:
    """
    Создает ключ для кеша.
    """
    return f"{user_id}:{endpoint}"


def set_cache(key: str, data: Any, minutes: int = 5) -> None:
    """
    Сохраняет данные в кеш.
    """
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    _cache[key] = {
        "data": data,
        "expires_at": expires_at
    }


def get_cache(key: str) -> Optional[Any]:
    """
    Получает данные из кеша, если они действительны.
    """
    cache_item = _cache.get(key)
    if not cache_item:
        return None

    if is_cache_valid(cache_item["expires_at"]):
        return cache_item["data"]

    # Удаляем недействительный кеш
    del _cache[key]
    return None


def is_cache_valid(expires_at: datetime) -> bool:
    """
    Проверяет, действителен ли кеш.
    """
    return datetime.now(timezone.utc) < expires_at


def invalidate_cache(user_id: str) -> None:
    """
    Инвалидирует все кеши для указанного пользователя.
    """
    keys_to_delete = [k for k in _cache.keys() if k.startswith(f"{user_id}:")]
    for key in keys_to_delete:
        del _cache[key]


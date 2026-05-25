# inter_exchange_arbitrage_bot/src/utils/decorators.py

from functools import wraps
from src.utils.logger import logger

def check_api_key(api_name: str, config_key: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not getattr(self.config, config_key):
                logger.info(f"{api_name} API ключ не настроен. Выполнение {func.__name__} пропущено.")
                if "gainers" in func.__name__:
                    return {"gainers": [], "losers": []}
                return []
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator
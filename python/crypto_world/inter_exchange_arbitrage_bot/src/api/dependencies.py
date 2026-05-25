# inter_exchange_arbitrage_bot/src/api/dependencies.py

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from src.constants.api_constants import HEADER_INTERNAL_API_KEY
from src.core.config import config
from src.lexicon.lexicon_ru import LEXICON_RU
from src.utils.logger import logger

api_key_header = APIKeyHeader(name=HEADER_INTERNAL_API_KEY, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Проверяет валидность API ключа для административных эндпоинтов.
    """
    # 1. Проверяем, настроен ли ключ на сервере вообще.
    if not hasattr(config, 'internal_api_key') or not config.internal_api_key:
        logger.error(LEXICON_RU['log_internal_api_key_not_set'])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=LEXICON_RU['api_error_key_not_configured']
        )

    # 2. Сравниваем ключ, предоставленный клиентом, с эталонным ключом из конфига.
    if api_key != config.internal_api_key:
        # Для безопасности логируем только часть полученного ключа.
        preview = api_key[:8] if api_key else 'None'
        logger.warning(LEXICON_RU['log_invalid_api_key_attempt'].format(api_key_preview=preview))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=LEXICON_RU['api_error_invalid_credentials']
        )

    # 3. Если все проверки пройдены, логируем успешную авторизацию.
    logger.info(LEXICON_RU['log_admin_request_authorized'])

    # И возвращаем ключ для возможного дальнейшего использования.
    return api_key
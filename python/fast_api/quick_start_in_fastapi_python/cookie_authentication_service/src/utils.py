# cookie_authentication_service/src/utils.py

import secrets


def generate_session_token() -> str:
    """
        Генерирует случайный сессионный токен.

        Returns:
            str: Сессионный токен, представленный в виде строки из 64 символов (hex).
    """
    return secrets.token_hex(32)

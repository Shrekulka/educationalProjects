# fast_api_post_manager/utils/password_utils.py

import bcrypt
from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyHeader


def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt и возвращает строковое представление хеша.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')  # Возвращаем строку


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля его хешу.

    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хеш пароля из БД

    Returns:
        bool: True если пароли совпадают, иначе False
    """
    try:
        password_bytes = plain_password.encode('utf-8')

        # Если хеш хранится как строка, конвертируем его в байты
        if isinstance(hashed_password, str):
            hashed_password_bytes = hashed_password.encode('utf-8')
        else:
            hashed_password_bytes = hashed_password

        return bcrypt.checkpw(password=password_bytes, hashed_password=hashed_password_bytes)
    except Exception as e:
        print(f"Ошибка при проверке пароля: {e}")
        return False


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     try:
#         password_byte_enc = plain_password.encode('utf-8')
#
#         # Если хеш хранится как строковое представление байтов
#         if hashed_password.startswith("b'") and hashed_password.endswith("'"):
#             # Извлекаем фактический хеш из строки
#             hashed_password = hashed_password[2:-1].replace('\\\\', '\\')
#
#         # Преобразуем в байты
#         hashed_password_bytes = hashed_password.encode('utf-8')
#
#         return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_bytes)
#     except Exception as e:
#         print(f"Ошибка при проверке пароля: {e}")
#         return False

apikey_scheme = APIKeyHeader(name="Authorization")
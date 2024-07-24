# Instagram_scraper_instaloader/config.py

import asyncio
from typing import List, Optional, Literal, Union

from pydantic.v1 import BaseSettings, Field

# Константы с значениями по умолчанию для различных настроек
DEFAULT_MIN_DELAY = 2                        # Минимальная задержка между запросами
DEFAULT_MAX_DELAY = 5                        # Максимальная задержка между запросами
DEFAULT_OUTPUT_FILE = "data/instagram_data"  # Имя файла для сохранения данных по умолчанию, включая путь
DEFAULT_SAVE_FORMAT = "csv"                  # Формат сохранения данных по умолчанию (json или csv)
SEMAPHORE = asyncio.Semaphore(5)             # Семафор для ограничения количества одновременных запросов


class InstagramProfileSettings(BaseSettings):
    """
    Класс для хранения и валидации настроек профиля Instagram.

    Этот класс используется для описания и проверки конфигурационных данных
    для профилей Instagram. Поля включают информацию о пользователе, такие как
    имя пользователя, ID, биография, количество постов, подписчиков и другое.

    Attributes:
        username (str): Обязательное поле, имя пользователя Instagram.
        user_id (Optional[int]): Необязательное поле, ID пользователя.
        full_name (Optional[str]): Необязательное поле, полное имя пользователя.
        biography (Optional[str]): Необязательное поле, биография пользователя.
        private (bool): Поле, указывающее, является ли аккаунт приватным. По умолчанию False.
        verified (bool): Поле, указывающее, является ли аккаунт верифицированным. По умолчанию False.
        is_business_account (bool): Поле, указывающее, является ли аккаунт бизнес-аккаунтом. По умолчанию False.
        business_category_name (Optional[str]): Необязательное поле, название категории бизнеса.
        category_name (Optional[str]): Необязательное поле, название категории.
        posts_count (int): Поле, указывающее количество постов. По умолчанию 0.
        followers (int): Поле, указывающее количество подписчиков. По умолчанию 0.
        following (int): Поле, указывающее количество подписок. По умолчанию 0.
        profile_pic_url (Optional[str]): Необязательное поле, URL фотографии профиля.
        external_url (Optional[str]): Необязательное поле, внешняя ссылка в профиле.
        has_highlight_reels (Optional[bool]): Необязательное поле, указывающее, есть ли highlights.
        last_post_likes (Optional[int]): Необязательное поле, количество лайков последнего поста.
        last_post_comments (Optional[int]): Необязательное поле, количество комментариев последнего поста.
        last_post_url (Optional[str]): Необязательное поле, URL последнего поста.
        last_post_timestamp (Optional[Union[int, str]]): Необязательное поле, timestamp последнего поста.
        igtv_count (Optional[int]): Необязательное поле, количество IGTV видео.
    """
    # Обязательное поле для имени пользователя
    username: str = Field(..., description="Имя пользователя Instagram")

    # Необязательное поле для ID пользователя
    user_id: Optional[int] = Field(None, description="ID пользователя")

    # Необязательное поле для полного имени
    full_name: Optional[str] = Field(None, description="Полное имя пользователя")

    # Необязательное поле для биографии
    biography: Optional[str] = Field(None, description="Биография пользователя")

    # Поле для приватности аккаунта
    private: bool = Field(False, description="Является ли аккаунт приватным")

    # Поле для верификации аккаунта
    verified: bool = Field(False, description="Является ли аккаунт верифицированным")

    # Поле для бизнес-аккаунта
    is_business_account: bool = Field(False, description="Является ли аккаунт бизнес-аккаунтом")

    # Необязательное поле для категории бизнеса
    business_category_name: Optional[str] = Field(None, description="Название категории бизнеса")

    # Необязательное поле для категории
    category_name: Optional[str] = Field(None, description="Название категории")

    # Поле для количества постов
    posts_count: int = Field(0, description="Количество постов")

    # Поле для количества подписчиков
    followers: int = Field(0, description="Количество подписчиков")

    # Поле для количества подписок
    following: int = Field(0, description="Количество подписок")

    # Необязательное поле для URL профиля
    profile_pic_url: Optional[str] = Field(None, description="URL фотографии профиля")

    # Необязательное поле для внешней ссылки
    external_url: Optional[str] = Field(None, description="Внешняя ссылка в профиле")

    # Необязательное поле для наличия highlights
    has_highlight_reels: Optional[bool] = Field(None, description="Есть ли highlights")

    # Необязательное поле для лайков последнего поста
    last_post_likes: Optional[int] = Field(None, description="Количество лайков последнего поста")

    # Необязательное поле для комментариев последнего поста
    last_post_comments: Optional[int] = Field(None, description="Количество комментариев последнего поста")

    # Необязательное поле для URL последнего поста
    last_post_url: Optional[str] = Field(None, description="URL последнего поста")

    # Необязательное поле для timestamp последнего поста
    last_post_timestamp: Optional[Union[int, str]] = Field(None, description="Timestamp последнего поста")

    # Необязательное поле для количества IGTV видео
    igtv_count: Optional[int] = Field(None, description="Количество IGTV видео")


class Settings(BaseSettings):
    """
        Класс для хранения и валидации основных настроек приложения.

        Этот класс используется для конфигурации параметров приложения, таких как
        список пользователей Instagram для анализа, параметры сохранения данных и
        задержка между запросами. Поля включают в себя информацию о формате сохранения,
        имени файла и задержке между запросами.

        Attributes:
            instagram_profiles (List[str]): Обязательное поле, список имен пользователей Instagram для анализа.
            save_data (bool): Поле, указывающее, следует ли сохранять данные в файл. По умолчанию False.
            save_format (Literal["json", "csv"]): Поле для выбора формата сохранения данных, допустимые значения "json"
                                                  или "csv".
            output_file (str): Поле для указания имени файла для сохранения данных (без расширения). По умолчанию
                               "instagram_data".
            min_delay (int): Поле для минимальной задержки между запросами в секундах. По умолчанию 2.
            max_delay (int): Поле для максимальной задержки между запросами в секундах. По умолчанию 5.
    """
    # Обязательное поле для списка имен пользователей Instagram
    instagram_profiles: List[str] = Field(..., description="Список имен пользователей Instagram для анализа")

    # Поле для определения, сохранять ли данные
    save_data: bool = Field(False, description="Сохранять ли данные в файл")

    # Поле для формата сохранения данных, может быть только "json" или "csv"
    save_format: Literal["json", "csv"] = Field(DEFAULT_SAVE_FORMAT,
                                                description="Формат сохранения данных (json или csv)")

    # Поле для имени файла сохранения данных
    output_file: str = Field(DEFAULT_OUTPUT_FILE,
                             description="Имя файла для сохранения данных, включая путь и имя файла (без расширения). "
                                         "По умолчанию 'data/instagram_data'")

    # Поле для минимальной задержки между запросами
    min_delay: int = Field(DEFAULT_MIN_DELAY, description="Минимальная задержка между запросами в секундах")

    # Поле для максимальной задержки между запросами
    max_delay: int = Field(DEFAULT_MAX_DELAY, description="Максимальная задержка между запросами в секундах")

    class Config:
        """
        Настройки конфигурации pydantic для загрузки переменных окружения.

        Этот класс конфигурации задает параметры для работы pydantic, такие как файл
        с переменными окружения и его кодировка.
        """
        env_file = ".env"            # Файл для загрузки переменных окружения
        env_file_encoding = "utf-8"  # Кодировка файла переменных окружения


# Создаем экземпляр класса Settings для хранения конфигурационных данных
config: Settings = Settings()

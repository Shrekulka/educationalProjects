# selenium/config.py

from pydantic.v1 import BaseSettings, SecretStr


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения.

    Атрибуты:
        geckodriver_path (str): Путь к исполняемому файлу geckodriver.
        login_url (str): URL страницы логина.
        infinite_scroll_url (str): URL страницы с бесконечной прокруткой.
        min_pause_time (float): Минимальное время паузы между действиями.
        max_pause_time (float): Максимальное время паузы между действиями.
        username (str): Имя пользователя для логина.
        password (SecretStr): Пароль пользователя (хранится в зашифрованном виде).
        headless_mode (bool): Флаг для запуска браузера в headless режиме.
        disable_cache (bool): Флаг для отключения кэширования.
        tracking_protection (bool): Флаг для включения защиты от отслеживания.
        custom_user_agent (str): Пользовательский User-Agent.

    """
    geckodriver_path: str = './geckodriver'
    login_url: str = 'https://quotes.toscrape.com/login'
    infinite_scroll_url: str = 'https://quotes.toscrape.com/scroll'
    min_pause_time: float = 1.2
    max_pause_time: float = 2.5
    username: str
    password: SecretStr

    # Настройки для веб-драйвера
    headless_mode: bool = True
    disable_cache: bool = True
    tracking_protection: bool = True
    custom_user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Создаем экземпляр класса Settings для хранения конфигурационных данных
config: Settings = Settings()
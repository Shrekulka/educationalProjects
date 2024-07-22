# selenium/common.py

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

from config import config


def setup_driver() -> WebDriver:
    """
    Настройка и инициализация веб-драйвера с расширенными опциями.

    Эта функция выполняет следующие шаги:
    1. Создает объект Service для geckodriver
    2. Инициализирует объект Options для настройки Firefox
    3. Применяет различные настройки в зависимости от конфигурации
    4. Создает и возвращает настроенный объект WebDriver

    Returns:
        WebDriver: Настроенный объект веб-драйвера Firefox

    Raises:
        WebDriverException: Если возникли проблемы при инициализации драйвера
    """
    # Создание объекта Service для geckodriver
    service = Service(config.geckodriver_path)

    # Инициализация объекта Options
    options = Options()

    # Основные настройки
    if config.headless_mode:
        options.add_argument('-headless')           # Запуск в фоновом режиме
    options.add_argument('-no-sandbox')             # Отключение песочницы для стабильности
    options.add_argument('-disable-dev-shm-usage')  # Отключение /dev/shm для стабильности в Docker

    # Настройки производительности
    if config.disable_cache:
        options.set_preference('browser.cache.disk.enable', False)
        options.set_preference('browser.cache.memory.enable', False)
        options.set_preference('browser.cache.offline.enable', False)
        options.set_preference('network.http.use-cache', False)

    # Настройки приватности
    if config.tracking_protection:
        options.set_preference('privacy.trackingprotection.enabled', True)
        options.set_preference('privacy.donottrackheader.enabled', True)

    # Отключение уведомлений и всплывающих окон
    options.set_preference('dom.webnotifications.enabled', False)
    options.set_preference('dom.push.enabled', False)
    options.set_preference('dom.disable_open_during_load', True)

    # Настройки для улучшения стабильности
    options.set_preference('browser.tabs.remote.autostart', False)
    options.set_preference('browser.tabs.remote.autostart.2', False)

    # Настройки для уменьшения использования ресурсов
    options.set_preference('media.autoplay.default', 0)
    options.set_preference('media.autoplay.allowed-muted', False)

    # Отключение WebGL для уменьшения нагрузки на GPU
    options.set_preference('webgl.disabled', True)

    # Настройки User-Agent
    if config.custom_user_agent:
        options.set_preference('general.useragent.override', config.custom_user_agent)

    # Дополнительные настройки для более "человеческого" поведения
    options.set_preference('intl.accept_languages', 'ru-RU,ru')
    options.set_preference('general.useragent.locale', 'ru-RU')

    # Создание и возврат настроенного объекта WebDriver
    return webdriver.Firefox(service=service, options=options)
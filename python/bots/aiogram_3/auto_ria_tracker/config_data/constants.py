# auto_ria_tracker/config_data/constants.py

from typing import Dict, List


class AutoRiaURLs:
    """
    URL Management Class for AUTO.RIA Vehicle Interactions

    This class provides comprehensive URL generation methods for interacting
    with the AUTO.RIA automotive marketplace website. It contains base URLs,
    search URLs, and methods for generating specific car and photo URLs.
    """
    # Базовый URL для украинской версии сайта
    BASE_URL: str = "https://auto.ria.com/uk"

    # URL для поиска автомобилей
    SEARCH_URL: str = f"{BASE_URL}/search/"

    # URL для API фотографий
    PHOTOS_API_URL: str = f"{BASE_URL}/bu/photos"

    # URL для CDN с фотографиями
    CDN_URL: str = "https://cdn.riastatic.com/photosnew/auto/photo"

    @classmethod
    def get_car_url(cls, car_id: int) -> str:
        """
        Generates a complete URL for a specific vehicle listing.

        This method constructs a detailed URL for a Toyota Sequoia
        based on the provided car identifier.

        Args:
            car_id (int): Unique identifier for the vehicle

        Returns:
            str: Full URL of the vehicle listing page
        """
        return f"{cls.BASE_URL}/auto_toyota_sequoia_{car_id}.html"

    @classmethod
    def get_photos_api_url(cls, car_id: int) -> str:
        """
        Constructs the API URL for retrieving vehicle photographs.

        Args:
            car_id (int): Unique identifier for the vehicle

        Returns:
            str: Complete API endpoint URL for vehicle photos
        """
        return f"{cls.PHOTOS_API_URL}/{car_id}"

    @classmethod
    def get_photo_url(cls, car_id: int, photo_id: str) -> str:
        """
        Generates a direct URL for a specific vehicle photograph.

        Args:
            car_id (int): Unique identifier for the vehicle
            photo_id (str): Identifier for the specific photo

        Returns:
            str: Complete URL for the vehicle image
        """
        return f"{cls.CDN_URL}/{car_id}_{photo_id}f.jpg"


class AutoRiaSelectors:
    """
    CSS Selector Management for AUTO.RIA Web Scraping

    This class centralizes CSS selectors used for parsing and extracting
    information from AUTO.RIA web pages. It provides consistent selector
    references for various elements like search results, car details,
    and image galleries.
    """
    # Селектор для результатов поиска
    SEARCH_RESULTS: str = '.content-bar'

    # Селектор для ID автомобиля
    CAR_ID: str = '.content .area.favorite-footer .item.unlink'

    # Селектор для заголовка объявления
    TITLE: str = '.head-ticket .address'

    # Селектор для цены
    PRICE: str = '.price-ticket'

    # Селектор для ссылки на объявление
    LINK: str = '.m-link-ticket'

    # Селектор для галереи изображений
    GALLERY_SELECTORS: list = [
        '.photo-74x56[data-id]',   # Основной селектор
        '.gallery-order images',   # Альтернативный селектор
        '.photo-74x56 images',      # Еще один альтернативный селектор
        '.carousel-photo img',      # Селектор изображений внутри карусели
        '.photo-gallery img',       # Селектор для полноразмерных изображений в галерее
        '.gallery-thumbnails img',  # Селектор для миниатюр галереи
        '.photos-block img',        # Дополнительный селектор внутри блока изображений
        'div.photo-slider img',     # Изображения в слайдере
        'div.gallery img',          # Общий селектор для галереи
        '.carousel-inner img',      # Изображения внутри Bootstrap-карусели
        '.swiper-slide img',        # Изображения внутри Swiper-слайдера (если используется)
        'img[data-large]',          # Часто встречается для хранения ссылок на полноразмерные фото
        'img[data-src]',            # Альтернативное хранение ссылок на фото
    ]

    # Селекторы для главного фото в разных форматах
    MAIN_PHOTO_PICTURE: str = '.ticket-photo picture'
    MAIN_PHOTO_WEBP: str = 'source[type="image/webp"]'
    MAIN_PHOTO_IMG: str = 'images[src]'

    # Список атрибутов, которые могут содержать ссылки на изображения
    PHOTO_ATTRS: list = [
        'src',            # Стандартный атрибут ссылки на изображение
        'data-src',       # Часто используется для lazy loading
        'data-url',       # Может содержать ссылку на изображение
        'data-original',  # Оригинальная ссылка на изображение
        'data-large',     # Часто используется для полноразмерных изображений
        'data-lazy',      # Lazy load-изображения
        'data-full',      # Полноразмерное изображение
        'data-thumb',     # Миниатюра изображения
        'href'            # Иногда изображения могут быть спрятаны в ссылках
    ]


class AutoRiaDefaults:
    """
    Default Configuration and Identifier Constants for Vehicle Search

    This class provides predefined constants and mappings for vehicle
    search parameters, including category IDs, manufacturer IDs,
    and standard configurations.
    """
    # ID категории легковых автомобилей
    CATEGORY_ID: int = 1
    # ID производителя Toyota
    MARKA_ID: int = 79

    # Модель по умолчанию
    DEFAULT_MODEL: str = 'SEQUOIA'

    # Словарь ID моделей Toyota
    MODEL_IDS: Dict[str, int] = {
        "SEQUOIA": 2104,
        "TUNDRA": 2046,
        "LAND_CRUISER": 2030
    }

    # Значения для фильтра по стране происхождения (параметр abroad)
    ABROAD_VALUES = {
        'ALL': -1,      # Все авто (не фильтровать по стране)
        'USA_ONLY': 0,  # Показывать только авто из США
        'NON_USA': 1    # Показывать только авто не из США
    }

    # Значения для фильтра по участию в ДТП (параметр damage)
    DAMAGE_VALUES = {
        'ALL': -1,          # Все авто (не фильтровать по ДТП)
        'NO_ACCIDENT': 1,   # Показывать только авто без ДТП
        'WITH_ACCIDENT': 0  # Показывать только авто после ДТП
    }

    # Форматы изображений
    IMAGE_FORMATS: Dict[str, str] = {
        "PREVIEW_JPG": "bx.jpg",
        "PREVIEW_WEBP": "bx.webp",
        "FULL_JPG": "f.jpg",
        "FULL_WEBP": "f.webp"
    }

    # Расширения файлов
    FILE_EXTENSIONS: Dict[str, str] = {
        "HTML": ".html"
    }


class HTTPConstants:
    """
    HTTP Connection and Request Configuration Constants

    Provides standardized constants for HTTP interactions, including
    timeout settings, headers, and status codes.
    """
    # Время ожидания для HTTP-соединений (в секундах)
    TIMEOUT: int = 30

    # Отключение проверки SSL-сертификата (для отладки)
    SSL_VERIFY: bool = False

    # Константы для статусов ответа от API
    STATUS_OK: int = 200
    STATUS_NOT_FOUND: int = 404

    # Код ответа при превышении лимита запросов
    STATUS_TOO_MANY_REQUESTS: int = 429

    # Задержка между повторными попытками (в секундах)
    RETRY_DELAY: int = 60

    # Время ожидания для отдельного запроса
    REQUEST_TIMEOUT: int = 30

    # Стандартные заголовки для HTTP-запросов
    HEADERS: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }


class AuctionURLs:
    """
    Auction Website URL Management

    Provides methods for generating auction lot URLs for different platforms.
    """
    # Базовый URL для аукциона Copart
    COPART_BASE: str = "https://www.copart.com"

    # Базовый URL для аукциона IAAI
    IAAI_BASE: str = "https://www.iaai.com"

    # Путь к лоту в URL
    LOT_PATH: str = "lot"

    @classmethod
    def get_copart_lot_url(cls, lot_number: str) -> str:
        """
        Generates a Copart auction lot URL.

        Args:
            lot_number (str): Unique identifier for the auction lot

        Returns:
            str: Complete URL for the specific lot
        """
        return f"{cls.COPART_BASE}/{cls.LOT_PATH}/{lot_number}"

    @classmethod
    def get_iaai_lot_url(cls, lot_number: str) -> str:
        """
        Generates an IAAI auction lot URL.

        Args:
            lot_number (str): Unique identifier for the auction lot

        Returns:
            str: Complete URL for the specific lot
        """
        return f"{cls.IAAI_BASE}/{cls.LOT_PATH}/{lot_number}"


class AuctionHTMLSelectors:
    """CSS Selectors for Auction Website Parsing

    Contains CSS selectors for extracting information from auction websites.
    """
    # Селектор для галереи изображений Copart
    COPART_GALLERY: str = "div.lot-gallery"

    # Селектор для изображений в лоте Copart
    COPART_IMAGES: str = "images"

    # Селектор для галереи изображений IAAI
    IAAI_GALLERY: str = "div.vehicle-photos"

    # Селектор для изображений в лоте IAAI
    IAAI_IMAGES: str = "images"


class AuctionLimits:
    """
    Auction-related Limits and Timeouts

    Defines constants for controlling auction data retrieval.
    """
    # Максимальное количество фотографий для обработки
    MAX_PHOTOS: int = 10

    # Время ожидания для запросов к аукционам
    REQUEST_TIMEOUT: int = 30


class TelegramConstants:
    """
    Telegram Message Formatting and Constant Values

    Provides predefined message templates, emoji, and configuration
    for Telegram bot interactions.
    """
    # Шаблоны сообщений с поддержкой форматирования
    MESSAGES = {
        'NEW_CAR': (
            "🚙 <b>{title}</b>\n"
            "💵 Цена: ${price:,.2f}\n"
            "🌐 <a href='{url}'>Объявление на AUTO.RIA</a>"
        ),
        'AUCTION_LINK': "🔨 <a href='{auction_url}'>Лот на аукционе</a>",
        'AUCTION_PHOTOS': (
            "📸 Фотографии с аукциона\n"
            "🚙 {title}\n"
            "🔨 <a href='{auction_url}'>Подробнее о лоте</a>"
        ),
        'PRICE_CHANGE': (
            "{price_emoji} <b>Изменение цены</b>\n\n"
            "🚗 {title}\n"
            "💰 Старая цена: ${old_price:,.2f}\n"
            "💰 Новая цена: ${new_price:,.2f}\n"
            "{diff_emoji} Разница: ${price_diff:,.2f}\n\n"
            "🔗 <a href='{url}'>Просмотреть на AUTO.RIA</a>"
        ),
        'CAR_SOLD': (
            "✅ <b>Автомобиль продан</b>\n\n"
            "🚗 {title}\n"
            "💰 Последняя цена: ${price:,.2f}\n\n"
            "🔗 <a href='{url}'>Просмотреть на AUTO.RIA</a>"
        ),
        'ERROR': "⚠️ <b>Error Processing Auction Photos</b>\n\n{error_message}"
    }

    # Заголовки альбомов
    ALBUM_TITLES = {
        'AUTO_RIA': "Фото с AUTO.RIA",
        'AUCTION': "Фото с аукциона"
    }

    # Эмодзи для индикации изменения цены
    PRICE_CHANGE_EMOJI = {
        'INCREASE': '📈',
        'DECREASE': '📉'
    }

    # Эмодзи для разницы в цене
    PRICE_DIFF_EMOJI = {
        'INCREASE': '🔺',
        'DECREASE': '🔻'
    }

    # Задержки между отправкой сообщений (в секундах)
    DELAYS = {
        'BETWEEN_ALBUMS': 10,
        'AFTER_AUCTION_PHOTOS': 5
    }

    # Максимальное количество фото в одном альбоме
    LIMITS = {
        'MAX_PHOTOS': 10
    }

    # Параметры форматирования канала
    CHANNEL = {
        'PREFIX_PUBLIC': '@',
        'PREFIX_PRIVATE': '-100'
    }

    # Параметры сообщений
    MESSAGE_PARAMS = {
        'PARSE_MODE': 'HTML'
    }

class CarServiceConstants:
    """
    Constants for Car Service Configuration and Monitoring

    Provides standard configuration values and threshold settings
    for car tracking and processing.
    """
    # Интервал проверки по умолчанию (в секундах)
    DEFAULT_CHECK_INTERVAL: int = 600

    # Минимальное изменение цены для уведомления
    PRICE_CHANGE_THRESHOLD: float = 1.0

    # Задержка при возникновении ошибки (в секундах)
    ERROR_RETRY_DELAY: int = 60

    # Таймаут для корректного завершения работы
    SHUTDOWN_TIMEOUT: float = 10.0


class CarValidationConstants:
    """
    Validation Constants for Car Data Processing

    Defines required fields and validation rules for car data.
    """
    # Обязательные поля для объявления автомобиля
    REQUIRED_FIELDS: List[str] = ['car_id', 'title', 'price']

    # Максимальное количество фото с аукциона
    MAX_AUCTION_PHOTOS: int = 10



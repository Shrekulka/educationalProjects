# auto_ria_tracker/external_services/auto_ria.py

import asyncio
from urllib.parse import quote

import aiohttp
from typing import Dict, List, Optional
from bs4 import BeautifulSoup, Tag

from config_data.constants import HTTPConstants, AutoRiaDefaults, AutoRiaURLs, AutoRiaSelectors
from logger_config import logger
from utils.proxy_manager import ProxyManager
from utils.retry_handler import RetryHandler

class AutoRiaParser:
    """
    A parser for AUTO.RIA website that extracts car listings data asynchronously.

    This class provides functionality to search and parse car listings based on user settings,
    including handling of proxies, retries, and error management.

    Attributes:
       session (Optional[aiohttp.ClientSession]): Async HTTP session for making requests
       retry_handler (RetryHandler): Handler for managing request retries
       proxy_manager (Optional[ProxyManager]): Manager for rotating proxies if provided

    Type Annotations:
       proxy_list: List[str] - List of proxy URLs in format "http://host:port"
       user_settings: Dict[str, Union[str, int, bool]] - User search parameters
       return: List[Dict] - List of parsed car data dictionaries
    """

    def __init__(self, proxy_list: List[str] = None)-> None:
        """
        Initialize the parser with optional proxy support.

        This class provides functionality to search and parse car listings based on user settings,
        including handling of proxies, retries, and error management.

        Args:
            proxy_list: Optional list of proxy servers to use for requests
                       Format: ["http://host:port", ...]

        Attributes:
            session (Optional[aiohttp.ClientSession]): Async HTTP session for making requests
            retry_handler (RetryHandler): Handler for managing request retries
            proxy_manager (Optional[ProxyManager]): Manager for rotating proxies if provided
        """
        # Инициализация парсера с опциональным списком прокси
        self.session: Optional[aiohttp.ClientSession] = None
        self.retry_handler = RetryHandler()
        self.proxy_manager = ProxyManager(proxy_list) if proxy_list else None

    async def __aenter__(self) -> 'AutoRiaParser':
        """
        Async context manager entry point. Initializes HTTP session.

        Creates an aiohttp ClientSession with SSL verification settings.
        This method is called automatically when entering an async context.

        Returns:
            AutoRiaParser: Instance of the parser with initialized session

        Example:
            async with AutoRiaParser() as parser:
                results = await parser.get_cars(settings)
        """

        # Создание асинхронной сессии при входе в контекстный менеджер
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=HTTPConstants.SSL_VERIFY)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb)-> None:
        """
        Async context manager exit point. Closes HTTP session.

        Ensures proper cleanup of resources by closing the aiohttp session.
        This method is called automatically when exiting an async context.

        Args:
            exc_type: The type of the exception that was raised
            exc_val: The instance of the exception that was raised
            exc_tb: The traceback of the exception that was raised
        """
        # Закрытие сессии при выходе из контекстного менеджера
        if self.session:
            await self.session.close()

    def _build_search_url(self, user_settings: Dict) -> str:
        """
        Constructs a search URL based on user settings.

        This method builds a complete search URL for AUTO.RIA by combining the base URL
        with query parameters obtained from the user's search settings.

        Args:
            user_settings: A dictionary containing search parameters:
                model (str): Car model (e.g., 'SEQUOIA', 'TUNDRA', 'LAND_CRUISER')
                accident (bool): Whether to include cars that have been in an accident (True - include, False - exclude)
                import_usa (bool): Filter for cars from the USA (True - only from the USA, False - not from the USA)

        Returns:
            str: The complete search URL with applied filter parameters

        Raises:
            ValueError: If the settings contain invalid value types
        """
        # Формирование URL для поиска на основе пользовательских настроек
        if not all(isinstance(v, (str, int, bool)) for v in user_settings.values()):
            raise ValueError("Invalid settings values")

        # Добавление параметра модели автомобиля
        model = user_settings.get('model', AutoRiaDefaults.DEFAULT_MODEL).upper()

        # Проверяем существование модели в словаре
        if model not in AutoRiaDefaults.MODEL_IDS:
            logger.warning(f"Model {model} not found in MODEL_IDS dictionary")
            model = AutoRiaDefaults.DEFAULT_MODEL

        # Установка базовых параметров поиска
        params = {
            'indexName': 'auto,order_auto,newauto_search',
            'categories.main.id': AutoRiaDefaults.CATEGORY_ID,
            'brand.id[0]': AutoRiaDefaults.MARKA_ID,
            'model.id[0]': AutoRiaDefaults.MODEL_IDS.get(model),
            'price.currency': 1,
        }

        # Обработка фильтра по авто из США
        if 'import_usa' in user_settings:
            params['country.import.usa.not'] = (
                AutoRiaDefaults.ABROAD_VALUES['NON_USA']
                if not user_settings['import_usa']
                else AutoRiaDefaults.ABROAD_VALUES['USA_ONLY']
            )

        # Обработка фильтра по ДТП
        if 'accident' in user_settings:
            params['damage.not'] = (
                AutoRiaDefaults.DAMAGE_VALUES['NO_ACCIDENT']
                if not user_settings['accident']
                else AutoRiaDefaults.DAMAGE_VALUES['WITH_ACCIDENT']
            )
        # Сборка конечного URL
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())

        logger.debug(f"Built URL parameters: {params}")
        url = f"{AutoRiaURLs.SEARCH_URL}?{query_string}"
        logger.debug(f"Final search URL: {url}")
        return url

    async def get_cars(self, user_settings: Dict) -> List[Dict]:
        """
        Retrieves and parses car listings based on search settings.

        This is the main method for fetching a list of cars from AUTO.RIA. It handles the entire
        process of searching, loading, and parsing car data.

        Args:
            user_settings: A dictionary containing search parameters:
                model (str): Car model (e.g., 'SEQUOIA')
                accident (bool): Whether to include cars that have been in an accident
                import_usa (bool): Filter for cars from the USA

        Returns:
            List[Dict]: A list of dictionaries containing car data, where each dictionary includes:
                - car_id (int): Unique identifier of the listing
                - url (str): Full URL of the listing
                - title (str): Title/description of the car
                - price (float): Car price
                - photos (List[str]): List of photo URLs
                - auction_url (Optional[str]): Auction URL (if available)
                - model (str): Car model in uppercase

        Notes:
            - The method automatically handles missing photos and invalid data
            - Photo URLs are encoded for safe transmission
            - If no model is specified in the settings, the default value DEFAULT_MODEL is used
            - All errors are logged but do not interrupt the method's execution
        """
        # Получение списка автомобилей по заданным параметрам
        try:
            # Получение URL для поиска
            url = self._build_search_url(user_settings)
            html = await self._fetch_page(url)

            if not html:
                logger.error("Failed to fetch page from AUTO.RIA")
                return []

            # Инициализация парсера HTML
            soup = BeautifulSoup(html, 'html.parser')
            cars = []

            # Поиск результатов на странице
            search_results = soup.select(AutoRiaSelectors.SEARCH_RESULTS)
            if not search_results:
                logger.warning(f"No search results found. URL: {url}")
                logger.debug(f"Page content length: {len(html)}")
                return []

            # Обработка каждого найденного объявления
            for card in search_results:
                try:
                    logger.debug(f"HTML карточки: {card}")

                    # Извлечение ID автомобиля из карточки
                    car_id = None
                    id_elem = card.select_one(AutoRiaSelectors.CAR_ID)
                    if id_elem:
                        car_id = int(id_elem.get('data-autoid', '0'))

                    # Проверка наличия ID
                    if not car_id:
                        logger.warning(f"Could not extract car ID from card: {card}")
                        continue

                    # Извлечение основной информации об автомобиле
                    title_elem = card.select_one(AutoRiaSelectors.TITLE)
                    price_elem = card.select_one(AutoRiaSelectors.PRICE)

                    # Проверка наличия обязательных элементов
                    if not title_elem or not price_elem:
                        logger.warning(f"Missing required elements in card: {car_id}")
                        continue

                    # Извлечение и проверка цены
                    price_value = float(price_elem.get('data-main-price', '0'))
                    if price_value == 0:
                        logger.warning(f"Invalid price value for car ID: {car_id}")
                        continue

                    # Получение фотографий автомобиля
                    photos = await self._extract_photos(card)
                    logger.debug(f"Отправляем фото в Telegram: {photos}")

                    logger.debug(f"Found {len(photos)} photos: {photos}")

                    valid_photos = [photo for photo in photos if photo.startswith('http')]
                    if not valid_photos:
                        logger.error("Нет валидных фото для отправки в Telegram")
                        continue

                    # Кодируем URL
                    encoded_photos = [quote(photo, safe=':/') for photo in valid_photos]
                    logger.debug(f"Закодированные фото URL: {encoded_photos}")

                    # Формирование данных об автомобиле
                    car_data = {
                        'car_id': car_id,
                        'url': card.select_one(AutoRiaSelectors.LINK)['href'],
                        'title': title_elem.text.strip(),
                        'price': price_value,
                        'photos': encoded_photos,
                        'auction_url': None,
                        'model': user_settings.get('model', AutoRiaDefaults.DEFAULT_MODEL).upper()
                    }

                    cars.append(car_data)
                    logger.debug(f"Successfully parsed car: {car_data['title']}")

                except (AttributeError, KeyError, ValueError) as e:
                    logger.error(f"Error parsing car card: {e}")
                    continue

            logger.info(f"Found {len(cars)} cars")
            return cars

        except Exception as e:
            logger.error(f"Unexpected error in get_cars: {e}")
            return []

    def _extract_car_id(self, card: Tag) -> Optional[int]:
        """
        Extracts car ID from a listing card using multiple strategies.

        Attempts to find the car ID first in data attributes, then falls back
        to parsing it from the listing URL if necessary.

        Args:
           card: BeautifulSoup Tag object containing car listing HTML

        Returns:
           Optional[int]: Car ID if found, None otherwise
        """
        # Извлечение ID автомобиля из карточки объявления различными способами
        try:
            # Попытка найти ID в data-атрибуте
            id_elem = card.select_one(AutoRiaSelectors.CAR_ID)
            if id_elem and 'data-autoid' in id_elem.attrs:
                return int(id_elem['data-autoid'])

            # Попытка извлечь ID из URL объявления
            link = card.select_one(AutoRiaSelectors.LINK)
            if link and 'href' in link.attrs:
                href = link['href']
                car_id = href.split('_')[-1].replace(
                    AutoRiaDefaults.FILE_EXTENSIONS['HTML'],
                    ''
                )
                return int(car_id)
            return None
        except Exception as e:
            logger.error(f"Ошибка при извлечении ID автомобиля: {e}")
            return None

    async def _extract_photos(self, card: Tag) -> List[str]:
        """
        Улучшенный метод извлечения фотографий с несколькими стратегиями получения фото
        """
        try:
            # Получение ID автомобиля
            car_id = self._extract_car_id(card)
            if not car_id:
                logger.error("Не удалось получить ID автомобиля")
                return []

            # Попытка получить фото различными способами
            photos = []

            # 1. Попытка через API
            api_photos = await self._fetch_photos_from_api(car_id)
            if api_photos:
                logger.debug(f"Получены фото через API: {len(api_photos)}")
                return api_photos

            # 2. Попытка через HTML страницу объявления
            html_photos = await self._extract_photos_from_html(car_id)
            if html_photos:
                logger.debug(f"Получены фото через HTML: {len(html_photos)}")
                return html_photos

            # 3. Получение основного фото из карточки
            main_photo = self._extract_main_photo(card)
            if main_photo:
                logger.debug("Получено основное фото из карточки")
                return [main_photo]

            logger.warning(f"Не удалось получить фотографии для авто {car_id}")
            return []

        except Exception as e:
            logger.error(f"Ошибка при извлечении фотографий: {e}")
            return []

    async def _fetch_photos_from_api(self, car_id: int) -> List[str]:
        """
        Улучшенный метод получения фотографий через API с расширенной обработкой ошибок
        """
        try:
            api_url = AutoRiaURLs.get_photos_api_url(car_id)
            logger.debug(f"Запрос к API фотографий: {api_url}")

            # Добавляем дополнительные заголовки для аутентификации
            headers = HTTPConstants.HEADERS.copy()
            headers['Referer'] = AutoRiaURLs.get_car_url(car_id)

            async with self.session.get(
                    api_url,
                    headers=headers,
                    timeout=HTTPConstants.REQUEST_TIMEOUT
            ) as response:
                # Расширенная обработка статусов
                if response.status == HTTPConstants.STATUS_OK:
                    data = await response.json()

                    # Извлечение и обработка URL фотографий
                    photos = []
                    if isinstance(data, dict):
                        photo_list = data.get('data', {}).get('photos', [])
                        for photo in photo_list:
                            photo_id = photo.get('photoId')
                            if photo_id:
                                photo_url = AutoRiaURLs.get_photo_url(car_id, photo_id)
                                if photo_url not in photos:  # Избегаем дубликатов
                                    photos.append(photo_url)

                    if photos:
                        logger.debug(f"Успешно получено {len(photos)} фото через API")
                        return photos
                    else:
                        logger.warning("API вернул пустой список фотографий")
                        return []

                elif response.status == HTTPConstants.STATUS_NOT_FOUND:
                    logger.info(f"Объявление {car_id} не найдено в API")
                    return []
                else:
                    logger.warning(f"API вернул неожиданный статус {response.status}")
                    return []

        except asyncio.TimeoutError:
            logger.error(f"Таймаут при запросе к API для авто {car_id}")
            return []
        except Exception as e:
            logger.error(f"Ошибка при получении фото через API: {e}")
            return []

    async def _extract_photos_from_html(self, car_id: int) -> List[str]:
        """
        Улучшенный метод извлечения фотографий из HTML с поддержкой разных форматов
        """
        try:
            url = AutoRiaURLs.get_car_url(car_id)
            logger.debug(f"Запрос HTML страницы: {url}")

            async with self.session.get(
                    url,
                    headers=HTTPConstants.HEADERS,
                    timeout=HTTPConstants.REQUEST_TIMEOUT
            ) as response:
                if response.status == HTTPConstants.STATUS_OK:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    photos = []
                    # Поиск фотографий в разных форматах
                    for selector in AutoRiaSelectors.GALLERY_SELECTORS:
                        elements = soup.select(selector)
                        for element in elements:
                            # Проверяем различные атрибуты
                            for attr in AutoRiaSelectors.PHOTO_ATTRS:
                                photo_url = element.get(attr, '')
                                if photo_url:
                                    # Преобразование URL для получения полноразмерного изображения
                                    for preview, full in AutoRiaDefaults.IMAGE_FORMATS.items():
                                        photo_url = photo_url.replace(preview, full)

                                    if photo_url not in photos:
                                        photos.append(photo_url)

                    if photos:
                        logger.debug(f"Найдено {len(photos)} фото в HTML")
                        return photos
                    else:
                        logger.warning("Не найдено фотографий в HTML")
                        return []
                else:
                    logger.warning(f"Не удалось получить HTML страницу, статус: {response.status}")
                    return []

        except Exception as e:
            logger.error(f"Ошибка при извлечении фото из HTML: {e}")
            return []

    def _extract_main_photo(self, card: Tag) -> Optional[str]:
        """
        Улучшенный метод извлечения основного фото с поддержкой разных форматов
        """
        try:
            # Поиск элемента picture
            picture = card.select_one(AutoRiaSelectors.MAIN_PHOTO_PICTURE)
            if picture:
                # Пробуем найти WebP версию
                webp_source = picture.select_one(AutoRiaSelectors.MAIN_PHOTO_WEBP)
                if webp_source and webp_source.get('srcset'):
                    photo_url = webp_source['srcset'].strip()
                    return self._convert_to_full_size(photo_url)

                # Пробуем найти JPG версию
                img = picture.select_one(AutoRiaSelectors.MAIN_PHOTO_IMG)
                if img and img.get('src'):
                    photo_url = img['src'].strip()
                    return self._convert_to_full_size(photo_url)

            # Если picture не найден, ищем прямые images теги
            img = card.select_one('images[src]')
            if img and img.get('src'):
                return self._convert_to_full_size(img['src'].strip())

            return None

        except Exception as e:
            logger.error(f"Ошибка при извлечении основного фото: {e}")
            return None

    def _convert_to_full_size(self, url: str) -> str:
        """
        Новый вспомогательный метод для конвертации URL превью в полноразмерное изображение
        """
        for preview, full in AutoRiaDefaults.IMAGE_FORMATS.items():
            url = url.replace(preview, full)
        return url

    async def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetches page content with retry support.

        Makes HTTP request to fetch page content, implementing retry logic
        for failed requests.

        Args:
            url: Target URL to fetch

        Returns:
            Optional[str]: Page HTML content or None if failed after all retries

        Notes:
            - Uses retry handler for failed requests
            - Includes proper error logging
            - Requires initialized session
        """

        # Получение содержимого страницы с механизмом повторных попыток
        if not self.session:
            return None

        try:
            return await self.retry_handler.execute(self._make_request, url)
        except Exception as e:
            logger.error(f"Failed to fetch page after all retries: {e}")
            return None

    async def _make_request(self, url: str) -> Optional[str]:
        """
        Makes HTTP request with proxy support and handles response.

        Low-level method for making HTTP requests, including proxy rotation
        and response handling.

        Args:
            url: Target URL

        Returns:
            Optional[str]: Response text or None if request failed

        Notes:
            - Handles proxy rotation if proxy manager is configured
            - Implements proper timeout handling
            - Includes rate limiting detection and handling
            - Uses standard headers for requests
        """
        # Выполнение HTTP-запроса с поддержкой прокси
        proxy = None
        if self.proxy_manager:
            proxy = self.proxy_manager.get_next_proxy()

        # Выполнение запроса с установленными параметрами
        async with self.session.get(
                url,
                timeout=HTTPConstants.REQUEST_TIMEOUT,
                headers=HTTPConstants.HEADERS,
                proxy=proxy
        ) as response:
            if response.status == HTTPConstants.STATUS_OK:
                return await response.text()
            elif response.status == HTTPConstants.STATUS_TOO_MANY_REQUESTS:
                await asyncio.sleep(HTTPConstants.RETRY_DELAY)
            return None

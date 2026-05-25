# auto_ria_tracker/external_services/auction_service.py

from typing import List, Optional

import aiohttp
from bs4 import BeautifulSoup

from config_data.constants import (
    AuctionLimits,
    AuctionURLs,
    AuctionHTMLSelectors,
    HTTPConstants
)
from logger_config import logger


class AuctionPhotoService:
    """Service for retrieving auction lot photos from Copart and IAAI platforms.
    Supports asynchronous photo fetching with error handling and limits.
    Provides context management for session handling.
    """

    def __init__(self)-> None:
        """Initializes the AuctionPhotoService with an optional ClientSession."""
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Creates an asynchronous ClientSession with predefined headers upon entering the context."""
        self.session = aiohttp.ClientSession(headers=HTTPConstants.HEADERS)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the ClientSession upon exiting the context to free resources."""
        if self.session:
            await self.session.close()

    async def get_auction_photos(self, lot_number: str) -> List[str]:
        """Retrieves auction photos by lot number with a fallback mechanism.

        Tries to fetch photos from Copart first. If no photos are found,
        it attempts to fetch from IAAI. Limits the number of returned photos
        to the maximum defined in AuctionLimits.

        Args:
            lot_number: The auction lot number to fetch photos for.

        Returns:
            A list of photo URLs. If no photos are found, returns an empty list.

        Raises:
            Exception: If an error occurs during photo retrieval.
        """
        photos = []
        try:
            # Попытка получить фотографии с Copart
            photos = await self._get_copart_photos(lot_number)
            # Если фотографии не найдены, пробуем IAAI
            if not photos:
                photos = await self._get_iaai_photos(lot_number)
        except Exception as e:
            logger.error(f"Error fetching all auction photos for lot {lot_number}: {e}")
            # Возвращаем не более максимального количества фотографий
        return photos[:AuctionLimits.MAX_PHOTOS]

    async def _get_copart_photos(self, lot_number: str) -> List[str]:
        """Retrieves photos from the Copart auction platform.

        Constructs the Copart lot URL, sends an asynchronous GET request,
        parses the HTML response, and extracts photo URLs from the gallery.

        Args:
            lot_number: The Copart auction lot number.

        Returns:
            A list of photo URLs if successful; otherwise, an empty list.

        Raises:
            Exception: If an error occurs during the request or parsing.
        """
        # Проверка наличия сессии
        if not self.session:
            logger.error("No active session")
            return []

        try:
            # Формирование URL для лота Copart
            url = AuctionURLs.get_copart_lot_url(lot_number)
            # Отправка асинхронного GET-запроса
            async with self.session.get(url, timeout=AuctionLimits.REQUEST_TIMEOUT) as response:
                # Проверка статуса ответа
                if response.status != HTTPConstants.STATUS_OK:
                    return []

                # Парсинг HTML-страницы
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                # Поиск элемента галереи
                gallery = soup.find('div', class_=AuctionHTMLSelectors.COPART_GALLERY)

                # Извлечение ссылок на фотографии из галереи
                return await self._parse_photos_from_gallery(gallery, AuctionHTMLSelectors.COPART_IMAGES)

        except Exception as e:
            logger.error(f"Error fetching Copart photos for lot {lot_number}: {e}")
            return []

    async def _get_iaai_photos(self, lot_number: str) -> List[str]:
        """Retrieves photos from the IAAI auction platform.

        Constructs the IAAI lot URL, sends an asynchronous GET request,
        parses the HTML response, and extracts photo URLs from the gallery.

        Args:
            lot_number: The IAAI auction lot number.

        Returns:
            A list of photo URLs if successful; otherwise, an empty list.

        Raises:
            Exception: If an error occurs during the request or parsing.
        """
        # Проверка наличия сессии
        if not self.session:
            logger.error("No active session")
            return []

        try:
            # Формирование URL для лота IAAI
            url = AuctionURLs.get_iaai_lot_url(lot_number)
            # Отправка асинхронного GET-запроса
            async with self.session.get(url, timeout=AuctionLimits.REQUEST_TIMEOUT) as response:
                # Проверка статуса ответа
                if response.status != HTTPConstants.STATUS_OK:
                    return []

                # Парсинг HTML-страницы
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                # Поиск элемента галереи
                gallery = soup.find('div', class_=AuctionHTMLSelectors.IAAI_GALLERY)

                # Извлечение ссылок на фотографии из галереи
                return await self._parse_photos_from_gallery(gallery, AuctionHTMLSelectors.IAAI_IMAGES)

        except Exception as e:
            logger.error(f"Error fetching IAAI photos for lot {lot_number}: {e}")
            return []

    @staticmethod
    async def _parse_photos_from_gallery(gallery: BeautifulSoup, image_selector: str) -> List[str]:
        """Extracts photo URLs from the provided gallery element.

        Searches for all image elements matching the selector within the gallery.
        Collects and returns their 'src' attributes.

        Args:
            gallery: The BeautifulSoup object representing the gallery.
            image_selector: The CSS selector for image elements.

        Returns:
            A list of image URLs. If no images are found, returns an empty list.
        """
        photos = []
        # Если галерея найдена, начинаем поиск изображений
        if gallery:
            # Поиск всех элементов изображений по селектору
            for img in gallery.find_all(image_selector):
                # Добавление ссылки на фотографию, если атрибут 'src' существует
                if 'src' in img.attrs:
                    photos.append(img['src'])
        return photos

    @staticmethod
    def extract_lot_number(auction_url: str) -> Optional[str]:
        """Extracts the lot number from the provided auction URL.

        Splits the URL to isolate the lot number segment.

        Args:
            auction_url: The URL of the auction lot.

        Returns:
            The extracted lot number if successful; otherwise, None.

        Raises:
            Exception: If URL parsing fails.
        """
        try:
            # Разбиение URL для извлечения номера лота
            return auction_url.split(f"/{AuctionURLs.LOT_PATH}/")[-1].split('/')[0]
        except Exception:
            return None
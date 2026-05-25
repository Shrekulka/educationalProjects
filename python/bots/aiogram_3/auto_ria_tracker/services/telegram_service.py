# auto_ria_tracker/services/telegram_service.py

import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InputMediaPhoto
from typing import Dict, Any, List

from config_data.constants import TelegramConstants
from external_services.auction_service import AuctionPhotoService
from logger_config import logger


class TelegramService:
    """
    A service class for handling Telegram messaging operations.

    This class provides functionality to send car-related messages, photos,
    and notifications to a specified Telegram channel.

    Attributes:
       bot (Bot): Aiogram Bot instance for sending messages
       channel_id (str): Target channel identifier where messages will be sent
    """

    def __init__(self, bot: Bot, channel_id: str)-> None:
        """
        Initialize the TelegramService with a bot instance and channel ID.

        Args:
            bot (Bot): Aiogram Bot instance
            channel_id (str): Channel identifier where messages will be sent
        """
        self.bot = bot

        # Проверяем и форматируем ID канала
        if not (channel_id.startswith(TelegramConstants.CHANNEL['PREFIX_PUBLIC']) or
                channel_id.startswith(TelegramConstants.CHANNEL['PREFIX_PRIVATE'])):
            self.channel_id = f"{TelegramConstants.CHANNEL['PREFIX_PUBLIC']}{channel_id}"
            logger.info(f"Channel ID modified to: {self.channel_id}")
        else:
            self.channel_id = channel_id
            logger.info(f"Channel ID initialized: {self.channel_id}")

    async def send_new_car(self, car_data: Dict[str, Any]) -> bool:
        """
        Send information about a new car including photos from both AUTO.RIA and auction.

        Args:
            car_data (Dict[str, Any]): Dictionary containing car information including:
                - title: Car title/name
                - price: Car price
                - url: AUTO.RIA listing URL
                - photos: List of AUTO.RIA photo URLs
                - auction_url: Auction listing URL (optional)
                - auction_photos: List of auction photo URLs (optional)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"Starting data transmission for {car_data['title']}")

            # Формируем основной текст объявления
            main_caption = self._format_main_caption(car_data)

            try:
                # Отправляем основные фото с AUTO.RIA
                if car_data.get('photos'):
                    photos = car_data['photos'][:TelegramConstants.LIMITS['MAX_PHOTOS']]
                    await self._send_photo_album(
                        photos=photos,
                        caption=main_caption,
                        title=TelegramConstants.ALBUM_TITLES['AUTO_RIA']
                    )
                    try:
                        await asyncio.sleep(TelegramConstants.DELAYS['BETWEEN_ALBUMS'])
                    except asyncio.CancelledError:
                        logger.info(f"Cancelled during delay after AUTO.RIA photos for {car_data['title']}")
                        raise

                # Отправляем фото с аукциона при наличии
                if car_data.get('auction_photos'):
                    auction_caption = self._format_auction_caption(car_data)
                    auction_photos = car_data['auction_photos'][:TelegramConstants.LIMITS['MAX_PHOTOS']]
                    await self._send_photo_album(
                        photos=auction_photos,
                        caption=auction_caption,
                        title=TelegramConstants.ALBUM_TITLES['AUCTION']
                    )
                    try:
                        await asyncio.sleep(TelegramConstants.DELAYS['AFTER_AUCTION_PHOTOS'])
                    except asyncio.CancelledError:
                        logger.info(f"Cancelled during delay after auction photos for {car_data['title']}")
                        raise

                logger.info(f"Successfully sent all data for {car_data['title']}")
                return True

            except asyncio.CancelledError:
                logger.info(f"Data transmission cancelled for {car_data['title']}")
                raise

            except Exception as e:
                logger.error(f"Error during photo sending for {car_data['title']}: {str(e)}")
                await self.send_error_notification(
                    f"Error sending photos for {car_data['title']}: {str(e)}"
                )
                return False

        except asyncio.CancelledError:
            logger.info(f"Data transmission cancelled during initialization for {car_data['title']}")
            raise

        except Exception as e:
            logger.error(f"Error in send_new_car for {car_data['title']}: {str(e)}")
            await self.send_error_notification(
                f"Error in advertisement processing for {car_data['title']}: {str(e)}"
            )
            return False

    async def _send_photo_album(self, photos: List[str], caption: str, title: str) -> bool:
        """
        Send a photo album with caption for the first photo.

        Args:
            photos (List[str]): List of photo URLs to send
            caption (str): Caption text for the first photo
            title (str): Album title for logging purposes

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not photos:
                logger.warning(f"No photos available to send for album '{title}'")
                return False

            logger.info(f"Preparing album '{title}' with {len(photos)} photos")

            # Создаем медиагруппу
            media_group = []

            # Добавляем первое фото с подписью
            media_group.append(
                InputMediaPhoto(
                    media=photos[0],
                    caption=caption,
                    parse_mode=TelegramConstants.MESSAGE_PARAMS['PARSE_MODE']
                )
            )

            # Добавляем остальные фото без подписи
            for photo_url in photos[1:]:
                media_group.append(
                    InputMediaPhoto(media=photo_url)
                )

            # Отправляем альбом
            await self.bot.send_media_group(
                chat_id=self.channel_id,
                media=media_group
            )

            logger.info(f"Album '{title}' sent successfully")
            return True

        except TelegramRetryAfter as e:
            logger.warning(f"Flood control: retry after {e.retry_after} seconds")
            await asyncio.sleep(e.retry_after)
            return await self._send_photo_album(photos, caption, title)

        except Exception as e:
            logger.error(f"Error sending album '{title}': {str(e)}")
            return False

    def _format_main_caption(self, car_data: Dict[str, Any]) -> str:
        """
        Format the main caption for car listing.

        Args:
            car_data (Dict[str, Any]): Car information dictionary

        Returns:
            str: Formatted HTML caption text
        """
        # Формируем базовый текст объявления
        caption = TelegramConstants.MESSAGES['NEW_CAR'].format(
            title=car_data['title'],
            price=car_data['price'],
            url=car_data['url']
        )
        # Добавляем ссылку на лот на аукционе, если она есть
        if car_data.get('auction_url'):
            caption += "\n" + TelegramConstants.MESSAGES['AUCTION_LINK'].format(auction_url=car_data['auction_url'])

        return caption

    def _format_auction_caption(self, car_data: Dict[str, Any]) -> str:
        """
        Format the caption for auction photos.

        Args:
            car_data (Dict[str, Any]): Car information dictionary

        Returns:
            str: Formatted HTML caption text
        """
        # Возвращаем отформатированное сообщение для фото с аукциона
        return TelegramConstants.MESSAGES['AUCTION_PHOTOS'].format(
            title=car_data['title'],
            auction_url=car_data['auction_url']
        )

    async def send_error_notification(self, error_message: str) -> bool:
        """
        Send error notification to the channel.

        Args:
            error_message (str): Error message to send

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Форматируем сообщение об ошибке, подставляя текст ошибки
            message = TelegramConstants.MESSAGES['ERROR'].format(error_message=error_message)
            # Отправляем сообщение в Telegram канал
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=TelegramConstants.MESSAGE_PARAMS['PARSE_MODE']
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")
            return False

    async def send_price_change(self, car_data: Dict[str, Any], old_price: float, new_price: float) -> bool:
        """
        Send notification about price change.

        Args:
            car_data (Dict[str, Any]): Car information dictionary
            old_price (float): Previous price
            new_price (float): New price

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Вычисляем разницу между новой и старой ценой
            price_diff = new_price - old_price

            # Выбираем эмодзи для индикатора изменения цены:
            price_emoji = (TelegramConstants.PRICE_CHANGE_EMOJI['INCREASE']
                           if price_diff > 0
                           else TelegramConstants.PRICE_CHANGE_EMOJI['DECREASE'])
            # Выбираем эмодзи для отображения разницы:
            diff_emoji = (TelegramConstants.PRICE_DIFF_EMOJI['INCREASE']
                          if price_diff > 0
                          else TelegramConstants.PRICE_DIFF_EMOJI['DECREASE'])

            # Формируем текст сообщения
            message = TelegramConstants.MESSAGES['PRICE_CHANGE'].format(
                price_emoji=price_emoji,
                title=car_data['title'],
                old_price=old_price,
                new_price=new_price,
                diff_emoji=diff_emoji,
                price_diff=abs(price_diff),
                url=car_data['url']
            )

            # Отправляем сообщение в Telegram канале
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=TelegramConstants.MESSAGE_PARAMS['PARSE_MODE']
            )
            return True

        except Exception as e:
            logger.error(f"Error sending price change notification: {e}")
            return False

    async def send_car_sold(self, car_data: Dict[str, Any]) -> bool:
        """
        Send notification about car being sold.

        Args:
            car_data (Dict[str, Any]): Car information dictionary

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Формируем текст сообщения о продаже
            message = TelegramConstants.MESSAGES['CAR_SOLD'].format(
                title=car_data['title'],
                price=car_data['price'],
                url=car_data['url']
            )

            # Отправляем сообщение в Telegram канале
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=TelegramConstants.MESSAGE_PARAMS['PARSE_MODE']
            )
            return True

        except Exception as e:
            logger.error(f"Error sending car sold notification: {e}")
            return False

    async def send_auction_photos(self, car_data: Dict[str, Any]) -> bool:
        """
        Send auction photos for a car.

        Args:
            car_data (Dict[str, Any]): Car information dictionary containing auction_url

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with AuctionPhotoService() as auction_service:
                # Извлекаем номер лота из URL аукциона
                lot_number = auction_service.extract_lot_number(car_data['auction_url'])
                if not lot_number:
                    return False

                # Получаем фотографии с аукциона
                photos = await auction_service.get_auction_photos(lot_number)
                if not photos:
                    return False

                # Формируем подпись для фотографий с аукциона
                caption = TelegramConstants.MESSAGES['AUCTION_PHOTOS'].format(
                    title=car_data['title'],
                    auction_url=car_data['auction_url']
                )

                # Формируем медиагруппу
                media = [
                    InputMediaPhoto(
                        media=photo,
                        caption=caption if i == 0 else None,
                        parse_mode=TelegramConstants.MESSAGE_PARAMS['PARSE_MODE'] if i == 0 else None
                    ) for i, photo in enumerate(photos[:TelegramConstants.LIMITS['MAX_PHOTOS']])
                ]

                # Отправляем фотографии
                await self.bot.send_media_group(
                    chat_id=self.channel_id,
                    media=media
                )
                return True
        except Exception as e:
            logger.error(f"Error sending auction photos: {e}")
            return False
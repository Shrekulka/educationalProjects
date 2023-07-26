import logging
import asyncio
from typing import List, Dict
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from modules.video_search import VideoSearch


class TelegramBot:
    """Класс TelegramBot для отправки видео на Telegram.

    Атрибуты:
        bot_token (str): Токен Telegram бота для доступа к API.
        chat_id (int): Идентификатор чата, в который будет отправляться видео.
        video_search (VideoSearch): Объект класса VideoSearch для поиска видео на YouTube.

    Методы:
        send_video(video_id: str) -> None:
            Асинхронно отправляет видео по его идентификатору на Telegram.
        send_videos_periodically(videos: List[Dict]) -> None:
            Асинхронно отправляет список видео на Telegram с периодичностью в 3 часа.
        on_startup() -> None:
            Асинхронно запускает Telegram бота.
        on_shutdown() -> None:
            Асинхронно останавливает Telegram бота и закрывает aiohttp.ClientSession.
    """

    def __init__(self, bot_token: str, chat_id: int, video_search: VideoSearch):
        """Инициализация объекта TelegramBot.

        Args:
            bot_token (str): Токен Telegram бота для доступа к API.
            chat_id (int): Идентификатор чата, в который будет отправляться видео.
            video_search (VideoSearch): Объект класса VideoSearch для поиска видео на YouTube.
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.video_search = video_search
        self.bot = Bot(token=self.bot_token)
        self.dp = Dispatcher(self.bot)
        self.dp.middleware.setup(LoggingMiddleware())

    async def send_video(self, video_id: str) -> None:
        """
        Асинхронно отправляет видео по его идентификатору на Telegram.

        Args:
            video_id (str): Идентификатор видео на YouTube.
        """
        try:
            print("Sending video to Telegram...")

            # Формируем URL видео на YouTube
            url = f"https://youtu.be/{video_id}"

            # Создаем подпись для сообщения с ссылкой на видео
            caption = f"Video link: {url}"

            # Отправляем сообщение с ссылкой на видео по указанному chat_id
            await self.bot.send_message(chat_id=self.chat_id, text=caption)

            print("Video successfully sent to Telegram.")
        except Exception as e:
            # В случае ошибки, логируем сообщение об ошибке
            logging.error(f"Error sending video to Telegram: {e}")

    async def send_videos_periodically(self, videos: List[Dict]) -> None:
        """
        Асинхронно отправляет список видео на Telegram с периодичностью в 3 часа.

        Args:
            videos (List[Dict]): Список с информацией о видео.
        """
        for video_data in videos:
            # Извлекаем идентификатор видео из объекта 'id'
            video_id = video_data['id']['videoId']

            # Отправляем видео на Telegram, используя метод send_video
            await self.send_video(video_id)

            # Ожидаем 3 часа перед отправкой следующего видео
            await asyncio.sleep(3 * 60 * 60)

    async def on_startup(self) -> None:
        """
        Асинхронно запускает Telegram бота.
        """
        try:
            print("Starting the bot...")
            # Запускаем бота методом start_polling
            await self.dp.start_polling()
        except Exception as e:
            # В случае ошибки выводим сообщение об ошибке и логируем ее
            logging.error(f"Error starting the bot: {e}")

    async def on_shutdown(self) -> None:
        """
        Асинхронно останавливает Telegram бота и закрывает aiohttp.ClientSession.
        """
        try:
            print("Stopping the bot...")
            # Закрываем хранилище (storage) бота
            await self.dp.storage.close()
            # Ждем завершения работы хранилища
            await self.dp.storage.wait_closed()
            # Закрываем сессию aiohttp.ClientSession для освобождения ресурсов
            self.bot.session.connector._closed = True
        except Exception as e:
            # В случае ошибки выводим сообщение об ошибке и логируем ее
            logging.error(f"Error stopping the bot: {e}")

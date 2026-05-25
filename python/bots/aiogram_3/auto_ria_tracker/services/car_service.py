# auto_ria_tracker/services/car_service.py

import asyncio
import sqlite3
from decimal import Decimal
from typing import Dict, List, Set, Union

import aiohttp

from config_data.constants import CarValidationConstants, CarServiceConstants, AutoRiaDefaults, AutoRiaURLs, \
    HTTPConstants
from database.database import Database
from external_services.auction_service import AuctionPhotoService
from external_services.auto_ria import AutoRiaParser
from logger_config import logger
from services.telegram_service import TelegramService


class CarService:
    """
    A service for tracking and processing car listings from Auto RIA.

    This class provides functionality to:
    - Monitor new car listings
    - Track price changes
    - Detect sold cars
    - Send notifications via Telegram
    - Manage background monitoring process
    """
    def __init__(self, database: Database, telegram_service: TelegramService, check_interval: int = CarServiceConstants.DEFAULT_CHECK_INTERVAL) -> None:
        # Инициализация сервиса с базой данных и службой уведомлений
        self.database = database                  # Подключение к базе данных
        self.telegram_service = telegram_service  # Служба отправки уведомлений
        self.check_interval = check_interval      # Интервал проверки обновлений
        self.is_running = False                   # Флаг активности мониторинга
        self.monitoring_task = None               # Задача фонового мониторинга

    async def process_new_cars(self, cars: List[Dict], user_id: int) -> None:
        """
        Processes and handles new car listings with enhanced error handling and transactional approach.

        Args:
            cars (List[Dict]): List of dictionaries containing car data to be processed. Each dictionary includes car details
                              such as title, price, car_id, auction_url, etc.
            user_id (int): ID of the user whose cars are being processed.

        Workflow:
        1. Retrieve currently active cars from the database
        2. Filter and validate new cars
        3. For each new car:
            a. Validate required fields using CarValidationConstants
            b. If car has auction URL:
                - Extract lot number
                - Retrieve and process auction photos
                - Limit photos to MAX_AUCTION_PHOTOS
            c. Begin transaction:
                - Add car to database
                - If successful, send Telegram notification
                - If notification fails, rollback database addition
        4. Handle various error scenarios with appropriate logging and recovery

        Error Handling:
        - Validates all required fields before processing
        - Handles auction photo retrieval errors separately
        - Uses transactions to ensure database consistency
        - Implements rollback mechanism for failed operations
        - Provides detailed logging for all error scenarios

        Transaction Flow:
        1. Database Addition -> Success -> Send Notification
        2. If notification fails -> Rollback database addition
        3. If any step fails -> Log error and continue with next car

        Raises:
            asyncio.CancelledError: If the process is cancelled during execution
            Exception: If any error occurs during the car processing workflow.
                      All exceptions are caught, logged, and handled appropriately
                      to ensure service continuity.

        Notes:
            - The method is non-blocking and can be cancelled safely
            - All errors are logged for debugging purposes
            - Failed operations are rolled back to maintain data consistency
            - Method continues processing remaining cars even if one fails
        """
        try:
            # Получаем текущие активные автомобили из базы данных
            active_cars = self.database.get_active_cars()
            active_car_ids = {car['car_id'] for car in active_cars}

            for car in cars:
                # Проверяем, не была ли отменена задача
                if not self.is_running:
                    logger.info("New car processing cancelled due to service stop")
                    return

                try:
                    # Проверка обязательных полей
                    if not all(car.get(field) for field in CarValidationConstants.REQUIRED_FIELDS):
                        logger.warning(f"Invalid car data: {car}")
                        continue

                    # Проверяем, является ли автомобиль новым
                    if car['car_id'] not in active_car_ids:
                        logger.info(f"New car found: {car['title']} for user {user_id}")

                        # Обработка фотографий с аукциона в отдельном блоке try-except
                        try:
                            if car.get('auction_url'):
                                async with AuctionPhotoService() as auction_service:
                                    lot_number = auction_service.extract_lot_number(car['auction_url'])
                                    if lot_number:
                                        auction_photos = await auction_service.get_auction_photos(lot_number)
                                        car['auction_photos'] = auction_photos[
                                                                :CarValidationConstants.MAX_AUCTION_PHOTOS]
                                        logger.info(f"Received {len(car['auction_photos'])} photos for {car['title']}")
                        except Exception as auction_error:
                            logger.error(f"Error retrieving auction photos: {auction_error}")
                            car['auction_photos'] = []

                        # Начинаем транзакцию
                        try:
                            # Сначала пытаемся добавить автомобиль в базу данных
                            if not self.database.add_car(car):
                                logger.error(f"Failed to add car to database: {car['title']}")
                                continue

                            # После успешного добавления в базу отправляем уведомление
                            if not await self.telegram_service.send_new_car(car):
                                # Если отправка не удалась, откатываем добавление в базу
                                self.database.remove_car(car['car_id'])
                                logger.error(
                                    f"Failed to send notification, car removed from database: {car['title']}")
                                continue

                            logger.info(f"Car successfully added and notification sent: {car['title']}")

                        except Exception as transaction_error:
                            # В случае любой ошибки в транзакции
                            logger.error(f"Error in transaction processing: {transaction_error}")
                            # Попытка отката изменений
                            try:
                                self.database.remove_car(car['car_id'])
                            except Exception as rollback_error:
                                logger.error(f"Error during transaction rollback: {rollback_error}")
                            continue

                except Exception as car_error:
                    logger.error(f"Error processing car: {car_error}")
                    continue

        except asyncio.CancelledError:
            logger.info("Car processing cancelled")
            raise

        except Exception as e:
            logger.error(f"Critical error in process_new_cars: {e}")

    async def process_price_changes(self, cars: List[Dict[str, Union[int, str, Decimal]]], user_id: int) -> None:
        """
        Process and notify price changes for cars associated with a specific user.

        This asynchronous method monitors price changes in car listings by comparing current prices
        with previously stored values in the database. When significant price changes are detected,
        it updates the database and sends notifications to the user.

        Args:
            cars (List[Dict[str, Union[int, str, Decimal]]]): A list of dictionaries containing current car data.
                Each dictionary must contain:
                    - car_id (int): Unique identifier for the car
                    - price (Decimal): Current price of the car
                    - title (str): Title/name of the car listing
            user_id (int): The unique identifier of the user to process cars for

        Returns:
            None

        Raises:
            DatabaseError: If database operations fail
            TelegramError: If notification sending fails

        Implementation Details:
            1. Retrieves all active cars from database
            2. Creates a price mapping for efficient lookups
            3. Gets user-specific settings for filtering
            4. For each car:
                - Checks if car exists in active cars
                - Compares old and new prices
                - If price change exceeds threshold:
                    * Updates price in database
                    * Sends notification to user
        """
        # Получаем список всех активных автомобилей из базы данных
        active_cars = self.database.get_active_cars()

        # Создаем словарь текущих цен для быстрого доступа
        car_prices = {car['car_id']: car['price'] for car in active_cars}

        # Получаем пользовательские настройки (понадобится для будущей фильтрации)
        user_settings = self.database.get_user_settings(user_id)

        # Итерируемся по каждому автомобилю в текущем списке
        for car in cars:
            # Проверяем, существует ли автомобиль в базе активных машин
            if car['car_id'] in car_prices:
                # Извлекаем старую и новую цены
                old_price = car_prices[car['car_id']]
                new_price = car['price']

                # Проверяем, является ли изменение цены существенным
                if abs(old_price - new_price) > CarServiceConstants.PRICE_CHANGE_THRESHOLD:
                    # Обновляем цену в базе данных
                    if self.database.update_car_price(car['car_id'], new_price):
                        # Отправляем уведомление об изменении цены через Telegram
                        await self.telegram_service.send_price_change(car, old_price, new_price)
                        logger.info(
                            f"Price change detected and notified for car: {car['title']} for user {user_id}")

    async def process_sold_cars(self, current_car_ids: Set[int], user_id: int) -> None:
        """
        Process and identify sold cars for a specific user based on their current model preference.

        This asynchronous method identifies cars that are no longer listed on the marketplace
        and marks them as sold after verification. It specifically handles cars matching the
        user's selected model preference.

        Args:
            current_car_ids (Set[int]): Set of car IDs currently available on the marketplace.
                These IDs are used to identify which cars are no longer listed.
            user_id (int): The unique identifier of the user to process sold cars for.

        Returns:
            None

        Raises:
            DatabaseError: If database operations fail
            AutoRiaParserError: If car listing verification fails
            TelegramError: If notification sending fails

        Implementation Details:
            1. Retrieves user settings to determine current model preference
            2. Gets active cars filtered by the user's preferred model
            3. For each active car not in current_car_ids:
                - Verifies car's removal from website
                - If confirmed removed:
                    * Marks car as sold in database
                    * Sends notification to user

        Dependencies:
            - AutoRiaParser: For verifying car listing status
            - Database: For car status management
            - TelegramService: For user notifications

        Notes:
            - Only marks cars as sold after confirming their removal from the marketplace
            - Filters cars based on user's model preference to prevent false positives
            - Includes error handling for network and database operations
        """
        # Получаем настройки пользователя для определения текущей предпочтительной модели
        user_settings = self.database.get_user_settings(user_id)
        current_model = user_settings.get('model', AutoRiaDefaults.DEFAULT_MODEL).upper()

        logger.info(f"User {user_id} model preference: {current_model}")

        # Получаем только активные машины текущей модели
        active_cars = self.database.get_active_cars(model=current_model)

        logger.info(f"Retrieved {len(active_cars)} active cars for user {user_id} with model {current_model}")

        for car in active_cars:
            # Если автомобиль больше не присутствует в текущем списке ID автомобилей
            if car['car_id'] not in current_car_ids:
                # Проверяем, действительно ли объявление удалено с сайта
                async with AutoRiaParser() as parser:
                    try:
                        url = AutoRiaURLs.get_car_url(car['car_id'])
                        async with parser.session.get(url) as response:
                            if response.status == HTTPConstants.STATUS_NOT_FOUND:
                                # Только если объявление действительно не найдено, помечаем как проданное
                                if self.database.mark_car_as_sold(car['car_id']):
                                    # Отправляем уведомление пользователю о проданном автомобиле
                                    await self.telegram_service.send_car_sold(car)
                                    logger.info(f"Car marked as sold and notified: {car['title']} for user {user_id}")
                    except Exception as e:
                        logger.error(f"Error checking car status: {e}")

    async def check_updates(self) -> None:
        """
        Performs comprehensive updates checking across all users.

        Main responsibilities:
            1. Retrieve all registered users
            2. Parse car listings for each user
            3. Process new cars, price changes, and sold cars
            4. Handle potential errors during the update process

        Raises:
            aiohttp.ClientError: Network-related errors
            sqlite3.Error: Database-related errors
        """
        try:
            # Получаем список всех зарегистрированных пользователей
            users = self.database.get_all_users()

            # Создаем асинхронный контекст парсера AutoRia
            async with AutoRiaParser() as parser:
                # Обрабатываем каждого пользователя
                for user_id in users:
                    # Получаем настройки конкретного пользователя
                    user_settings = self.database.get_user_settings(user_id)

                    # Получаем список автомобилей для пользователя
                    cars = await parser.get_cars(user_settings)

                    # Пропускаем итерацию, если автомобили не найдены
                    if not cars:
                        logger.warning(f"No cars found for user {user_id}")
                        continue

                    # Создаем множество идентификаторов текущих автомобилей
                    current_car_ids = {car['car_id'] for car in cars}

                    # Последовательно обрабатываем новые, измененные и проданные автомобили
                    await self.process_new_cars(cars, user_id)
                    await self.process_price_changes(cars, user_id)
                    await self.process_sold_cars(current_car_ids, user_id)

        except aiohttp.ClientError as e:
            logger.error(f"Network error during update check: {e}")
        except sqlite3.Error as e:
            logger.error(f"Database error during update check: {e}")
        except Exception as e:
            logger.error(f"Error during update check: {e}")

    async def monitoring_loop(self) -> None:
        """
        Continuous monitoring loop that checks for updates periodically.
        Handles exceptions and implements error recovery mechanism.
        """
        while self.is_running:
            try:
                # Выполнение проверки обновлений
                await self.check_updates()
                # Ожидание установленного интервала между проверками
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                # Ожидание перед повторной попыткой в случае ошибки
                await asyncio.sleep(CarServiceConstants.ERROR_RETRY_DELAY)

    def start_monitoring(self) -> bool:
        """
        Start the car monitoring process.
        Returns:
            bool: True if monitoring started successfully, False if already running
        """
        # Проверка, не запущен ли уже мониторинг
        if self.is_running:
            logger.info(f"Monitoring already started. Task status: "
                        f"{self.monitoring_task.done() if self.monitoring_task else 'No task'}")
            return False

        logger.info("Starting car monitoring service")
        self.is_running = True
        self.monitoring_task = asyncio.create_task(self.monitoring_loop())
        logger.info(f"Created monitoring task: {self.monitoring_task.get_name()}")
        return True

    def stop_monitoring(self) -> bool:
        """
        Stop the car monitoring process.
        Returns:
            bool: True if monitoring was successfully stopped, False if already stopped
        """
        # Проверка, был ли мониторинг уже остановлен
        if not self.is_running:
            logger.info("Monitoring already stopped")
            return False

        logger.info("Stopping car monitoring service")
        self.is_running = False

        # Отмена задачи мониторинга, если она еще выполняется
        if self.monitoring_task and not self.monitoring_task.done():
            self.monitoring_task.cancel()
            logger.info("Monitoring task cancelled")

        return True

    async def shutdown(self) -> None:
        """
        Gracefully shut down the monitoring service.

        Ensures proper cancellation of the monitoring task with a timeout mechanism.
        """
        logger.info("Starting graceful shutdown...")

        # Останавливаем мониторинг
        self.stop_monitoring()

        # Проверяем наличие активной задачи мониторинга
        if self.monitoring_task:
            try:
                # Ожидаем завершения задачи с установленным таймаутом
                await asyncio.wait_for(self.monitoring_task, timeout=CarServiceConstants.SHUTDOWN_TIMEOUT)

            except asyncio.TimeoutError:
                logger.warning("Shutdown timeout exceeded, forcing task cancellation")
            except asyncio.CancelledError:
                logger.info("Monitoring task was cancelled during shutdown")
            finally:
                # В любом случае отменяем задачу если она еще активна
                if not self.monitoring_task.done():
                    self.monitoring_task.cancel()
                    try:
                        await self.monitoring_task
                    except asyncio.CancelledError:
                        pass

            logger.info("Shutdown completed")

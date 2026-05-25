# auto_ria_tracker/database/database.py

import sqlite3
from typing import Optional, List, Dict, Any
import json

from config_data.config import config
from config_data.constants import AutoRiaDefaults
from logger_config import logger


class Database:
    """
    A database management class for handling car auction data.

    Attributes:
        db_path (str): Path to the SQLite database file.

    Methods:
        create_tables(): Initialize database tables
        add_car(car_data): Add a new car to the database
        update_car_price(car_id, new_price): Update car price and track price history
        mark_car_as_sold(car_id): Mark a car as sold
        get_active_cars(): Retrieve list of active cars
        get_user_settings(user_id): Get or create user settings
        update_user_settings(): Update user preferences
        get_all_users(): Get list of all users
        remove_car(car_id): Remove a car record from the database
    """
    def __init__(self) -> None:
        """
        Initialize the database connection and create tables.

        Args:
            None

        Side Effects:
            - Sets db_path from configuration
            - Calls create_tables() to ensure database structure
        """
        # Получаем путь к базе данных из конфигурации
        self.db_path = config.db.db_path

        # Создаем необходимые таблицы при инициализации
        self.create_tables()

    def create_tables(self) -> None:
        """
        Create necessary database tables if they do not exist.

        Tables created:
        - cars: Stores car information, including model details.
        - price_history: Tracks price changes for cars.
        - user_settings: Stores user preferences, including the default model.

        Raises:
            sqlite3.Error: If database table creation or modification fails
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Создаем основную таблицу для хранения информации об автомобилях
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cars (
                        car_id INTEGER PRIMARY KEY,
                        url TEXT UNIQUE,
                        title TEXT,
                        price REAL,
                        auction_url TEXT,
                        photos TEXT,
                        auction_photos TEXT DEFAULT '[]',  
                        status TEXT DEFAULT 'active',
                        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        model TEXT
                    )
                ''')

                # Проверяем структуру таблицы
                cursor.execute("PRAGMA table_info(cars)")
                columns = [column[1] for column in cursor.fetchall()]

                # Если колонки model нет, добавляем её
                if 'model' not in columns:
                    cursor.execute('ALTER TABLE cars ADD COLUMN model TEXT')

                # Добавляем колонку auction_photos, если её нет
                if 'auction_photos' not in columns:
                    cursor.execute('''
                        ALTER TABLE cars 
                        ADD COLUMN auction_photos TEXT DEFAULT '[]'
                    ''')

                # Создаем таблицу для истории изменения цен
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS price_history (
                        id INTEGER PRIMARY KEY,
                        car_id INTEGER,
                        old_price REAL,
                        new_price REAL,
                        change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (car_id) REFERENCES cars (car_id)
                    )
                ''')

                # Создаем таблицу для хранения настроек пользователей
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_settings (
                        user_id INTEGER PRIMARY KEY,
                        model TEXT DEFAULT 'Sequoia',
                        import_usa BOOLEAN DEFAULT 1,
                        accident BOOLEAN DEFAULT 1
                    )
                ''')

                conn.commit()
                logger.info("Database successfully initialized")

        except sqlite3.Error as e:
            logger.error(f"Error creating database tables: {e}")

    def add_car(self, car_data: Dict[str, Any]) -> Optional[int]:
        """
        Add a new car to the database.

        Args:
            car_data (Dict[str, Any]): Dictionary containing car details
                - car_id (int): Unique car identifier
                - url (str): Car listing URL
                - title (str): Car title
                - price (float): Car price
                - auction_url (Optional[str]): Auction URL (optional)
                - photos (Optional[List[str]]): Car photos (optional)
                - auction_photos (Optional[List[str]]): Auction photos (optional)
                - model (str): Model of the car (optional, defaults to a predefined model if not provided)

        Returns:
            Optional[int]: Last row ID if car added successfully, None otherwise

        Raises:
            sqlite3.IntegrityError: If car already exists (e.g., duplicate car_id)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Преобразуем списки фотографий в JSON
                photos_json = json.dumps(car_data.get('photos', []))
                auction_photos_json = json.dumps(car_data.get('auction_photos', []))

                # Выполняем вставку новой записи об автомобиле
                cursor.execute('''
                    INSERT INTO cars (car_id, url, title, price, auction_url, photos, auction_photos, model)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    car_data['car_id'],
                    car_data['url'],
                    car_data['title'],
                    car_data['price'],
                    car_data.get('auction_url'),
                    photos_json,
                    auction_photos_json,
                    car_data.get('model', AutoRiaDefaults.DEFAULT_MODEL)
                ))

                conn.commit()
                logger.info(f"Car successfully added to database: {car_data['title']}")
                return cursor.lastrowid

        except sqlite3.IntegrityError:
            logger.warning(f"Car already exists in database: {car_data['title']}")
            return None
        except Exception as e:
            logger.error(f"Error adding car to database: {e}")
            return None

    def update_car_price(self, car_id: int, new_price: float) -> bool:
        """
        Update car price and log price history.

        Args:
            car_id (int): Unique car identifier
            new_price (float): Updated car price

        Returns:
            bool: True if price updated successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Получаем текущую цену автомобиля
                cursor.execute('SELECT price FROM cars WHERE car_id = ?', (car_id,))
                result = cursor.fetchone()

                if result:
                    # Сохраняем старую цену в историю изменений  ъ
                    old_price = result[0]

                    cursor.execute('''
                        INSERT INTO price_history (car_id, old_price, new_price)
                        VALUES (?, ?, ?)
                    ''', (car_id, old_price, new_price))

                    # Обновляем текущую цену автомобиля в базе
                    cursor.execute('''
                        UPDATE cars 
                        SET price = ?, last_updated = CURRENT_TIMESTAMP
                        WHERE car_id = ?
                    ''', (new_price, car_id))

                    logger.info(f"Price updated for car ID {car_id}: {old_price} -> {new_price}")
                    return True
                return False
        except sqlite3.Error as e:
            logger.error(f"Error updating car price for ID {car_id}: {e}")
            return False

    def mark_car_as_sold(self, car_id: int) -> bool:
        """
        Mark a car as sold in the database.

        Args:
            car_id (int): Unique car identifier

        Returns:
            bool: True if car status updated successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Обновляем статус и метку времени
                cursor.execute('''
                    UPDATE cars 
                    SET status = 'sold', last_updated = CURRENT_TIMESTAMP
                    WHERE car_id = ?
                ''', (car_id,))

                # Возвращаем результат - был ли найден и обновлен автомобиль
                if cursor.rowcount > 0:
                    logger.info(f"Car marked as sold: ID {car_id}")
                    return True
                logger.warning(f"No car found with ID {car_id} to mark as sold")
                return False

        except sqlite3.Error as e:
            logger.error(f"Error marking car as sold (ID {car_id}): {e}")
            return False

    def get_active_cars(self, model: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve a list of active cars, optionally filtered by model.

        Args:
           model (Optional[str]): The model of the cars to filter by. If not provided, all active cars are retrieved.

        Returns:
           List[Dict[str, Any]]: List of active car dictionaries. Each dictionary contains car details such as
           car_id, url, title, price, auction_url, photos, auction_photos, status, and model.

        Raises:
           sqlite3.Error: If there is an error querying the database.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Используем row_factory для получения результатов в виде словаря
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Если параметр model передан, выполняем запрос с фильтрацией по модели
                if model:
                    cursor.execute('''
                                   SELECT * FROM cars 
                                   WHERE status = 'active' AND model = ?
                                   ORDER BY first_seen DESC
                               ''', (model,))
                # Если параметр model не передан, выполняем запрос только по статусу 'active'
                else:
                    cursor.execute('''
                                   SELECT * FROM cars 
                                   WHERE status = 'active'
                                   ORDER BY first_seen DESC
                               ''')

                # Преобразуем результаты в список словарей
                active_cars = [dict(row) for row in cursor.fetchall()]
                logger.info(f"Retrieved {len(active_cars)} active cars")
                return active_cars

        except sqlite3.Error as e:
            logger.error(f"Error retrieving active cars: {e}")
            return []

    def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve or create user settings.

        Args:
            user_id (int): Unique user identifier

        Returns:
            Dict[str, Any]: User settings with default values if not exists
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Пытаемся получить существующие настройки
                cursor.execute('''
                    SELECT model, import_usa, accident 
                    FROM user_settings WHERE user_id = ?
                ''', (user_id,))
                result = cursor.fetchone()

                # Если настройки существуют, возвращаем их
                if result:
                    logger.info(f"Retrieved settings for user ID {user_id}")
                    return {"model": result[0], "import_usa": bool(result[1]), "accident": bool(result[2])}

                # Если настроек нет, создаем новую запись со значениями по умолчанию
                cursor.execute('''
                    INSERT INTO user_settings (user_id) VALUES (?)
                ''', (user_id,))
                conn.commit()

                logger.info(f"Created default settings for user ID {user_id}")
                # Возвращаем дефолтные настройки
                return {"model": "Sequoia", "import_usa": True, "accident": True}

        except sqlite3.Error as e:
            logger.error(f"Error retrieving user settings for ID {user_id}: {e}")
            # Возвращаем дефолтные настройки в случае ошибки
            return {"model": "Sequoia", "import_usa": True, "accident": True}

    def update_user_settings(self, user_id: int, model: Optional[str] = None, import_usa: Optional[bool] = None, accident: Optional[bool] = None) -> bool:
        """
        Updates user preferences in the database.

        This method allows partial updates of user settings. Only the provided
        parameters will be modified, while others remain unchanged.

        Args:
            user_id (int): Unique identifier of the user.
            model (Optional[str]): Preferred car model. If None, the existing value remains unchanged.
            import_usa (Optional[bool]): Preference for importing from the USA (stored as 0/1).
                                         If None, the existing value remains unchanged.
            accident (Optional[bool]): Preference for accident history (stored as 0/1).
                                       If None, the existing value remains unchanged.

        Returns:
            bool: True if the update was successful, False if the user was not found.

        Raises:
            sqlite3.Error: If a database error occurs.
            ValueError: If `user_id` is not a positive integer.
        """
        # Проверяем, что user_id положительный, иначе выбрасываем исключение
        if user_id < 1:
            raise ValueError("user_id must be a positive integer")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Очищаем строку модели от лишних пробелов, если она передана
                model = model.strip() if model is not None else None

                # Преобразуем булевое значения в 0 или 1 для хранения в БД
                import_usa = int(import_usa) if import_usa is not None else None
                accident = int(accident) if accident is not None else None

                # Выполняем SQL-запрос на обновление данных
                cursor.execute('''
                    UPDATE user_settings SET 
                        model = COALESCE(?, model),
                        import_usa = COALESCE(?, import_usa),
                        accident = COALESCE(?, accident)
                    WHERE user_id = ?
                ''', (model, import_usa, accident, user_id))

                conn.commit()

                # Проверяем, была ли изменена хотя бы одна строка
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Successfully updated settings for user_id={user_id}")
                else:
                    logger.warning(f"No settings were updated. User with user_id={user_id} not found.")

                return success

        except sqlite3.Error as e:
            logger.error(f"Database error while updating settings for user_id={user_id}: {e}")
            raise

    def get_all_users(self) -> List[int]:
        """
        Retrieve a list of all user IDs from the user_settings table.

        Returns:
            List[int]: A list of all unique user identifiers in the database
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Извлекаем все идентификаторы пользователей
                cursor.execute('SELECT user_id FROM user_settings')
                users = [row[0] for row in cursor.fetchall()]

                logger.info(f"Retrieved {len(users)} users from database")
                return users

        except sqlite3.Error as e:
            logger.error(f"Error retrieving users from database: {e}")
            return []

    def remove_car(self, car_id: int) -> bool:
        """
        Removes a car record from the database.

        Args:
            car_id (int): The unique identifier of the car to remove.

        Returns:
            bool: True if the car was successfully removed, False otherwise.

        Note:
            This method is primarily used for transaction rollback when notification fails.
            It completely removes the car record rather than just marking it as inactive.

        Raises:
            sqlite3.Error: Database-related errors are caught and logged.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Удаляем связанные записи из price_history
                cursor.execute('DELETE FROM price_history WHERE car_id = ?', (car_id,))

                # Удаляем запись автомобиля
                cursor.execute('DELETE FROM cars WHERE car_id = ?', (car_id,))

                conn.commit()

                # Проверяем успешность удаления
                if cursor.rowcount > 0:
                    logger.info(f"Successfully deleted car with ID: {car_id}")
                    return True
                else:
                    logger.warning(f"Car with ID {car_id} not found for deletion")
                    return False

        except sqlite3.Error as e:
            logger.error(f"Error deleting car {car_id}: {e}")
            return False

# Создаем единственный экземпляр базы данных
db = Database()

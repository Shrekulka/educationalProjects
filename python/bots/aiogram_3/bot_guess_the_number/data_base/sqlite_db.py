# bot_guess_the_number/data_base/sqlite_db.py

import traceback

import aiosqlite as sq

from logger import logger
from models.user_game_data import UserGameData


async def sql_start() -> None:
    """
        Initializes the SQLite database and creates the 'user_game_data' table if it doesn't exist.

        Returns:
            None
    """
    try:
        # Установка асинхронного соединения с базой данных
        async with sq.connect("game_bd.db") as base:
            # Получение курсора для выполнения SQL-запросов
            cur = await base.cursor()

            # Проверка успешного подключения к базе данных
            if base:
                logger.info("Database connected successfully!")

            # Создание таблицы 'user_game_data', если она не существует
            await cur.execute(
                """CREATE TABLE IF NOT EXISTS user_game_data (user_id INTEGER PRIMARY KEY, is_playing INTEGER, 
                   target_number INTEGER, remaining_attempts INTEGER, total_games INTEGER, games_won INTEGER)""")
            # Фиксация изменений в базе данных
            await base.commit()

        # Обработка исключения, если произошла ошибка при инициализации базы данных
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in sql_start: {e}\n{detailed_send_message_error}")


async def get_user_game_data(user_id: int) -> UserGameData:
    """
        Retrieves user game data based on the user ID from the 'user_game_data' table.

        Args:
            user_id: User ID.

        Returns:
            UserGameData: User game data.
    """
    try:
        # Установка асинхронного соединения с базой данных
        async with sq.connect("game_bd.db") as base:
            # Получение курсора для выполнения SQL-запросов
            cur = await base.cursor()

            # Выполнение SQL-запроса для выборки данных игры пользователя по ID
            await cur.execute('SELECT * FROM user_game_data WHERE user_id=?', [user_id])

            # Получение результата SQL-запроса
            result = await cur.fetchone()

            # Если данные найдены, возвращаем их
            if result:
                return UserGameData(*result)
            # Если данных не найдено, создаем по умолчанию
            else:
                default_data = UserGameData(user_id)
                await update_user_game_data(default_data)
                return default_data

        # Обработка исключения, если произошла ошибка при получении данных игры
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in get_user_game_data: {e}\n{detailed_send_message_error}")


async def update_user_game_data(user_data: UserGameData) -> None:
    """
        Updates user game data in the 'user_game_data' table.

        Args:
            user_data: UserGameData object containing updated data.

        Returns:
            None
    """
    try:
        # Проверяем, существуют ли уже данные пользователя в базе данных
        user_in_db = await get_user_game_data(user_data.user_id)
        # Если данных о пользователе нет, создаем запись с данными по умолчанию
        if user_in_db is None:
            await create_default_user_data(user_data.user_id)

        # Установка асинхронного соединения с базой данных
        async with sq.connect("game_bd.db") as base:
            # Получение курсора для выполнения SQL-запросов
            cur = await base.cursor()

            # Выполнение SQL-запроса для обновления данных игры пользователя
            await cur.execute('INSERT OR REPLACE INTO user_game_data VALUES (?, ?, ?, ?, ?, ?)',
                              (user_data.user_id, int(user_data.is_playing), user_data.target_number,
                               user_data.remaining_attempts, user_data.total_games, user_data.games_won))

            # Фиксация изменений в базе данных
            await base.commit()

        # Обработка исключения, если произошла ошибка при обновлении данных игры
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in update_user_game_data: {e}\n{detailed_send_message_error}")


async def create_default_user_data(user_id: int) -> None:
    """
    Creates default user data in the 'user_game_data' table for a new user.

    Args:
        user_id: User ID.

    Returns:
        None
    """
    # Создаем объект с данными по умолчанию для нового пользователя
    default_data = UserGameData(user_id)
    # Обновляем запись в базе данных с данными по умолчанию для нового пользователя
    await update_user_game_data(default_data)

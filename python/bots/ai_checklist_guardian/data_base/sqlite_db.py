# ai_checklist_guardian/data_base/sqlite_db.py

import traceback
from typing import List

import aiosqlite as sq

from create_bot import bot
from logger import logger
from models.user_data import UserData


async def sql_start() -> None:
    """
        Initializes the SQLite database and creates the 'reports' table if it doesn't exist.

        Returns:
            None
    """
    try:
        # Установка асинхронного соединения с базой данных
        async with sq.connect("ai_bd.db") as base:
            # Получение курсора для выполнения SQL-запросов
            cur = await base.cursor()

            # Проверка успешного подключения к базе данных
            if base:
                logger.info("Database connected successfully!")

            # Создание таблицы 'reports', если она не существует
            await cur.execute(
                'CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'location TEXT, option TEXT, comment TEXT, photo_link TEXT, report TEXT)'
            )

            # Фиксация изменений в базе данных
            await base.commit()

        # Обработка исключения, если произошла ошибка при инициализации базы данных
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in sql_start: {e}\n{detailed_send_message_error}")


async def sql_add_report(user_data: UserData) -> None:
    """
        Adds a user report to the 'reports' table in the SQLite database.

        Args:
            user_data (UserData): User data containing location, option, comment, photo_link, and report.

        Returns:
            None
    """
    try:
        # Установка асинхронного соединения с базой данных
        async with sq.connect("ai_bd.db") as base:
            # Получение курсора для выполнения SQL-запросов
            cur = await base.cursor()

            # Выполнение SQL-запроса для добавления отчета пользователя в таблицу 'reports'
            await cur.execute('INSERT INTO reports (location, option, comment, photo_link, report) '
                              'VALUES (?, ?, ?, ?, ?)', (user_data.location, user_data.option,
                                                         user_data.comment, user_data.photo_link, user_data.report))

            # Фиксация изменений в базе данных
            await base.commit()

        # Обработка исключения, если произошла ошибка при добавлении отчета
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in sql_add_report: {e}\n{detailed_send_message_error}")


async def get_report(user_id) -> str:
    """
        Retrieves a user report based on the user ID from the 'reports' table.

        Args:
            user_id: User ID.

        Returns:
            str: User report text or an error message if the report is not found.
    """
    try:
        # Установка асинхронного соединения с базой данных
        async with sq.connect("ai_bd.db") as base:
            # Получение курсора для выполнения SQL-запросов
            cur = await base.cursor()

            # Выполнение SQL-запроса для выборки отчета пользователя по ID
            await cur.execute('SELECT report FROM reports WHERE id=?', [user_id])

            # Получение результата SQL-запроса
            result = await cur.fetchone()

            # Проверка наличия результата
            if result:
                return result[0]
            else:
                return "Report not found"

        # Обработка исключения, если произошла ошибка при получении отчета
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in get_report: {e}\n{detailed_send_message_error}")


async def sql_read(message, cur) -> None:
    """
        Reads and sends all records from the 'reports' table to the user.

        Args:
            message: User's message.
            cur: Database cursor.

        Returns:
            None
    """
    try:
        # Итерация по всем записям в таблице 'reports' и отправка их пользователю
        for ret in cur.execute('SELECT * FROM reports').fetchall():
            await bot.send_message(message.from_user.id,
                                   f'Location: {ret[1]}\nOption: {ret[2]}\nComment: {ret[3]}\nPhoto Link: {ret[4]}')

        # Обработка исключения, если произошла ошибка при чтении записей
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in sql_read: {e}\n{detailed_send_message_error}")


async def sql_read2(cur) -> List:
    """
        Reads all records from the 'reports' table.

        Args:
            cur: Database cursor.

        Returns:
            list: List of records.
    """
    try:
        # Выполнение SQL-запроса для выборки всех записей из таблицы 'reports'
        return await cur.execute('SELECT * FROM reports').fetchall()

        # Обработка исключения, если произошла ошибка при чтении записей
    except Exception as e:
        # Запись подробной информации об ошибке в лог
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in sql_read2: {e}\n{detailed_send_message_error}")


async def sql_delete_command(base, cur, data) -> None:
    """
        Deletes a record from the 'reports' table.

        Args:
            base: Database connection.
            cur: Database cursor.
            data: Record ID to delete.

        Returns:
            None
    """
    try:
        # Выполнение SQL-запроса для удаления записи из таблицы 'reports'
        cur.execute('DELETE FROM reports WHERE id == ?', (data,))

        # Фиксация изменений в базе данных
        await base.commit()

        # Обработка исключения, если произошла ошибка при удалении записи
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error in sql_delete_command: {e}\n{detailed_send_message_error}")

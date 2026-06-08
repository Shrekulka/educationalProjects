# first_steps_with_SQLite/main.py


import sqlite3 as sq
import traceback

from logger import logger
from utils import generate_data_for_bd, is_table_empty, execute_and_log_query


def main():
    try:
        # Устанавливает связь, с помощью контекста менеджера, с нашей BD (находится в каталоге, где и исполняемый файл),
        # если ее нет, то создастся. При такой установке связи не нужно закрывать соединение, оно закроется
        # автоматически
        with sq.connect("my_bd.db") as con:
            logger.info(f"Connection successfully established!\n")
            # Для взаимодействия с BD используем экземпляр класса Cursor
            cur = con.cursor()

            # Создаем таблицу, если ее нет (CREATE TABLE IF NOT EXISTS), с таким именем (users) и колонками (name,
            # gender, age, score)
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL, 
                        gender TEXT,
                        age INTEGER NOT NULL DEFAULT 18,
                        score INTEGER)""")

            # Проверка наличия данных в таблице
            if is_table_empty(cur, "users"):
                fields_and_types = {"user_id": "INTEGER",
                                    "name": "TEXT",
                                    "gender": "TEXT",
                                    "age": "INTEGER",
                                    "score": "INTEGER"}
                generate_data_for_bd(cur, fields_and_types, num_records=10, seed=42)
                execute_and_log_query(cur, "SELECT * FROM users")
            else:
                # Вставим здесь примеры работы с Командами SELECT и INSERT
                # Пример добавления записей в таблицу 'users'
                cur.execute("INSERT INTO users (name, gender, age, score) VALUES ('John Doe', 'Male', 30, 80)")
                cur.execute("INSERT INTO users (name, gender, age, score) VALUES ('Jane Smith', 'Female', 25, 95)")

                # Примеры запросов SELECT
                execute_and_log_query(cur, "SELECT user_id, name, gender, age FROM users")
                execute_and_log_query(cur, "SELECT * FROM users")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score < 50")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score BETWEEN 50 and 80")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score == 83")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score == 97 ORDER BY age ASC")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score == 97 ORDER BY name DESC")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score == 97 LIMIT 2 OFFSET 1")

                # Операторы сравнения
                execute_and_log_query(cur, "SELECT * FROM users WHERE score = 97")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score > 60")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score < 60")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score >= 60")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score <= 60")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score != 60")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score BETWEEN 50 AND 80")

                # Ключевые слова для комбинирования условий
                execute_and_log_query(cur, "SELECT * FROM users WHERE score > 50 AND age < 30")
                execute_and_log_query(cur, "SELECT * FROM users WHERE score > 50 OR age < 30")
                execute_and_log_query(cur, "SELECT * FROM users WHERE NOT score = 60")
                execute_and_log_query(cur, "SELECT * FROM users WHERE age IN (25, 30, 35)")
                execute_and_log_query(cur, "SELECT * FROM users WHERE age NOT IN (25, 30, 35)")

            # # Удаление таблицы, если она существует
            # drop_table_if_exists(cur, "users")

    except Exception as error:
        detailed_send_message_error_main = traceback.format_exc()
        logger.error(f"An unexpected error occurred: {error}\n{detailed_send_message_error_main}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An unexpected error occurred: {e}\n{detailed_send_message_error}")

# commands_when_work_with_tables/main.py


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
                ########################################################################################################
                # обнулим значения для всех игроков

                # 1) напрямую - cur.execute("UPDATE users SET score = 0")
                # 2) через функцию - execute_and_log_query(cur, "UPDATE users SET score = 0")
                execute_and_log_query(cur, "UPDATE users SET score = 0")

                # Выполним SELECT, чтобы убедиться, что данные были обнулены
                # 1) напрямую:
                # cur.execute("SELECT * FROM users")
                # result = cur.fetchall()
                # for row in result:
                #     print(row)
                # 2) через функцию - execute_and_log_query(cur, "SELECT * FROM users")
                execute_and_log_query(cur, "SELECT * FROM users")
                ########################################################################################################
                # для женского пола очки увеличим на 100
                execute_and_log_query(cur, "UPDATE users SET score = score + 100 WHERE gender = 'Female'")
                execute_and_log_query(cur, "SELECT * FROM users")
                ########################################################################################################
                # для David Guzman увеличим очки на 7
                execute_and_log_query(cur, "UPDATE users SET score = score + 7 WHERE name LIKE 'David Guzman'")
                execute_and_log_query(cur, "SELECT * FROM users")
                ########################################################################################################
                # добавим 15 очков любому, чье имя начинается с буквы 'A'
                execute_and_log_query(cur, "UPDATE users SET score = score + 15 WHERE name LIKE 'A%'")
                execute_and_log_query(cur, "SELECT * FROM users")
                ########################################################################################################
                # Удалим записи у тех у кого user_id равен 2 и 5
                execute_and_log_query(cur, "DELETE FROM users WHERE user_id IN (2, 5)")
                execute_and_log_query(cur, "SELECT * FROM users")
                ########################################################################################################

                ########################################################################################################
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

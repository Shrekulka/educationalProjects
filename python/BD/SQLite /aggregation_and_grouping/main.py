# aggregation_and_grouping/main.py


import sqlite3 as sq
import traceback

from colorama import Fore, Style

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
                # Выполняем запрос для выбора всех данных из таблицы "users"
                execute_and_log_query(cur, "SELECT * FROM users")
                ########################################################################################################
                # Выполняем подсчет количества пользователей с мужским полом в таблице "users"
                result = cur.execute("SELECT count(user_id) FROM users WHERE  gender = 'Male'")
                print(f"\n{Fore.GREEN}Found {result.fetchone()[0]} male in the table{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем подсчет уникальных значений возраста в таблице "users"
                result = cur.execute("SELECT count(DISTINCT age) FROM users")
                print(f"{Fore.GREEN}Found {result.fetchone()[0]} unique ages in the table{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем подсчет суммы баллов для пользователей с женским полом в таблице "users"
                result = cur.execute("SELECT sum(score) FROM users WHERE gender = 'Female'")
                print(f"{Fore.GREEN}Total score for females: {result.fetchone()[0]}{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем запрос для выбора минимального значения возраста из таблицы "users"
                result_min_age = cur.execute("SELECT min(age) FROM users")
                print(f"{Fore.GREEN}Minimum age in the table: {result_min_age.fetchone()[0]}{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем запрос для выбора максимального значения баллов из таблицы "users"
                result_max_score = cur.execute("SELECT max(score) FROM users")
                print(f"{Fore.GREEN}Maximum score in the table: {result_max_score.fetchone()[0]}{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем запрос для вычисления среднего значения возраста пользователей в таблице "users"
                result_avg_age = cur.execute("SELECT avg(age) FROM users")
                print(f"{Fore.GREEN}Average age in the table: {result_avg_age.fetchone()[0]:.2f}{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем запрос для выбора суммы баллов сгруппированных по полу в таблице "users"
                result_gender_score_sum = cur.execute("SELECT gender, sum(score) FROM users GROUP BY gender")
                # Используем цикл for для обработки каждой строки результата
                for row in result_gender_score_sum.fetchall():
                    gender, total_score = row
                    print(f"{Fore.GREEN}Total score for {gender}: {total_score}{Style.RESET_ALL}")
                ########################################################################################################
                # Выполняем запрос для выбора суммы баллов сгруппированных по полу в таблице "users", а затем используем
                # вложенный запрос с дополнительным GROUP BY sum для группировки результатов по уникальной сумме баллов
                result_gender_score_sum = cur.execute("SELECT gender, sum FROM (SELECT gender, SUM(score) "
                                                      "AS sum FROM users GROUP BY gender) GROUP BY sum DESC")
                # Используем цикл for для обработки каждой строки результата
                for row in result_gender_score_sum.fetchall():
                    gender, total_score = row
                    print(f"{Fore.GREEN}Total score for {gender}: {total_score}{Style.RESET_ALL}")
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

# first_steps_with_SQLite/utils.py

import traceback

from colorama import Fore, Style
from faker import Faker
from tabulate import tabulate

from logger import logger

fake = Faker()


def fake_value(field_type):
    # Извлекаем имя поля и его тип из переданной пары
    field, field_type = field_type

    # Генерация значения в зависимости от типа поля
    if field == "name":
        # Если поле - "name", генерируем случайное имя
        return fake.name()
    elif field == "gender":
        # Если поле - "gender", выбираем случайный элемент из ('Male', 'Female')
        return fake.random_element(elements=('Male', 'Female'))
    elif field == "age":
        # Если поле - "age", генерируем случайный возраст в диапазоне от 18 до 65 лет
        return fake.random_int(min=18, max=65)
    elif field == "score":
        # Если поле - "score", генерируем случайный балл в диапазоне от 0 до 100
        return fake.random_int(min=0, max=100)
    elif field == "user_id":
        pass
    else:
        # Если тип поля неизвестен, можно добавить обработку для других типов полей, если это необходимо
        # В данном случае, возвращаем None, но можно внести изменения в соответствии с требованиями
        return None


# Функция для генерации данных в базу данных

def generate_data_for_bd(cur, fields_and_types, num_records=10, seed=42):
    try:
        # Установка seed для повторяемости данных
        Faker.seed(seed)

        # Генерация и вставка данных в таблицу
        for _ in range(num_records):
            values = [fake_value(field_type) for field_type in fields_and_types.items()]
            fields = list(fields_and_types.keys())
            placeholders = ', '.join(['?' for _ in range(len(fields))])

            # Генерация строки запроса для вставки данных в таблицу 'users'
            query = f"INSERT INTO users ({', '.join(fields)}) VALUES ({placeholders})"

            # Выполнение SQL-запроса с использованием сформированного запроса и значений
            cur.execute(query, values)

            # Вывод отладочной информации
            logger.debug(f"{num_records} records inserted into the 'users' table.")
        else:
            logger.info("Skipping data generation as the 'users' table is not empty.")

    except Exception as e:
        # Обработка и вывод ошибки в случае неудачи
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error generating data for BD: {e}\n{detailed_send_message_error}")


# Функция для проверки, пуста ли таблица
def is_table_empty(cursor, table_name):
    try:
        # Проверяем существование таблицы
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone() is not None

        if table_exists:
            # Если таблица существует, выполняем запрос на подсчет записей в таблице
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            # Получение результата запроса
            row_count = cursor.fetchone()[0]
            # Возвращение True, если таблица пуста, иначе False
            is_empty = row_count == 0
            # Логгирование информации о пустоте таблицы
            if is_empty:
                logger.info(f"The '{table_name}' table is empty.")
            else:
                logger.info(f"The '{table_name}' table contains {row_count} records.")
            return is_empty
        else:
            # Если таблицы не существует, логгируем информацию и возвращаем False (не пустая таблица)
            logger.info(f"The '{table_name}' table does not exist.")
            return False

    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error checking if the table is empty: {e}\n{detailed_send_message_error}")
        return False


# Удаление таблицы, если она существует
def drop_table_if_exists(cur, table_name):
    try:
        # Выполнение SQL-запроса на удаление таблицы, если она существует
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        # Логирование успешного удаления таблицы
        logger.info(f"Table '{table_name}' successfully dropped.")
    except Exception as e:
        # Обработка ошибки и логирование деталей ошибки
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error dropping table: {e}\n{detailed_send_message_error}")


def execute_and_log_query(cur, query):
    try:
        # Выполнение SQL-запроса
        cur.execute(query)
        # Получение результатов запроса
        result = cur.fetchall()

        if result:
            # Форматирование заголовков таблицы с цветами
            headers = [Fore.GREEN + f"{description[0]}{Style.RESET_ALL}" for description in cur.description]
            # Форматирование данных таблицы с цветами
            formatted_result = [[Fore.YELLOW + str(cell) + Style.RESET_ALL for cell in row] for row in result]

            # Добавление цвета CYAN к символам '+' '|' '-'
            table = tabulate(formatted_result, headers=headers, tablefmt="pretty").replace('+',
                                                                                           f'{Fore.CYAN}+{Style.RESET_ALL}').replace(
                '|', f'{Fore.CYAN}|{Style.RESET_ALL}').replace('-', f'{Fore.CYAN}-{Style.RESET_ALL}')

            # Вывод результата запроса с цветами
            print(f"{Fore.MAGENTA}Result of the SELECT query:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{table}{Style.RESET_ALL}")
        else:
            # Вывод сообщения, если запрос не вернул результатов
            print("Query returned no results.")
    except Exception as e:
        # Обработка ошибки и логирование деталей ошибки
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error executing the query: {query}\n{e}\n{detailed_send_message_error}")

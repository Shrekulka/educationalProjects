# numeric_data_file_analyzer/main.py

import traceback

from logger_config import logger
from services.number_analyzer import (get_numbers_from_file, find_max_number, find_min_number,
                                      find_median, find_average, find_longest_sequence)


def main() -> None:
    """
        Main function to analyze numeric data from a file.

        This function performs the following tasks:
        1. Obtains numeric data from a file.
        2. Finds the maximum number in the file.
        3. Finds the minimum number in the file.
        4. Calculates the median of the numbers.
        5. Calculates the average arithmetic value of the numbers.
        6. Identifies the largest increasing and decreasing sequences of numbers.

        Parameters:
        None

        Returns:
        None
    """
    # Отримуємо числа з файлу
    numbers = get_numbers_from_file()
    ####################################################################################################################
    # 1. Максимальне число в файлі:
    max_number = find_max_number(numbers)
    print(f"Maximum number in the file: {max_number}")
    ####################################################################################################################
    # 2. Мінімальне число в файлі:
    min_number = find_min_number(numbers)
    print(f"Minimum number in the file: {min_number}")
    ####################################################################################################################
    # 3. Медіана:
    median = find_median(numbers)
    print(f"Median in the file: {median}")
    ####################################################################################################################
    # 4. Cереднє арифметичне значення:
    average = find_average(numbers)
    print(f"Average arithmetic value in the file: {average}")
    ####################################################################################################################
    # 5-6*. Найбільшу послідовність чисел (які ідуть один за одним), яка збільшується та зменьшується
    increasing_seq, decreasing_seq = find_longest_sequence(numbers)
    print(f"Largest increasing sequence in the file: {increasing_seq}")
    print(f"Largest decreasing sequence in the file: {decreasing_seq}")
    ####################################################################################################################


if __name__ == '__main__':
    try:
        main()
        # Обробка переривання користувачем
    except KeyboardInterrupt:
        logger.warning("Application terminated by the user")
    # Обробка неочікуваних помилок
    except Exception as error:
        # Отримання детальної інформації про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Unexpected error in the application: {error}\n{detailed_send_message_error}")

# numeric_data_file_analyzer/services/number_analyzer.py

import bz2
import os
import timeit
import traceback
from typing import List, Union, Tuple

import numpy as np
import requests

from config_data.config import FILE_URL, DOWNLOAD_URL_TEMPLATE, TEMP_ARCHIVE_FILE, TEMP_UNPACKED_FILE
from logger_config import logger


def get_numbers_from_file() -> List[int]:
    """
        Extracts numbers from a file.

        This function downloads a file from a predefined URL, extracts numbers from it, and returns them as a list.

        The function performs the following steps:
            1. Extracts the file ID from the predefined URL.
            2. Constructs the download URL using the file ID.
            3. Downloads the file from the constructed URL.
            4. Decodes the content of the downloaded file using the BZ2 compression algorithm.
            5. Saves the downloaded file in the current directory as a temporary archive.
            6. Extracts the archive to obtain the file containing numbers.
            7. Parses the numbers from the extracted file and stores them in a list.
            8. Removes the temporary archive and the extracted file.
            9. Logs the execution time of the function.

        Returns:
        List[int]: A list of numbers extracted from the file.

        Raises:
        Exception: If an error occurs during any step of the process, an error message is logged, and an empty list is
        returned.
    """
    try:
        # Запускаємо таймер для вимірювання початкового часу виконання
        start_time = timeit.default_timer()

        # Видобуваємо ідентифікатор файлу з URL
        file_id = FILE_URL.split('/')[-2]
        logger.info(f"file_id: {file_id}")

        # Формуємо URL для завантаження
        download_url = DOWNLOAD_URL_TEMPLATE + file_id
        logger.info(f"download_url: {download_url}")

        # Завантажуємо файл по прямому посиланню
        response = requests.get(download_url)

        # Перевіряємо наявність помилок під час завантаження
        response.raise_for_status()

        # Декодуємо вміст відповіді з використанням BZ2
        decoded_content = bz2.decompress(response.content).decode('utf-8')
        logger.info(f"response: \n{decoded_content[:100]}")

        # Зберігаємо файл у поточній директорії
        with open(TEMP_ARCHIVE_FILE, 'wb') as file:
            file.write(response.content)

        # Розпаковуємо архів
        unpacked_file = TEMP_UNPACKED_FILE
        with bz2.BZ2File(TEMP_ARCHIVE_FILE) as archive, open(unpacked_file, 'wb') as file:
            file.write(archive.read())

        # Видобуваємо числа із розпакованого файлу
        with open(unpacked_file) as file:
            file_numbers = [int(line.strip()) for line in file]
        logger.info(f"numbers: {file_numbers[:100]}")

        # Видаляємо тимчасовий архів та розпакований файл
        os.remove(TEMP_ARCHIVE_FILE)
        os.remove(unpacked_file)

        # Зупиняємо таймер та обчислюємо час виконання
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info(f"Time taken for get_numbers_from_file: {round(execution_time, 5)} seconds")

        # Повертаємо список чисел, які були витягнуті з файлу
        return file_numbers

    # Обробка виняткових ситуацій.
    except Exception as e:
        # Отримуємо детальну інформацію про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An error occurred: {e}\n{detailed_send_message_error}")
        return []


def find_max_number(num_list_for_max: List[int]) -> Union[int, None]:
    """
        Finds the maximum number in a list of numbers.

        Parameters:
        num_list_for_max (List[int]): The list of numbers to search.

        Returns:
        Union[int, None]: The maximum number found in the list, or None if the list is empty.
    """
    try:
        # Початок вимірювання часу виконання функції.
        start_time = timeit.default_timer()

        # Знаходження максимального числа в заданому списку.
        max_number = np.max(num_list_for_max)

        # Зупиняємо таймер та обчислюємо час виконання
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info(f"Time taken for find_max_number: {round(execution_time, 5)} seconds")

        # Повернення знайденого максимального числа.
        return max_number

    # Обробка виняткових ситуацій.
    except Exception as e:
        # Отримуємо детальну інформацію про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An error occurred while finding max number: {e}\n{detailed_send_message_error}")
        # Повернення значення None у випадку помилки.
        return None


def find_min_number(num_list_for_min: List[int]) -> Union[int, None]:
    """
        Finds the minimum number in a list of numbers.

        Parameters:
        num_list_for_min (List[int]): The list of numbers to search.

        Returns:
        Union[int, None]: The minimum number found in the list, or None if the list is empty.
    """
    try:
        # Початок вимірювання часу виконання функції.
        start_time = timeit.default_timer()

        # Знаходження мінімального числа в заданому списку.
        min_number = np.min(num_list_for_min)

        # Зупиняємо таймер та обчислюємо час виконання
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info(f"Time taken for find_min_number: {round(execution_time, 5)} seconds")

        # Повернення знайденого мінімального числа.
        return min_number

    # Обробка виняткових ситуацій.
    except Exception as e:
        # Отримуємо детальну інформацію про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An error occurred while finding min number: {e}\n{detailed_send_message_error}")
        # Повернення значення None у випадку помилки.
        return None


def find_median(num_list_for_median: List[int]) -> Union[float, None]:
    """
        Calculates the median of a list of numbers.

        Parameters:
        num_list_for_median (List[int]): The list of numbers.

        Returns:
        Union[float, None]: The median of the numbers in the list, or None if the list is empty.
    """
    try:
        # Початок вимірювання часу виконання функції.
        start_time = timeit.default_timer()

        # Знаходження медіани у заданому списку чисел.
        median = np.median(num_list_for_median)

        # Зупиняємо таймер та обчислюємо час виконання
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info(f"Time taken for find_median: {round(execution_time, 5)} seconds")

        # Повернення знайденої медіани.
        return median

    # Обробка виняткових ситуацій.
    except Exception as e:
        # Отримуємо детальну інформацію про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An error occurred while finding median: {e}\n{detailed_send_message_error}")
        # Повернення значення None у випадку помилки.
        return None


def find_average(num_list_for_average: List[int]) -> Union[float, None]:
    """
        Calculates the average arithmetic value of a list of numbers.

        Parameters:
        num_list_for_average (List[int]): The list of numbers.

        Returns:
        Union[float, None]: The average arithmetic value of the numbers in the list, or None if the list is empty.
    """
    try:
        # Початок вимірювання часу виконання функції.
        start_time = timeit.default_timer()

        # Обчислення середнього арифметичного значення у заданому списку чисел.
        average = np.mean(num_list_for_average)

        # Зупиняємо таймер та обчислюємо час виконання
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info(f"Time taken for find_average: {round(execution_time, 5)} seconds")

        # Повернення знайденого середнього арифметичного значення.
        return average

    # Обробка виняткових ситуацій.
    except Exception as e:
        # Отримуємо детальну інформацію про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An error occurred while finding average: {e}\n{detailed_send_message_error}")
        # Повернення значення None у випадку помилки.
        return None


def find_longest_sequence(sequence: List[int]) -> Tuple[List[int], List[int]]:
    """
        Finds the longest increasing and decreasing sequences in a list of numbers.

        Parameters:
        sequence (List[int]): The list of numbers.

        Returns:
        Tuple[List[int], List[int]]: A tuple containing the longest increasing sequence and the longest decreasing
        sequence found in the list.
    """
    try:
        # Початок вимірювання часу виконання функції.
        start_time = timeit.default_timer()

        # Визначення довжини вхідного списку.
        n = len(sequence)
        # Перевірка, чи список порожній.
        if n == 0:
            # Повернення порожніх списків у випадку порожнього вхідного списку.
            return [], []

        # Ініціалізація списків довжин найбільших зростаючих та спадаючих послідовностей.
        increasing_lengths = np.ones(n, dtype=np.int32)
        decreasing_lengths = np.ones(n, dtype=np.int32)

        # Ітерація по елементам списку, починаючи з індексу 1.
        for i in range(1, n):
            # Перевірка, чи елемент більший за попередній.
            if sequence[i] > sequence[i - 1]:
                # Інкрементування довжини зростаючої послідовності.
                increasing_lengths[i] = increasing_lengths[i - 1] + 1
            # Перевірка, чи елемент менший за попередній.
            if sequence[i] < sequence[i - 1]:
                # Інкрементування довжини спадаючої послідовності.
                decreasing_lengths[i] = decreasing_lengths[i - 1] + 1

        # Знаходження максимальної довжини зростаючої та спадаючої послідовностей.
        max_increasing_length = np.max(increasing_lengths)
        max_decreasing_length = np.max(decreasing_lengths)

        # Визначення зростаючої послідовності за допомогою знаходження максимального значення довжини.
        increasing_sequence = sequence[np.argmax(increasing_lengths) - max_increasing_length + 1: np.argmax(
            increasing_lengths) + 1]
        # Визначення спадаючої послідовності за допомогою знаходження максимального значення довжини.
        decreasing_sequence = sequence[np.argmax(decreasing_lengths) - max_decreasing_length + 1: np.argmax(
            decreasing_lengths) + 1]

        # Зупиняємо таймер та обчислюємо час виконання
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info(f"Time taken for find_longest_sequence: {round(execution_time, 5)} seconds")

        # Повернення знайдених послідовностей.
        return increasing_sequence, decreasing_sequence

    # Обробка виняткових ситуацій.
    except Exception as e:
        # Отримуємо детальну інформацію про помилку
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"An error occurred while finding the longest sequence: {e}\n{detailed_send_message_error}")
        # Повернення порожніх списків у випадку помилки.
        return [], []

# bot_guess_the_number_dictionary/utils/client_utils.py
import random

from logger import logger

# Словарь, в котором будут храниться данные пользователя
users = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    """
    Generate a random integer between 1 and 100.

    Returns:
        int: Random integer.
    """
    hidden_number = random.randint(1, 100)
    logger.info(f"The random number is {hidden_number}")
    return hidden_number

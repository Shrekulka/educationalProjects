# bot_guess_the_number/utils/client_utils.py

import random

from logger import logger


def get_random_number() -> int:
    """
    Generate a random integer between 1 and 100.

    Returns:
        int: Random integer.
    """
    hidden_number = random.randint(1, 100)
    logger.info(f"The random number is {hidden_number}")
    return hidden_number

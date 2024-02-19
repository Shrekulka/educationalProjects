# bot_rock_paper_scissors/services/services.py

import random

from lexicon.lexicon_ru import LEXICON_RU
from logger_config import logger
from services import game_state

# Cловарь, который содержит соответствия между выбором в игре "Камень, Ножницы, Бумага" и их текстовыми описаниями
# на русском языке. Каждому ключу в словаре соответствует текстовое описание из словаря LEXICON_RU.
rps_dict = {
    'rock': LEXICON_RU['rock'],  # Соответствие выбора 'rock' текстовому описанию из словаря LEXICON_RU
    'paper': LEXICON_RU['paper'],  # Соответствие выбора 'paper' текстовому описанию из словаря LEXICON_RU
    'scissors': LEXICON_RU['scissors'],  # Соответствие выбора 'scissors' текстовому описанию из словаря LEXICON_RU
}


# Функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    """
        Returns a random choice for the bot in the game.

        Returns:
            str: The bot's choice.
    """
    # Получение всех ключей из словаря rps_dict
    keys = rps_dict.keys()
    # Записываем случайное значение из списка ключей в bot_choice
    bot_choice = random.choice(list(keys))
    logger.debug(f"Bot choice: {bot_choice}")
    # Возвращает случайное значение из списка ключей
    return bot_choice


# Функция, возвращающая ключ из словаря, по которому хранится значение, передаваемое как аргумент - выбор пользователя
# Функция начинается с нижнего подчеркивания, говорит о том, что используется она только внутри модуля и не должна
# "смотреть" наружу.
def _normalize_user_answer(user_answer: str) -> str:
    """
        Returns the key from the dictionary corresponding to the value passed as an argument, which is the user's
        choice.

        Args:
            user_answer (str): The user's choice.

        Returns:
            str: The key corresponding to the user's choice in the dictionary.
    """
    key = None
    # Проход по ключам словаря rps_dict
    for key in rps_dict:
        # Если значение, соответствующее текущему ключу, равно user_answer
        if rps_dict[key] == user_answer:
            break  # Прерываем цикл
    logger.debug(f"Normalized user answer: {key}")
    # Возвращаем текущий ключ, соответствующий значению user_answer
    return key


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    """
        Determines the winner of the game.

        Args:
            user_choice (str): The user's choice.
            bot_choice (str): The bot's choice.

        Returns:
            str: The result of the game ('nobody_won', 'user_won', or 'bot_won').
    """
    # Нормализация выбора пользователя с помощью функции _normalize_user_answer
    user_choice = _normalize_user_answer(user_choice)
    # Определение правил игры: камень побеждает ножницы, ножницы побеждают бумагу, бумага побеждает камень
    rules = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    # Если выбор пользователя равен выбору бота, игра заканчивается вничью
    if user_choice == bot_choice:
        result = 'nobody_won'
    # Если выбор пользователя побеждает выбор бота согласно правилам игры
    elif rules[user_choice] == bot_choice:
        # Пользователь побеждает
        result = 'user_won'
        game_state.user_score += 1
    else:
        # В противном случае побеждает бот
        result = 'bot_won'
        game_state.bot_score += 1

    logger.debug(f"Game result: {result}")
    return result

# naval_combat_game/services/game_services.py

import copy

from config_data.game_config_data import FIELD_SIZE
from database.game_database import users
from models.game_models import generate_ships


# Определение функции reset_field, которая обновляет игровое поле для каждого игрока
def reset_field(user_id: int) -> None:
    """
        Reset the game field for the specified user.

        This function updates the game field for the specified user by resetting the ship positions
        and initializing a new empty game field.

        Args:
            user_id (int): The ID of the user whose game field needs to be reset.

        Returns:
            None
    """
    # Записываем в "базу данных" новое расположение кораблей для указанного пользователя
    users[user_id]['ships'] = copy.deepcopy(generate_ships())
    # Инициализируем новое пустое игровое поле для указанного пользователя
    # Этот код создает двумерный список (матрицу) размером FIELD_SIZE x FIELD_SIZE, где каждая строка представлена
    # списком из FIELD_SIZE элементов, и каждый элемент в этой строке инициализируется значением 0.
    users[user_id]['field'] = [
        [0 for _ in range(FIELD_SIZE)]  # Создаем список с FIELD_SIZE нулями для каждой строки поля
        for _ in range(FIELD_SIZE)]     # Создаем FIELD_SIZE строк для поля

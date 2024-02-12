# bot_guess_the_number/models/user_game_data.py

from dataclasses import dataclass

from config import ATTEMPTS


@dataclass
class UserGameData:
    """
        Class to store game data for the current user.

        Attributes:
            is_playing (bool): Flag indicating whether the user is currently playing.
            target_number (int): The number chosen by the bot for guessing.
            remaining_attempts (int): The number of remaining attempts.
            total_games (int): Total number of games played.
            games_won (int): Number of games won.
    """
    user_id: int                        # Идентификатор пользователя
    is_playing: bool = False            # Флаг, указывающий, играет ли пользователь в игру
    target_number: int = None           # Загаданное число
    remaining_attempts: int = ATTEMPTS  # Количество оставшихся попыток
    total_games: int = 0                # Общее количество сыгранных игр
    games_won: int = 0                  # Количество выигранных игр

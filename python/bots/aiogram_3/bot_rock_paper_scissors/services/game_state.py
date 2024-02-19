# bot_rock_paper_scissors/services/game_state.py

# Инициализация переменных для хранения счета пользователя и бота
user_score: int = 0
bot_score: int = 0


# Определение функции reset_game для сброса счета игры
def reset_game() -> None:
    """
        Resets the game score, setting the user's and bot's scores to 0.

        Returns:
            None
    """
    # Обнуление счета пользователя и бота при вызове функции
    global user_score, bot_score
    user_score = 0
    bot_score = 0

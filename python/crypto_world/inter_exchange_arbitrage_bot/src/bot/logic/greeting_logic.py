# inter_exchange_arbitrage_bot/src/bot/logic/greeting_logic.py

import random
import datetime

from src.constants.trading_greetings import TIME_GREETING_MAP, REPEATED_GREETINGS

# --- НАША ЛЕГКОВЕСНАЯ "ПАМЯТЬ" ---
# Словарь для хранения последнего временного блока приветствия для каждого пользователя
# Формат: {user_id: (start_hour, end_hour)}
# Эта переменная будет жить, пока работает бот.
USER_GREETING_STATE = {}


def get_dynamic_greeting(user_id: int) -> str:
    """
    Генерирует умное приветствие для трейдера.
    Отправляет полное приветствие только один раз за временной блок (утро/день/вечер).
    При повторных вызовах возвращает короткую фразу.
    """
    hour = datetime.datetime.now().hour

    # Находим текущий временной блок
    current_block = next(
        (time_range for time_range in TIME_GREETING_MAP if time_range[0] <= hour < time_range[1]),
        None
    )

    # Получаем последний блок, в котором мы приветствовали пользователя
    last_greeted_block = USER_GREETING_STATE.get(user_id)

    # Если мы находимся в том же блоке, что и в прошлый раз, возвращаем короткую фразу
    if current_block and current_block == last_greeted_block:
        return random.choice(REPEATED_GREETINGS)

    # Если это новый блок (или первый вход), генерируем полное приветствие
    if current_block:
        greeting_list = TIME_GREETING_MAP[current_block]
        # "Запоминаем", что мы поприветствовали пользователя в этом блоке
        USER_GREETING_STATE[user_id] = current_block
        return random.choice(greeting_list)
    else:
        # Фраза на случай, если что-то пошло не так
        USER_GREETING_STATE[user_id] = "default"
        return "Удачной торговли"
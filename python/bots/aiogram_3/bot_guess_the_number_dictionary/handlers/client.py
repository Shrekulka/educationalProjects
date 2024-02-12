# bot_guess_the_number_dictionary/handlers/client.py
import traceback

from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import ATTEMPTS, POSITIVE_RESPONSE, NEGATIVE_RESPONSE
from create_bot import bot
from utils.client_utils import users, get_random_number


# Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
        Handles the /start command, sends a welcome message to the user with their name and suggests starting the
        "Guess the number" game. Removes the /start command from the chat.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None

        Exceptions:
            If an error occurs while sending the message, returns information about the error.
    """
    try:
        # Отправка приветственного сообщения с именем пользователя и предложение начать игру
        await bot.send_message(message.from_user.id,
                               f"Hello, {message.from_user.first_name}! 👋\n\nLet's play 'Guess the number'?"
                               f"\n\nTo get the rules and a list of available commands, send /help 🎮")
        # Удаление команды /start из чата
        await message.delete()

        # Если пользователь только запустил бота и его ID отсутствует в словаре 'users',
        # добавляем его в словарь со значениями по умолчанию для состояния игры.
        if message.from_user.id not in users:
            users[message.from_user.id] = {
                'in_game': False,  # Флаг, указывающий, играет ли пользователь в данный момент.
                'secret_number': None,  # Загаданное число для текущей игры (если игра активна).
                'attempts': None,  # Количество попыток, оставшихся у пользователя в текущей игре.
                'total_games': 0,  # Общее количество игр, сыгранных пользователем.
                'wins': 0  # Количество выигранных игр пользователем.
            }

    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    """
        Handles the /help command, sends the game rules and a list of available commands to the user.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None
    """
    # Отправляем сообщение с правилами игры и списком команд
    await message.answer(f"Game rules:\n\nI choose a number between 1 and 100, and you need to guess it"
                         f"\nYou have {ATTEMPTS} attempts\n\nAvailable commands:\n/help - game "
                         f"rules and command list\n/cancel - exit the game\n/stat - view statistics\n\nLet's play? 🎲")


# Этот хэндлер будет срабатывать на команду "/stat"
# @dp.message(Command(commands='stat'))
async def process_stat_command(message: Message) -> None:
    """
        Handles the /stat command, sending the user's game statistics.

        Arguments:
            message (Message): The message object containing information about the user.

        Returns:
            None
    """
    # Проверяем, есть ли у пользователя данные об игре в словаре пользователей.
    # Если данных нет, отправляем сообщение о том, что у него пока нет статистики.
    if message.from_user.id not in users:
        await message.answer("You don't have any game statistics yet. 📊")
        return
    # Отправляем сообщение со статистикой игры пользователя
    await message.answer(f"🎮 Total games played: {users[message.from_user.id]["total_games"]}\n"
                         f"🏆 Games won: {users[message.from_user.id]["wins"]}")


# Этот хэндлер будет срабатывать на команду "/cancel"
# @dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message) -> None:
    """
        Handles the /cancel command, allows the user to exit the game.

        Arguments:
            message (Message): The message object containing information about the user who sent the command.

        Returns:
            None
    """
    # Если пользователь находится в игре (флаг in_game установлен в True)
    if users[message.from_user.id]['in_game']:
        # устанавливаем этот флаг в False, чтобы он вышел из игры, и отправляем сообщение об этом.
        users[message.from_user.id]['in_game'] = False
        # Отправляем сообщение о том, что пользователь вышел из игры
        await message.answer("You have exited the game. If you want to play again, let me know. 😔")
    # Если пользователь не играет, отправляем сообщение о том, что мы не играем с ним, но можем поиграть один раз
    else:
        await message.answer("We're not playing with you anyway. Maybe let's play once? 😉")


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
# @dp.message(F.text.lower().in_(POSITIVE_RESPONSE))
async def process_positive_answer(message: Message) -> None:
    """
       Handles the user's positive response to play the game.

       Args:
           message (Message): The message object containing the user's response.

       Returns:
           None
    """
    # Проверяем, не находится ли пользователь уже в игре. Если пользователь не в игре (флаг in_game равен False),
    if not users[message.from_user.id]['in_game']:
        # устанавливаем этот флаг в True, чтобы начать новую игру.
        users[message.from_user.id]['in_game'] = True
        # Затем генерируем новое случайное число для пользователя
        users[message.from_user.id]['secret_number'] = get_random_number()
        # и устанавливаем количество попыток для него.
        users[message.from_user.id]['attempts'] = ATTEMPTS
        # Отправляем сообщение о начале игры
        await message.answer("Hooray! 🎉\n\nI've chosen a number between 1 and 100, try to guess it!")
    # Если пользователь уже играет, отправляем сообщение о том, что мы можем реагировать только на числа от 1 до 100
    # и команды /cancel и /stat во время игры
    else:
        await message.answer("I can only react to numbers from 1 to 100 and the commands "
                             "/cancel and /stat while we're playing the game. 🎲")


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
# @dp.message(F.text.lower().in_(NEGATIVE_RESPONSE))
async def process_negative_answer(message: Message) -> None:
    """
        Handles the user's negative response to play the game.

        Args:
            message (Message): The message object containing the user's response.

        Returns:
            None
    """
    # Если пользователь не играет, отправляем сообщение о том, что это жаль, и предлагаем сыграть снова
    if not users[message.from_user.id]['in_game']:
        await message.answer("That\'s too bad. 😔\n\nIf you want to play again, just let me know.")
    # Если пользователь уже играет, отправляем сообщение о том, что мы сейчас играем, и просим отправлять числа 1-100
    else:
        await message.answer("We are currently playing a game. Please send numbers from 1 to 100. 🎲")


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
# @dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message) -> None:
    """
        Handles the user's numeric responses during the game.

        Args:
            message (Message): The message object containing the user's response.

        Returns:
            None
    """
    # Если пользователь находится в состоянии игры, выполняем следующие действия:
    if users[message.from_user.id]['in_game']:

        # Если у пользователя закончились попытки:
        if users[message.from_user.id]['attempts'] == 0:
            # Завершаем игру, увеличиваем счетчик общих игр и отправляем сообщение о проигрыше.
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            # Отправляем сообщение о том, что пользователь проиграл и предлагаем сыграть ещё раз
            await message.answer(f"Unfortunately, you have no more attempts left. You lost. 😔\n\nMy number "
                                 f"was {users[message.from_user.id]["secret_number"]}\n\nLet\'s play again? 🎮")

        # Если введенное пользователем число совпадает с загаданным числом:
        elif int(message.text) == users[message.from_user.id]['secret_number']:
            # Пользователь угадал число, завершаем игру и увеличиваем счетчики побед и общих игр.
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            # Отправляем сообщение о том, что пользователь угадал число и предлагаем сыграть ещё раз
            await message.answer("Hooray!!! You guessed the number! 🎉\n\nMaybe let\'s play again? 🎮")

        # Если введенное число больше загаданного:
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            # Уменьшаем количество оставшихся попыток и отправляем сообщение.
            count_attempts = users[message.from_user.id]['attempts'] - 1  # Уменьшаем количество попыток на 1
            users[message.from_user.id]['attempts'] = count_attempts  # Обновляем количество попыток в словаре
            # Отправляем сообщение о том, что число меньше введенного и указываем количество оставшихся попыток
            await message.answer(f"My number is lower. 🔽\nYou have {count_attempts} attempts left.")

        # Если введенное число меньше загаданного:
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            # Уменьшаем количество оставшихся попыток и отправляем сообщение.
            count_attempts = users[message.from_user.id]['attempts'] - 1  # Уменьшаем количество попыток на 1
            users[message.from_user.id]['attempts'] = count_attempts  # Обновляем количество попыток в словаре
            # Отправляем сообщение о том, что число больше введенного и указываем количество оставшихся попыток
            await message.answer(f"My number is higher. 🔼\nYou have {count_attempts} attempts left.")

    # Если пользователь ещё не начал игру, отправляем сообщение с предложением начать игру
    else:
        await message.answer("We are not playing yet. Do you want to play? 🎲")


# Этот хэндлер будет срабатывать на остальные любые сообщения
# @dp.message()
async def process_other_answers(message: Message) -> None:
    """
       Handles any other user's responses.

       Args:
           message (Message): The message object containing the user's response.

       Returns:
           None
    """
    # Если пользователь уже играет, отправляем сообщение о том, что игра уже идёт
    if users[message.from_user.id]['in_game']:
        await message.answer("We are currently playing a game. Please send numbers from 1 to 100. 🎯")
    # Если пользователь не играет, отправляем сообщение с предложением начать игру
    else:
        await message.answer("I'm a pretty limited bot, let's just play a game, shall we? 😅")


def register_handlers_client(dp: Dispatcher) -> None:
    """
        Register all handlers for the client part of the bot.

        Args:
            dp: The Dispatcher instance.
    """
    # Регистрируем хэндлеры команд
    dp.message.register(process_start_command, CommandStart())  # Обработка команды /start
    dp.message.register(process_stat_command, Command(commands='stat'))  # Обработка команды /stat
    dp.message.register(process_help_command, Command(commands='help'))  # Обработка команды /help
    dp.message.register(process_cancel_command, Command(commands='cancel'))  # Обработка команды /cancel

    # Регистрируем хэндлеры ответов пользователя

    # Обработка положительных ответов пользователя
    dp.message.register(process_positive_answer, lambda m: m.text.lower() in POSITIVE_RESPONSE)
    # Обработка отрицательных ответов пользователя
    dp.message.register(process_negative_answer, lambda m: m.text.lower() in NEGATIVE_RESPONSE)
    # Обработка числовых ответов пользователя
    dp.message.register(process_numbers_answer, lambda m: m.text.isdigit() and 1 <= int(m.text) <= 100)
    # Обработка прочих ответов пользователя
    dp.message.register(process_other_answers)

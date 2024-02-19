# bot_rock_paper_scissors/handlers/user_handlers.py

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import services.game_state as gs
from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU
from services import game_state
from services.services import get_bot_choice, get_winner

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
       Handles the /start command.

       Sends a greeting message and offers the user to start the game.

       Args:
           message (Message): The incoming message.

       Returns:
           None
    """
    # Отправляет сообщение с текстом из словаря LEXICON_RU для команды /start с клавиатурой yes_no_kb
    await message.answer(text=LEXICON_RU['/start'].format(first_name=message.from_user.first_name),
                         reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    """
        Handles the /help command.

        Sends a help message explaining the rules of the game.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    # Отправляет сообщение со справкой из словаря LEXICON_RU с клавиатурой yes_no_kb
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_answer(message: Message) -> None:
    """
        Handles the user's agreement to play the game.

        Sends a message prompting the user to make a choice.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    # При старте новой игры обнулять счет:
    game_state.reset_game()
    # Отправляет сообщение с текстом "yes" из словаря LEXICON_RU с клавиатурой game_kb
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message) -> None:
    """
        Handles the user's refusal to play the game.

        Sends a message confirming the user's decision.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    # Отправляет сообщение с подтверждением отказа пользователя
    await message.answer(text=LEXICON_RU['no'].format(bot_score=gs.bot_score, user_score=gs.user_score))


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(F.text.in_([LEXICON_RU['rock'], LEXICON_RU['paper'], LEXICON_RU['scissors']]))
async def process_game_button(message: Message) -> None:
    """
        Handles the user's selection of a game option.

        Determines the bot's choice, announces it, and determines the winner.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    # Получение выбора бота (камень, ножницы или бумага)
    bot_choice = get_bot_choice()
    # Отправка сообщения с выбором бота пользователю
    await message.answer(text=f"{LEXICON_RU["bot_choice"]} - {LEXICON_RU[bot_choice]}")
    # Определение победителя игры
    winner = get_winner(message.text, bot_choice)
    # Отправка сообщения о победителе с кнопками для новой игры
    await message.answer(text=LEXICON_RU[winner].format(bot_score=gs.bot_score, user_score=gs.user_score),
                         reply_markup=yes_no_kb)

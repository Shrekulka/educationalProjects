# telegram_bot_menu_button/keyboards/set_menu.py
from typing import List

from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_COMMANDS_RU


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot) -> None:
    """
        Sets up the main menu of the bot using commands and their descriptions from the LEXICON_COMMANDS_RU dictionary.

        Args:
            bot (Bot): The bot object.

        Returns:
            None
    """
    # Создание списка команд main_menu_commands с помощью генератора списка, где каждый элемент представляет собой
    # объект BotCommand с командой и её описанием, извлеченными из словаря LEXICON_COMMANDS_RU.
    main_menu_commands: List[BotCommand] = [
        BotCommand(command=command, description=description) for command, description in LEXICON_COMMANDS_RU.items()]

    # Установка нового набора команд бота с использованием созданного списка main_menu_commands с помощью
    # метода set_my_commands.
    await bot.set_my_commands(main_menu_commands)


# telegram_bot_book/keyboards/main_menu.py

from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_COMMANDS


# Функция для установки главного меню бота.
async def set_main_menu(bot: Bot) -> None:
    """
        Setting up the main menu of the bot.

        This asynchronous function configures the "Menu" button in the bot.
        It creates a list of commands for the main menu using data from the LEXICON_COMMANDS dictionary.
        Each command in the main menu consists of a pair of "command"-"description".
        After creating the list of commands, the function sets them for the bot using the set_my_commands method.

        Parameters:
        bot (Bot): The bot object for which the main menu is being configured.

        Returns:
        None
    """
    # Формируем список команд главного меню, используя названия и описания из словаря LEXICON_COMMANDS.
    main_menu_commands = [BotCommand(command=command, description=description)
                          for command, description in LEXICON_COMMANDS.items()]

    # Устанавливаем для бота список команд в соответствии с главным меню.
    await bot.set_my_commands(main_menu_commands)

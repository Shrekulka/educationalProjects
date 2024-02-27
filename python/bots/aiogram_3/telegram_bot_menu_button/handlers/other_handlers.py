# telegram_bot_menu_button/handlers/other_handlers.py

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.set_menu import set_main_menu

router = Router()


# Иногда нужно не просто изменить команды, доступные по нажатию на кнопку Menu, а нужно полное их удаление вместе с
# кнопкой. Для этого тоже есть метод у объекта типа Bot - delete_my_commands()

# Этот хэндлер будет срабатывать на команду "/delmenu" и удалять кнопку Menu c командами
@router.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot: Bot) -> None:
    """
        Handles the /delmenu command by removing the "Menu" button from the main menu.

        Args:
            message (Message): The message object.
            bot (Bot): The bot object.

        Returns:
            None
    """
    await bot.delete_my_commands()
    await message.answer(text="Кнопка 'Menu' удалена. Для возвращения /restore_menu",
                         reply_markup=ReplyKeyboardRemove())


# Хэндлер для команды /restore_menu
@router.message(Command(commands="restore_menu"))
async def restore_main_menu(message: Message, bot: Bot):
    """
        Handles the /restore_menu command by restoring the main menu.

        Args:
            message (Message): The message object.
            bot (Bot): The bot object.

        Returns:
            None
    """
    await set_main_menu(bot)  # Вызов функции для восстановления главного меню
    await message.answer("Главное меню было восстановлено!")

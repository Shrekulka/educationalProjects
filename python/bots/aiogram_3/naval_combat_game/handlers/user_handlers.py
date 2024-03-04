# naval_combat_game/handlers/user_handlers.py

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from database.game_database import users
from filters.game_filters import FieldCallbackFactory
from keyboards.game_keyboard import get_field_keyboard
from lexicon.game_lexicon import LEXICON
from services.game_services import reset_field

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду /start, записывать пользователя в "базу данных", обнулять игровое поле и
# отправлять пользователю сообщение с клавиатурой
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
        Handle the /start command to initialize the game for the user.

        This function handles the /start command by initializing the game for the user.
        It registers the user in the game database, resets the game field, and sends a welcome message with the game
        keyboard.

        Args:
            message (Message): The message object containing information about the command.

        Returns:
            None
    """
    # Проверяем, есть ли идентификатор пользователя в базе данных игры
    if message.from_user.id not in users:
        # Если пользователя нет в базе данных, создаем для него запись с пустым словарем
        users[message.from_user.id] = {}
    # Сбрасываем игровое поле для пользователя, инициализируя новое поле
    reset_field(message.from_user.id)
    # Отправляем сообщение пользователю с текстом, полученным из LEXICON по ключу '/start',
    # и клавиатурой, сформированной на основе его идентификатора пользователя
    await message.answer(text=LEXICON['/start'], reply_markup=get_field_keyboard(message.from_user.id))


# Этот хэндлер будет срабатывать на нажатие любой инлайн-кнопки на поле, запускать логику проверки результата нажатия и
# формирования ответа
@router.callback_query(FieldCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery, callback_data: FieldCallbackFactory) -> None:
    """
        Handle the callback query when any inline button on the game field is pressed.

        This function processes the callback query when any inline button on the game field is pressed.
        It updates the game field based on the user's action and sends a response message accordingly.

        Args:
            callback (CallbackQuery): The callback query object containing information about the button press.
            callback_data (FieldCallbackFactory): The callback data containing the coordinates of the pressed button.

        Returns:
            None
    """
    # Получаем игровое поле и расположение кораблей для пользователя, совершившего нажатие
    field = users[callback.from_user.id]['field']
    ships = users[callback.from_user.id]['ships']

    # Проверяем, что в клетке, по которой было совершено нажатие, нет ни корабля, ни попадания
    if field[callback_data.x][callback_data.y] == 0 and \
            ships[callback_data.x][callback_data.y] == 0:
        # Если в клетке нет корабля и не было попадания, устанавливаем ответ "Мимо!"
        answer = LEXICON['miss']
        # Отмечаем клетку как промах (значение 1 обозначает промах)
        field[callback_data.x][callback_data.y] = 1
    # Проверяем, что в клетке, по которой было совершено нажатие, есть корабль
    elif field[callback_data.x][callback_data.y] == 0 and \
            ships[callback_data.x][callback_data.y] == 1:
        # Если в клетке есть корабль устанавливаем ответ "Попал!"
        answer = LEXICON['hit']
        # Отмечаем клетку как попадание (значение 2 обозначает попадание)
        field[callback_data.x][callback_data.y] = 2
    else:
        # Если клетка уже была открыта, устанавливаем ответ "Вы уже стреляли сюда!"
        answer = LEXICON['used']

    try:
        # Пытаемся изменить текст сообщения, чтобы обновить игровое поле и клавиатуру
        await callback.message.edit_text(
            text=LEXICON['next_move'],
            reply_markup=get_field_keyboard(callback.from_user.id))
    except TelegramBadRequest:
        # Если возникла ошибка при изменении текста сообщения, отправляем ответ о возникшей ошибке
        await callback.answer("Произошла ошибка при обработке вашего запроса.")

    # Отправляем ответ пользователю
    await callback.answer(answer)

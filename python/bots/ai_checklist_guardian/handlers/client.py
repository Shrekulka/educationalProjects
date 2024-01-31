# ai_checklist_guardian/handlers/client.py
import traceback

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import bot, dp
from data_base.sqlite_db import sql_add_report, get_report
from keyboards.client_kb import kb_client_locations, kb_checklist
from logger import logger
from models.user_data import UserData
from services.openai_service import OpenAIService
from states import UserSteps

# Создание экземпляра службы OpenAI
openai_service = OpenAIService()

# Создание объекта данных пользователя
user_data = UserData()


# Хендлер приветствия при старте
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message) -> None:
    """
         Handle the /start command, initialize the conversation and ask the user to choose a location.

         Args:
             message: The incoming message.
    """
    try:
        # Отправка приветственного сообщения с именем пользователя
        await bot.send_message(message.from_user.id, f"Hello, {message.from_user.first_name}!"
                                                     f" 👋\nLet's get to work.")
        # Удаление команды /start из чата
        await message.delete()
        # Просим пользователя выбрать локацию
        await message.answer("Choose a location:", reply_markup=kb_client_locations)
        # Устанавливаем состояние пользователя в LOCATION
        await UserSteps.LOCATION.set()
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Хендлер для обработки выбора локации
@dp.message_handler(state=UserSteps.LOCATION, content_types=types.ContentTypes.TEXT)
async def process_location(message: types.Message) -> None:
    """
       Handle the user's chosen location, ask for a checklist option, and set the user's state to CHECKLIST.

       Args:
           message: The incoming message.
    """
    try:
        # Получение выбранной локации из сообщения пользователя
        location = message.text
        # Сохраняем выбранную локацию в user_data
        user_data.location = location
        # Просим пользователя выбрать вариант чек-листа
        await message.answer("Choose a checklist option:", reply_markup=kb_checklist)
        # Устанавливаем состояние пользователя в CHECKLIST
        await UserSteps.CHECKLIST.set()
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Хендлер для обработки выбора варианта чек-листа
@dp.message_handler(state=UserSteps.CHECKLIST, content_types=types.ContentTypes.TEXT)
async def process_checklist(message: types.Message, state: FSMContext) -> None:
    """
       Handle the user's chosen checklist option and set the user's state accordingly.

       Args:
           message: The incoming message.
           state: The FSMContext to manage the user's state.
    """
    try:
        # Получение выбранного варианта чек-листа из сообщения пользователя
        option = message.text
        # Сохранение выбранного варианта чек-листа в user_data
        user_data.option = option
        # Если пользователь выбрал опцию "Оставить комментарий"
        if option == "Leave comment":
            # Установка состояния пользователя в COMMENT
            await UserSteps.COMMENT.set()
            # Просьба пользователя оставить комментарий
            await message.answer("Leave a comment:")
        # Если выбран другой вариант
        else:
            # Установка состояния пользователя в REPORT и переход к формированию и отправке отчета
            await UserSteps.REPORT.set()
            await send_report(message, state, checklist=option)
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Хендлер для ожидания комментария
@dp.message_handler(state=UserSteps.COMMENT, content_types=types.ContentTypes.TEXT)
async def process_comment(message: types.Message) -> None:
    """
       Handle the user's comment and proceed to the next step in the conversation.

       Args:
           message: The incoming message.
    """
    try:
        # Получение текста комментария из сообщения пользователя
        comment_text = message.text
        # Сохраняем комментарий в user_data
        user_data.comment = comment_text
        # После сохранения комментария, просим пользователя загрузить фотографию
        await message.answer("Now, please upload a photo.")
        # Устанавливаем состояние пользователя в PHOTO
        await UserSteps.PHOTO.set()
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Хендлер для ожидания загрузки фотографии
@dp.message_handler(state=UserSteps.PHOTO, content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message, state: FSMContext) -> None:
    """
        Handle the user's uploaded photo, process it, and proceed to the next step in the conversation.

        Args:
            message: The incoming message.
            state: The FSMContext to manage the user's state.
    """
    try:
        # Обрабатываем фотографию
        photo_link = message.photo[-1].file_id
        # Сохраняем ссылку на фотографию в user_data
        user_data.photo_link = photo_link
        # Устанавливаем состояние пользователя в REPORT
        await UserSteps.REPORT.set()
        # После сохранения фотографии, переходим к формированию и отправке отчета
        await send_report(message, state, checklist=user_data.option)
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Хендлер для формирования и отправки отчета на OpenAI
async def send_report(message: types.Message, state: FSMContext, checklist) -> None:
    """
        Handle the process of generating and sending a report to OpenAI.

        Args:
            message: The incoming message.
            state: The FSMContext to manage the user's state.
            checklist: The chosen checklist option.
    """
    user_data_local = None
    try:
        # Получение данных из state
        data = await state.get_data()
        for key, value in data.items():
            logger.info(f"Key: {key}, Value: {value}")

        # Создание объекта UserData
        user_data_local = UserData(
            location=user_data.location,
            option=user_data.option,
            comment=user_data.comment,
            photo_link=user_data.photo_link,
            report=user_data.report  # report=user_data_local.get("report")
        )
        # Получение словаря атрибутов объекта user_data_local
        user_data_dict = vars(user_data_local)
        # Использование цикла для вывода ключей и значений
        for key, value in user_data_dict.items():
            logger.info(f"Key: {key}, Value: {value}")
        # Формирование текста отчета на основе user_data
        report_text = user_data_local.generate_report()
        # Отправка отчета в OpenAI
        ai_response = openai_service.send_report(report_text, checklist=checklist)
        # Отправка анализированного отчета пользователю
        await message.answer(f"Report analysis:\n{ai_response}")
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")

    finally:
        try:
            # Сохранение данных в БД
            await sql_add_report(user_data_local)
            # Получение отчета из базы данных
            user_id = message.from_user.id
            report_from_db = await get_report(user_id)

            if report_from_db:
                # Отправка сохраненного отчета пользователю
                await bot.send_message(user_id, report_from_db)
            else:
                await bot.send_message(user_id, "Report not found.")
        except Exception as e:
            detailed_send_message_error = traceback.format_exc()
            await message.reply(f"An error occurred while working with the database:"
                                f" {str(e)}\n{detailed_send_message_error}")
        finally:
            # Сброс состояния пользователя
            await state.finish()


# Регистрация всех хэндлеров и передача их в файл bot_telegram
def register_handlers_client(dp: Dispatcher) -> None:
    """
        Register all handlers for the client part of the bot.

        Args:
            dp: The Dispatcher instance.
    """
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(process_location, state=UserSteps.LOCATION, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(process_checklist, state=UserSteps.CHECKLIST, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(process_comment, state=UserSteps.COMMENT, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(process_photo, state=UserSteps.PHOTO, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(send_report, state=UserSteps.REPORT, content_types=types.ContentTypes.TEXT)

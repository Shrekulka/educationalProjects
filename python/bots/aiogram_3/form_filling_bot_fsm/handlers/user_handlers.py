# form_filling_bot_fsm/handlers/user_handlers.py

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (Message, CallbackQuery, PhotoSize)

from database.database import user_dict
from keyboards.keyboard import markup_gender, markup_education, markup_news
from lexicon.lexicon import LEXICON_RU
from logger_config import logger
from states.states import FSMFillForm

# Инициализируем роутер уровня модуля
user_router: Router = Router()


# Этот хэндлер будет срабатывать на команду /start вне состояний и предлагать перейти к заполнению анкеты, отправив
# команду /fillform
@user_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message) -> None:
    """
        Обрабатывает команду /start в состоянии default_state.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Description:
            Обработчик команды /start в состоянии default_state.
            default_state - это специальное состояние машины состояний (FSM), которое означает "состояние по
            умолчанию" или "вне состояний". Оно используется для определения поведения бота, когда он не находится
            ни в одном из определенных состояний FSM.
            StateFilter(default_state) - это фильтр, который пропускает событие в хэндлер только если бот находится
            в состоянии default_state.
            Отправляет пользователю приветственное сообщение из словаря LEXICON_RU['start'], определяя язык
            пользователя по его настройкам. Также предлагает перейти к заполнению анкеты, отправив команду
            /fillform.
    """
    # Отправляем пользователю сообщение с текстом из словаря LEXICON_RU['start'], определяя язык пользователя, который
    # он установил в настройках
    await message.answer(text=LEXICON_RU['start'].format(language=message.from_user.language_code))


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии по умолчанию и сообщать, что эта команда работает
# внутри машины состояний
@user_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message) -> None:
    """
        Обрабатывает команду /cancel в состоянии default_state.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Description:
            Этот хэндлер срабатывает на команду "/cancel" в состоянии по умолчанию и сообщает, что эта команда работает
            внутри машины состояний. В процессе заполнения анкеты, то есть внутри машины состояний, можно через отправку
            команды /cancel выходить из FSM и удалять все данные, накопленные в процессе ее работы. Но в состоянии "по
            умолчанию" нет никаких данных, поэтому сбрасывать нечему. Вне состояний выводится сообщение, что здесь
            использование команды ни к чему не приведет.
        """
    await message.answer(text=LEXICON_RU['cancel'].format(username=message.from_user.username))


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях, кроме состояния по умолчанию, и отключать
# машину состояний
@user_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext) -> None:
    """
        Обрабатывает команду /cancel в любых состояниях, кроме состояния default_state.

        Args:
            message (Message): Объект сообщения от пользователя.
            state (FSMContext): Контекст Finite State Machine для управления состояниями.

        Returns:
            None

        Description:
            Этот хэндлер срабатывает на команду "/cancel" в любых состояниях, кроме состояния "по умолчанию", и
            отключает машину состояний. Если пользователь отправляет команду /cancel находясь внутри машины
            состояний, ему приходит сообщение о том, что он вышел из FSM, и контекст очищается с помощью await
            state.clear(). Таким образом, информация о текущем состоянии и данные, полученные внутри состояний от
            пользователя, удаляются. В результате состояние переходит в состояние по умолчанию, а данные обнуляются.

        Note:
            Для отлова команды /cancel в любом состоянии, кроме состояния по умолчанию, используется дополнительный
             фильтр ~StateFilter(default_state), где ~ выполняет функцию логического отрицания. То есть фильтр
             пропускает апдейты в хэндлер в любом состоянии, кроме состояния "по умолчанию".
    """

    # Отправляем пользователю сообщение о том, что он вышел из машины состояний, подставляя его полное имя из объекта
    # сообщения message.
    await message.answer(text=LEXICON_RU['cancel_out_of_state'].format(full_name=message.from_user.full_name))
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /fillform и переводить бота в состояние ожидания ввода имени
@user_router.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext) -> None:
    """
        Обрабатывает команду /fillform для начала заполнения анкеты.

        Args:
            message (Message): Объект сообщения от пользователя.
            state (FSMContext): Контекст состояния бота.

        Returns:
            None

        Этот хэндлер будет срабатывать на команду /fillform и переводить бота в состояние ожидания ввода имени.
        Пользователю будет отправлено сообщение с просьбой ввести его имя, а затем бот будет переведен в состояние
        ожидания ввода имени.
    """
    # Отправляем пользователю запрос на ввод его имени, используя текст из словаря LEXICON_RU, и подставляем в него ID
    # пользователя из объекта сообщения.
    await message.answer(text=LEXICON_RU['fillform'].format(id=message.from_user.id))
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя и переводить в состояние ожидания ввода возраста
@user_router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext) -> None:
    """
        Обрабатывает корректно введенное имя пользователя.

        Args:
            message (Message): Объект сообщения от пользователя.
            state (FSMContext): Объект контекста состояния пользователя.

        Returns:
            None

        Метод срабатывает, когда пользователь вводит корректное имя, состоящее только из букв. Введенное имя сохраняется
         в хранилище под ключом "name". После сохранения имени пользователю отправляется ответное сообщение, где имя
         подставляется в шаблонизированную строку. Затем устанавливается состояние ожидания ввода возраста.
    """
    # Получаем текущие данные из состояния и состояние пользователя
    logger.info(await state.get_data())
    logger.info(await state.get_state())
    # Получаем введенное пользователем имя из сообщения
    stored_name = message.text
    # Обновляем данные в хранилище, сохраняя введенное имя под ключом "name"
    await state.update_data(name=stored_name)
    # Отправляем ответное сообщение пользователю, вставляя в шаблонизированную строку введенное пользователем имя
    await message.answer(text=LEXICON_RU['fill_name'].format(name=stored_name))
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер будет срабатывать, если во время ввода имени будет введено что-то некорректное

# Этот хэндлер идет после хэндлера process_name_sent, потому что если он будет идти до, то до process_name_sent очередь
# никогда не дойдет, ведь фильтр у warning_not_name настроен только на состояние и будет забирать все апдейты в
# состоянии FSMFillForm.fill_name. А нам, все-таки в этом состоянии еще нужно ловить корректно введенное имя.
@user_router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message) -> None:
    """
        Обрабатывает случай, когда во время ввода имени пользователем введено некорректное значение.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Если введенное значение не является корректным именем, отправляет пользователю предупреждение о некорректном
        вводе, призывая ввести имя снова или отменить заполнение анкеты командой /cancel.
    """
    # Отправляем пользователю предупреждение о некорректном вводе имени, используя текст из словаря LEXICON_RU
    await message.answer(text=LEXICON_RU['warning_invalid_name'])


# Этот хэндлер будет срабатывать, если введен корректный возраст и переводить в состояние выбора пола
@user_router.message(StateFilter(FSMFillForm.fill_age), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext) -> None:
    """
        Обрабатывает корректно введенный возраст пользователя.

        Args:
            message (Message): Объект сообщения от пользователя.
            state (FSMContext): Объект контекста состояния пользователя.

        Returns:
            None

        Метод срабатывает, когда пользователь вводит корректный возраст, состоящий только из цифр, в пределах от 4 до
        120 включительно. Введенный возраст сохраняется в хранилище под ключом "age". После сохранения возраста
        пользователю отправляется ответное сообщение, в котором возраст подставляется в шаблонизированную строку. Затем
        формируется инлайн-клавиатура с кнопками для выбора пола, сообщение с клавиатурой отправляется пользователю, и
        устанавливается состояние ожидания выбора пола.
    """
    # Получаем введенный пользователем возраст из сообщения
    stored_age = message.text
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=stored_age)
    # Отправляем пользователю сообщение с запросом ввести его возраст, используя текст из словаря LEXICON_RU. Введенный
    # возраст подставляется в шаблонизированную строку.
    await message.answer(text=LEXICON_RU['fill_age'].format(age=stored_age), reply_markup=markup_gender)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста будет введено что-то некорректное
@user_router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message) -> None:
    """
        Обрабатывает случай, когда во время ввода возраста пользователем введено некорректное значение.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Если введенное значение не является корректным возрастом (целое число от 4 до 120), отправляет пользователю
        предупреждение о некорректном вводе, призывая ввести возраст снова или отменить заполнение анкеты командой
        /cancel.
    """
    # Отправляем пользователю предупреждение о некорректном вводе возраста, используя текст из словаря LEXICON_RU
    await message.answer(text=LEXICON_RU['warning_invalid_age'])


# Этот хэндлер будет срабатывать на нажатие кнопки при выборе пола и переводить в состояние отправки фото
@user_router.callback_query(StateFilter(FSMFillForm.fill_gender), F.data.in_(['male', 'female', 'undefined_gender']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Обрабатывает нажатие кнопки при выборе пола пользователем.

        Args:
            callback (CallbackQuery): Объект CallbackQuery, представляющий собой нажатие на кнопку.
            state (FSMContext): Объект контекста состояния пользователя.

        Returns:
            None

        Метод срабатывает при нажатии на кнопку выбора пола в инлайн-клавиатуре. После получения значения пола сохраняет
        его в хранилище под ключом "gender". Затем удаляет сообщение с кнопками, чтобы подготовиться к следующему этапу
        заполнения анкеты - загрузке фотографии. После этого отправляет пользователю сообщение с подтверждением
        выбранного пола и переводит бота в состояние ожидания загрузки фото.
    """
    # Получаем введенный пользователем пол из кнопки
    stored_gender = callback.data
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище, по ключу "gender"
    await state.update_data(gender=stored_gender)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото чтобы у пользователя не было желания
    # тыкать кнопки
    await callback.message.delete()
    # Отправляем пользователю сообщение с подтверждением выбранного пола, используя текст из словаря LEXICON_RU.
    # В сообщении подставляем выбранный пользователем пол, который был сохранен ранее в переменную stored_gender.
    await callback.message.answer(text=LEXICON_RU['fill_gender'].format(gender=stored_gender))
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.upload_photo)


# Этот хэндлер будет срабатывать, если во время выбора пола будет введено/отправлено что-то некорректное
@user_router.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message) -> None:
    """
        Обрабатывает случай, когда во время выбора пола пользователем введено некорректное значение.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Если введенное значение не является корректным полом, отправляет пользователю предупреждение о некорректном
        выборе, призывая выбрать пол снова или отменить заполнение анкеты командой /cancel.
    """
    # Отправляем пользователю предупреждение о некорректном выборе пола, используя текст из словаря LEXICON_RU.
    await message.answer(text=LEXICON_RU['warning_invalid_gender'])


# Этот хэндлер будет срабатывать, если отправлено фото и переводить в состояние выбора образования
@user_router.message(StateFilter(FSMFillForm.upload_photo), F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize) -> None:
    """
        Обрабатывает отправку пользователем фотографии.

        Args:
            message (Message): Объект сообщения от пользователя.
            state (FSMContext): Объект контекста состояния пользователя.
            largest_photo (PhotoSize): Объект с максимальным разрешением фотографии.

        Returns:
            None

        Метод срабатывает, когда пользователь отправляет фотографию в состоянии ожидания загрузки фото.
        Данные о фотографии сохраняются в хранилище под ключами "photo_unique_id" и "photo_id".
        Затем пользователю отправляется сообщение с предложением выбрать образование с использованием инлайн-клавиатуры.
        После этого устанавливается состояние ожидания выбора образования.
    """
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище по ключам "photo_unique_id" и "photo_id"
    await state.update_data(photo_unique_id=largest_photo.file_unique_id, photo_id=largest_photo.file_id)
    # Отправляем пользователю сообщение с предложением выбрать образование, используя текст из словаря LEXICON_RU,
    # и включаем инлайн-клавиатуру с кнопками выбора образования.
    await message.answer(text=LEXICON_RU['fill_education'], reply_markup=markup_education)
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FSMFillForm.fill_education)


# Этот хэндлер будет срабатывать, если во время отправки фото будет введено/отправлено что-то некорректное
@user_router.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message) -> None:
    """
        Обрабатывает случай, когда во время отправки фотографии пользователем введено некорректное значение.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Если введенное значение не является фотографией или произошла ошибка при загрузке фотографии, отправляет
        пользователю предупреждение о некорректной загрузке фотографии.
    """
    # Отправляем пользователю предупреждение о некорректной загрузке фотографии, используя текст из словаря LEXICON_RU.
    await message.answer(text=LEXICON_RU['warning_invalid_photo'])


# Этот хэндлер будет срабатывать, если выбрано образование и переводить в состояние согласия получать новости
@user_router.callback_query(StateFilter(FSMFillForm.fill_education), F.data.in_(['secondary', 'higher', 'no_edu']))
async def process_education_press(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Обрабатывает выбор образования пользователем.

        Args:
            callback (CallbackQuery): Объект обратного вызова от кнопки.
            state (FSMContext): Объект контекста состояния пользователя.

        Returns:
            None

        Метод получает выбранное пользователем образование и сохраняет его в хранилище под ключом "education".
        Затем редактирует предыдущее сообщение с кнопками, меняя текст и клавиатуру на новые. После этого
        устанавливает состояние ожидания выбора получения новостей.
    """
    # Получаем введенное пользователем образование из кнопки
    stored_education = callback.data
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(education=stored_education)
    # Редактируем предыдущее сообщение с кнопками, меняя текст и клавиатуру на новые.
    # Используем текст из словаря LEXICON_RU, вставляя в него выбранное образование.
    # Отправляем новую клавиатуру, чтобы пользователь мог выбрать, хочет ли он получать новости.
    await callback.message.edit_text(text=LEXICON_RU['fill_news'].format(education=stored_education),
                                     reply_markup=markup_news)
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)


# Этот хэндлер будет срабатывать, если во время выбора образования будет введено/отправлено что-то некорректное
@user_router.message(StateFilter(FSMFillForm.fill_education))
async def warning_not_education(message: Message)-> None:
    """
        Обрабатывает случай, когда во время выбора образования пользователем введено некорректное значение.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Если введенное значение не является одним из вариантов выбора образования (secondary, higher, no_edu),
        отправляет пользователю предупреждение о некорректном выборе образования.
    """
    # Отправляем пользователю предупреждение о некорректном выборе образования, используя текст из словаря LEXICON_RU
    await message.answer(text=LEXICON_RU['warning_invalid_news'])


# Этот хэндлер будет срабатывать на выбор получать или не получать новости и выводить из машины состояний
@user_router.callback_query(StateFilter(FSMFillForm.fill_wish_news), F.data.in_(['yes_news', 'no_news']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext) -> None:
    """
       Обрабатывает выбор пользователя о получении или не получении новостей.

       Args:
           callback (CallbackQuery): Объект обратного вызова.
           state (FSMContext): Объект контекста состояния пользователя.

       Returns:
           None

       Метод сохраняет выбор пользователя о получении или не получении новостей и завершает работу машины состояний.
       Данные пользователя сохраняются в базу данных. Пользователю отправляются уведомления о завершении процесса
       и предложение посмотреть анкету.
    """
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(wish_news=callback.data == 'yes_news')
    # Добавляем в "базу данных" анкету пользователя по ключу id пользователя
    user_dict[callback.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Обновляем текст сообщения, заменяя переменную wish_news значением callback.data из словаря LEXICON_RU, чтобы
    # сообщить пользователю о выборе получения или не получения новостей.
    await callback.message.edit_text(text=LEXICON_RU['fill_wish_news'].format(wish_news=callback.data))
    # Отправляем в чат сообщение с предложением посмотреть свою анкету
    await callback.message.answer(text=LEXICON_RU['view_profile'])


# Этот хэндлер будет срабатывать, если во время согласия на получение новостей будет введено/отправлено что-то
# некорректное
@user_router.message(StateFilter(FSMFillForm.fill_wish_news))
async def warning_not_wish_news(message: Message) -> None:
    """
       Обрабатывает случай, когда во время согласия на получение новостей пользователем введено некорректное значение.

       Args:
           message (Message): Объект сообщения от пользователя.

       Returns:
           None

       Если введенное значение не является корректным для согласия на получение новостей, отправляет пользователю
       предупреждение о некорректном вводе.
       """
    # Отправляем пользователю предупреждение о некорректном вводе, используя текст из словаря LEXICON_RU
    await message.answer(text=LEXICON_RU['warning_invalid_fill_wish_news'])


# Этот хэндлер будет срабатывать на отправку команды /showdata и отправлять в чат данные анкеты, либо сообщение об
# отсутствии данных
@user_router.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message) -> None:
    """
        Обрабатывает отправку команды /showdata и отправляет в чат данные анкеты, либо сообщение об отсутствии данных.

        Args:
            message (Message): Объект сообщения от пользователя.

        Returns:
            None

        Если данные пользователя присутствуют в базе данных, отправляет анкету пользователя в виде сообщения с
        фотографией и подписью. В противном случае отправляет сообщение о том, что анкета еще не заполнена.
    """
    # Выводим информацию об апдейте в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        # Если данные пользователя есть в базе данных, получаем их
        user_data = user_dict[message.from_user.id]
        # Отправляем фото пользователя с анкетой
        await message.answer_photo(
            # Используем ID фото из данных пользователя
            photo=user_data['photo_id'],
            # Форматируем подпись анкеты с данными пользователя
            caption=LEXICON_RU["showdata_available"].format(**user_data))
    else:
        # Если данных пользователя нет в базе данных, отправляем сообщение о недоступности анкеты
        await message.answer(text=LEXICON_RU["showdata_unavailable"])


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех для которых есть отдельные хэндлеры, вне состояний
@user_router.message(StateFilter(default_state))
async def send_echo(message: Message) -> None:
    """
       Отправляет эхо-ответ на любые сообщения в состоянии "по умолчанию".

       Args:
           message (Message): Объект сообщения от пользователя.

       Returns:
           None

       Отправляет пользователю стандартный текстовый ответ "Извините, моя твоя не понимать".
    """
    # Отправляем пользователю сообщение с текстом "echo", которое будет повторять текст сообщения пользователя
    await message.reply(text=LEXICON_RU["echo"])


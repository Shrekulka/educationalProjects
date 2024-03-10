# Common Message Editing Principle

## There are three main ways to replace an old message with a new one upon pressing an inline button:

Let's implement all 3 methods for better understanding.

edit_messages/lexicon/lexicon.py
```bash
# Dictionary with jokes, where the key is the joke number, and the value is the joke itself
jokes: dict[int, str] = {
    1: "joke 1",
    2: "joke 2",
    3: "joke 3",
    # Other jokes...
}
```

edit_messages/services/services.py
```bash
from random import randint
from lexicon.lexicon import jokes

# Function to generate a random number in the range from 1 to the length of the 'jokes' dictionary
def random_joke() -> int:
    return randint(1, len(jokes))
```

edit_messages/handlers/user_handlers.py
```bash
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import jokes
from services.services import random_joke

# Initialize the module-level router
user_router: Router = Router()

# This handler will be triggered by commands "/start" and "/joke"
@user_router.message(Command(commands=['start', 'joke']))
async def process_start_command(message: Message):
    # Create a keyboard with one button "More!"
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='More!', callback_data='more')]]
    # Create keyboard markup using the created keyboard
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Send the user a random joke with the "More!" button
    await message.answer(text=jokes[random_joke()], reply_markup=markup)
```

a) Via sending a new message without deleting the old one

edit_messages/handlers/user_handlers.py
```bash
# This handler will be triggered by pressing the "More!" button and send a new message without deleting the old one
@user_router.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Create a keyboard with one button "More!" and assign it to the variable 'keyboard'
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='More!', callback_data='more')]]
    # Create keyboard markup using the created keyboard
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Respond to the callback to remove the waiting clock
    await callback.answer()
    # Send a new message with a joke to the chat using a randomly selected joke and created keyboard
    await callback.message.answer(text=jokes[random_joke()], reply_markup=markup)

```

b) Via sending a new message with deleting the old one

edit_messages/handlers/user_handlers.py
```bash
# This handler will be triggered by pressing the "More!" button and send a new message to the chat, deleting the old one
@user_router.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Create a keyboard with one button "More!" and assign it to the variable 'keyboard'
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='More!', callback_data='more')]]
    # Create keyboard markup using the created keyboard
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Delete the message in which the "More!" button was pressed
    await callback.message.delete()
    # Send a new message with a joke to the chat using a randomly selected joke and created keyboard
    await callback.message.answer(text=jokes[random_joke()], reply_markup=markup)
```

с) By editing the old message and modifying the message. The most successful method.

#### Exception TelegramBadRequest (message is not modified)

In this method, when replacing the original message, you should consider the following:
The most non-obvious nuance that you often encounter at the beginning of bot development is the message in the terminal
*message is not modified*, indicating that an attempt was made to send a message to the chat that exactly duplicates
the one that needs to be edited.

If you realize during the code writing process that you may encounter such an exception, you can take one of the 
following paths:
- Compare the text you want to send with the one you want to edit. If they match, do not send a new text.
- Catch the exception with a try/except block. It makes sense if the situation potentially occurs rarely, otherwise 
  sending unmodified messages increases the load on the Telegram Bot API and will reduce the performance of your code 
  due to the relatively slow try/except construction.
- You can reliably change the message before sending it.

edit_messages/handlers/user_handlers.py
```bash
# This handler will be triggered by pressing the "More!" button and will edit the original message.
@dp.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Create a keyboard with one button "More!"
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='More!', callback_data='more')]]
    # Create keyboard markup using the created keyboard
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Get the text of the new joke by generating a random key and extracting the joke from the 'jokes' dictionary
    text = jokes[random_joke()]
    
    # Check to ensure that the text of the new joke is different from the text of the previous joke.
    # If the texts match, generate a new joke.
    while text == callback.message.text:
        text = jokes[random_joke()]
    
    # Edit the message, replacing the old joke with the new one to guarantee text difference
    await callback.message.edit_text(text=text, reply_markup=markup)
```

or we can ignore the exception using try/except

edit_messages/handlers/user_handlers.py
```bash
# This handler will trigger when the "More" button is pressed and will edit the original message.
@dp.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Create a keyboard with one button "More"
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='More', callback_data='more')]]
    # Create keyboard markup using the created keyboard
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    try:
        # Try to edit the message that was pressed
        await callback.message.edit_text(
            # Generate the text of a new joke
            text=jokes[random_joke()],
            # Add the keyboard with the "More" button
            reply_markup=markup)
    except TelegramBadRequest:
        # If a TelegramBadRequest exception occurs, it usually means that the message has already been deleted or 
        # modified, so we simply respond to the callback with an empty answer
        await callback.answer()
```
The main drawback of methods where we ignore the TelegramBadRequest exception is that the user does not receive the 
updated message. They pressed the button, but the message somehow did not change, although the hourglasses disappeared. 
Therefore, in most cases, it still makes sense to check for a match between the old and new messages before calling the 
edit_text method.

## Project Structure:
```bash
📁 formatting_text_in_messages              # Root directory of the entire project
 │
 ├── .env                                   # File with environment variables (secret data) for bot configuration.
 │
 ├── .env.example                           # File with examples of secrets for GitHub.
 │
 ├── .gitignore                             # File telling git which files and directories to ignore.
 │
 ├── bot.py                                 # Main executable file - entry point to the bot.
 │
 ├── requirements.txt                       # File with project dependencies.
 │
 ├── logger_config.py                       # Logger configuration.
 │
 ├── README.md                              # File with project description.
 │
 ├── 📁 config_data/                        # Directory with the bot configuration module.
 │   ├── __init__.py                        # Package initializer file.
 │   └── config_data.py                     # Module for bot configuration.
 │
 ├── 📁 handlers/                           # Package with handlers.
 │   ├── __init__.py                        # Package initializer file.
 │   └── user_handlers.py                   # Module with user handlers. Main update handlers for the bot.
 │                                              
 ├── 📁 keyboards/                          # Directory for storing keyboards sent to the user.
 │   ├── __init__.py                        # Package initializer file.                      
 │   └── more_button_keyboard.py            # Module with keyboards.
 │                                                 
 ├── 📁 lexicon/                            # Directory for storing bot dictionaries.      
 │   ├── __init__.py                        # Package initializer file.                      
 │   └── lexicon.py                         # File with dictionary of command and request mappings to displayed texts.
 │
 └── 📁 services/                           # Services directory containing modules for processing service functions.
     ├── __init__.py                        # Package initializer file. 
     └── services.py                        # services.py file containing functions for processing service tasks.
```




# Общий принцип редактирования сообщений

## Есть три основных способа заменить старое сообщение новым при нажатии на инлайн-кнопку:
Давайте для лучшего понимания реализуем все 3 способа.

edit_messages/lexicon/lexicon.py
```bash
# Словарь с шутками, где ключ - номер шутки, а значение - сама шутка
jokes: dict[int, str] = {
    1: "Шутка 1",
    2: "Шутка 2",
    3: "Шутка 3",
    # и остальные шутки ...
}
```

edit_messages/services/services.py
```bash
from random import randint
from lexicon.lexicon import jokes

# Функция, генерирующая случайное число в диапазоне от 1 до длины словаря jokes
def random_joke() -> int:
    return random.randint(1, len(jokes))
```

edit_messages/handlers/user_handlers.py
```bash
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import jokes
from services.services import random_joke

# Инициализируем роутер уровня модуля
user_router: Router = Router()
# Этот хэндлер будет срабатывать на команды "/start" и "/joke"
@dp.message(Command(commands=['start', 'joke']))
async def process_start_command(message: Message):
    # Создаем клавиатуру с одной кнопкой "Хочу еще!"
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='Хочу еще!', callback_data='more')]]
    # Создаем разметку клавиатуры, используя созданную клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю случайную шутку с кнопкой "Хочу еще!"
    await message.answer(text=jokes[random_joke()], reply_markup=markup)
```

a) Через отправку нового сообщения без удаления старого

edit_messages/handlers/user_handlers.py
```bash
# Этот хэндлер будет срабатывать на нажатие кнопки "Хочу еще!" и отправлять в чат новое сообщение, не удаляя старое
@user_router.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Создаем клавиатуру с одной кнопкой "Хочу еще!" и присваиваем ее переменной keyboard
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='Хочу еще!', callback_data='more')]]
    # Создаем разметку клавиатуры, используя созданную клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отвечаем на callback, чтобы убрать часики ожидания ответа
    await callback.answer()
    # Отправляем в чат новое сообщение с шуткой, используя случайно выбранную шутку и созданную клавиатуру
    await callback.message.answer(text=jokes[random_joke()], reply_markup=markup)
```

b) Через отправку нового сообщения с удалением старого

edit_messages/handlers/user_handlers.py
```bash
# Этот хэндлер будет срабатывать на нажатие кнопки "Хочу еще!" и отправлять в чат новое сообщение, удаляя старое
@user_router.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Создаем клавиатуру с одной кнопкой "Хочу еще!" и присваиваем ее переменной keyboard
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='Хочу еще!', callback_data='more')]]
    # Создаем разметку клавиатуры, используя созданную клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Удаляем сообщение, в котором была нажата кнопка "Хочу еще!"
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой, используя случайно выбранную шутку и созданную клавиатуру
    await callback.message.answer(text=jokes[random_joke()], reply_markup=markup)
```
с) Через редактирование старого сообщения и изменять сообщение. Самый удачный способ.

##### Исключение TelegramBadRequest (message is not modified)
В этом способе при замене исходного сообщения надо учитывать следующее:
Самый неочевидный нюанс, с которым часто сталкиваешься в начале пути разработки ботов - это сообщение в терминале 
*message is not modified*, сообщающее о том, что была попытка отправить в чат сообщение, которое в точности повторяет 
то, которое нужно отредактировать.
Если вы, в процессе написания кода, понимаете, что можете столкнуться с таким исключением, то можете пойти по одному из 
следующих путей:
- Сравнивать текст, который вы хотите отправить с тем, который вы хотите отредактировать. Если они совпадают, то не 
  отправлять новый текст.
- Перехватывать исключение конструкцией try/except. Имеет смысл, если ситуация потенциально может возникать достаточно 
  редко, а иначе отправка немодифицированных сообщений увеличивает нагрузку на Telegram Bot API и будет снижать 
  производительность вашего кода из-за относительно медленно работающей конструкции try/except.
- Можно гарантированно менять сообщение перед отправкой.

edit_messages/handlers/user_handlers.py
```bash
# Этот хэндлер будет срабатывать на нажатие кнопки "Хочу еще!" и будет редактировать исходное сообщение.
@dp.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Создаем клавиатуру с одной кнопкой "Хочу еще!"
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='Хочу еще!', callback_data='more')]]
    # Создаем разметку клавиатуры, используя созданную клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Получаем текст новой шутки, генерируя случайный ключ и извлекая шутку из словаря jokes
    text = jokes[random_joke()]
    
    # Проверяем, чтобы текст новой шутки отличался от текста предыдущей шутки.
    # Если тексты совпадают, генерируем новую шутку.
    while text == callback.message.text:
        text = jokes[random_joke()]
    
    # Редактируем сообщение, заменяя старую шутку на новую, чтобы гарантировать различие текста
    await callback.message.edit_text(text=text, reply_markup=markup)
```
либо будем игнорировать исключение с помощью try/except

edit_messages/handlers/user_handlers.py
```bash
# Этот хэндлер будет срабатывать на нажатие кнопки "Хочу еще!" и будет редактировать исходное сообщение.
@dp.callback_query(F.data == 'more')
async def process_more_press(callback: CallbackQuery):
    # Создаем клавиатуру с одной кнопкой "Хочу еще!"
    keyboard: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text='Хочу еще!', callback_data='more')]]
    # Создаем разметку клавиатуры, используя созданную клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    try:
        # Пытаемся отредактировать сообщение, на которое нажали
        await callback.message.edit_text(
            # Генерируем новый текст шутки
            text=jokes[random_joke()],
            # Добавляем клавиатуру с кнопкой "Хочу еще!"
            reply_markup=markup)
    except TelegramBadRequest:
        # Если возникает исключение TelegramBadRequest, это обычно означает, что сообщение уже удалено или изменено,
        # поэтому мы просто отвечаем на коллбэк пустым ответом
        await callback.answer()
```
Основной недостаток методов, при которых мы игнорируем исключение TelegramBadRequest, состоит в том, что пользователь не
получает обновленного сообщения. На кнопку, вроде, нажал, но сообщение почему-то не поменялось, хотя и часики, вроде 
пропали. Поэтому, в большинстве случаев, имеет смысл все-таки проверять на совпадение старого и нового сообщения перед 
вызовом метода edit_text.

## Структура проекта:
```bash
📁 formatting_text_in_messages              # Корневая директория всего проекта
 │
 ├── .env                                   # Файл с переменными окружения (секретными данными) для конфигурации бота.
 │
 ├── .env.example                           # Файл с примерами секретов для GitHub
 │
 ├── .gitignore                             # Файл, сообщающий гиту какие файлы и директории не отслеживать
 │
 ├── bot.py                                 # Основной исполняемый файл - точка входа в бот
 │
 ├── requirements.txt                       # Файл с зависимостями проекта.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта.
 │
 ├── 📁 config_data/                        # Директория с модулем конфигурации бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета. 
 │   └── config_data.py                     # Модуль для конфигурации бота.
 │
 ├── 📁 handlers/                           # Пакет с обработчиками.
 │   ├── __init__.py                        # Файл-инициализатор пакета.
 │   └── user_handlers.py                   # Модуль с обработчиками пользователя. Основные обработчики обновлений бота.
 │                                              
 ├── 📁 keyboards/                          # Директория для хранения клавиатур отправляемые пользователю.
 │   ├── __init__.py                        # Файл-инициализатор пакета.                      
 │   └── more_button_keyboard.py            # Модуль с клавиатурами.
 │                                                 
 ├── 📁 lexicon/                            # Директория для хранения словарей бота.      
 │   ├── __init__.py                        # Файл-инициализатор пакета.                      
 │   └── lexicon.py                         # Файл со словарем соответствий команд и запросов отображаемым текстам.
 │
 └── 📁 services/                           # Директория services, содержащая модули для обработки сервисных функций.
     ├── __init__.py                        # Файл-инициализатор пакета. 
     └── services.py                        # Файл services.py, содержащий функции для обработки сервисных задач.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
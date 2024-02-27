# The "own_keyboard_generator" project is a Telegram bot that generates and sends inline keyboards to the user in 
# response to the "/start" command. Keyboards are created using the **create_inline_kb** function from the 
# keyboard_generator_function module.

1. **keyboard_generator_function.py**: This module contains the **create_inline_kb** function, which generates an inline 
   keyboard based on the provided arguments. The function takes the width of the keyboard (number of buttons in a row), 
   arguments for creating buttons, the text of the last button (default is not set), and named arguments for creating 
   additional buttons. It utilizes the lexicon from the lexicon.lexicon_ru module to localize button texts into Russian.

2. **user_handlers.py**: This module contains handlers for the "/start" command and sending messages with generated 
   keyboards.

3. **lexicon_ru.py**: This module contains the LEXICON and BUTTONS dictionaries, which store lexicons in Russian for 
   project text elements and labels with corresponding text values for buttons, respectively.


### Project Structure:
```bash
 📁 own_keyboard_generator/                       # Project directory, the main bot file.
 │
 ├── .env                                          # File with configuration and secrets.
 │
 ├── .env.example                                  # File with examples of secrets for GitHub.
 │
 ├── .gitignore                                    # File telling Git which files and directories not to track.
 │
 ├── bot.py                                        # Main executable file - entry point into the bot.
 │
 ├── requirements.txt                              # File with project dependencies.
 │
 ├── logger_config.py                              # Logger configuration.
 │
 ├── README.md                                     # File with project description.
 │
 ├── 📁 config_data/                               # Directory with the bot configuration module.
 │   ├── __init__.py                               # Package initializer file. 
 │   └── config_data.py                            # Module for bot configuration.
 │ 
 ├── 📁 handlers/                                  # Directory with handlers.
 │   ├── __init__.py                               # Package initializer file.
 │   └── user_handlers.py                          # Module with handlers for user updates.
 │
 ├── 📁 keyboards/                                 # Directory to store keyboards sent to users.
 │   ├── __init__.py                               # Package initializer file.                      
 │   └── keyboard_generator_function.py            # Module containing a function to generate inline keyboards.
 │ 
 └── 📁 lexicon/                                   # Directory to store bot dictionaries.
     ├── __init__.py                               # Package initializer file.            
     └── lexicon_ru.py                             # Module with a dictionary of command mappings and displayed texts.
```
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Проект "own_keyboard_generator" представляет собой Telegram-бота, который генерирует и отправляет пользователю 
# инлайн-клавиатуры в ответ на команду "/start". Клавиатуры создаются с помощью функции **create_inline_kb** из модуля 
# keyboard_generator_function.

1. **keyboard_generator_function.py**: Этот модуль содержит функцию **create_inline_kb**, которая генерирует 
   инлайн-клавиатуру на основе предоставленных аргументов. Функция принимает ширину клавиатуры (количество кнопок в 
   строке), аргументы для создания кнопок, текст последней кнопки (по умолчанию не задан), а также именованные аргументы
   для создания дополнительных кнопок. Она использует лексикон из модуля lexicon.lexicon_ru для локализации текстов 
   кнопок на русский язык.

2. **user_handlers.py**: Этот модуль содержит обработчики для команды "/start" и отправки сообщений с сгенерированными 
   клавиатурами.

3. **lexicon_ru.py**: Этот модуль содержит словари LEXICON и BUTTONS, которые хранят лексикон на русском языке для 
   текстовых элементов проекта и метки с соответствующими текстовыми значениями для кнопок, соответственно.


### Структура проекта:
```bash
 📁 improved_echo_bot/                             # Директория проекта, основной файл бота.
 │
 ├── .env                                          # Файл с конфигурацией и секретами.
 │
 ├── .env.example                                  # Файл с примерами секретов для GitHub
 │
 ├── .gitignore                                    # Файл, сообщающий гиту какие файлы и директории не отслеживать
 │
 ├── bot.py                                        # Основной исполняемый файл - точка входа в бот
 │
 ├── requirements.txt                              # Файл с зависимостями проекта.
 │
 ├── logger_config.py                              # Конфигурация логгера.
 │
 ├── README.md                                     # Файл с описанием проекта.
 │
 ├── 📁 config_data/                               # Директория с модулем конфигурации бота.
 │   ├── __init__.py                               # Файл-инициализатор пакета. 
 │   └── config_data.py                            # Модуль для конфигурации бота.
 │ 
 ├── 📁 handlers/                                  # Директория с хэндлерами.
 │   ├── __init__.py                               # Файл-инициализатор пакета.
 │   └── user_handlers.py                          # Модуль с обработчиками апдейтов от пользователя.
 │                                              
 ├── 📁 keyboards/                                 # Директория для хранения клавиатур отправляемые пользователю.
 │   ├── __init__.py                               # Файл-инициализатор пакета.                      
 │   └── keyboard_generator_function.py            # Модуль содержит функцию для генерации инлайн-клавиатуры
 │ 
 └── 📁 lexicon/                                   # Директория для хранения словарей бота.
     ├── __init__.py                               # Файл-инициализатор пакета.            
     └── lexicon_ru.py                             # Модуль со словарем соответствий команд и отображаемых текстов.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
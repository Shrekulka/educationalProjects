# The set_my_commands method adds the necessary commands that will be shown when the Menu button is pressed.

Telegram bot providing a main menu with various commands for users and the ability to remove/restore the 'Menu' button.

## Project Description:

#### Project Purpose:
This project is created to provide Telegram users with a bot that offers a main menu with commands for getting help, 
support, contact information, and payment information.

#### Bot Commands:
/help: Command to get help about the bot's functionality.
/support: Command to get support.
/contacts: Command to display additional contact methods.
/payments: Command to get payment information.

#### Interactive Interaction:
Users can manually type "/" and enter the command name (e.g., /help), or they can click on the menu button corresponding
to the desired command (e.g., the "Help" button for the /help command). This provides a convenient way to interact with 
the bot.

To remove the main menu, the /delmenu command is provided. To restore it, use /restore_menu.

#### Project Structure:
 ```bash
 📁 telegram_bot_menu_button/                      # Project directory, main bot file.
 │
 ├── .env                                          # Configuration and secrets file.
 │
 ├── .env.example                                  # File with secret examples for GitHub
 │
 ├── .gitignore                                    # File telling git which files and directories to ignore
 │
 ├── bot.py                                        # Main executable file - entry point for the bot
 │
 ├── requirements.txt                              # File with project dependencies.
 │
 ├── logger_config.py                              # Logger configuration.
 │
 ├── README.md                                     # Project description file.
 │
 ├── 📁 config_data/                               # Directory with bot configuration module.
 │    ├── __init__.py                               # Package initializer file. 
 │    └── config_data.py                            # Module for bot configuration.
 │ 
 ├── 📁 handlers/                                  # Directory with handlers.
 │   ├── __init__.py                               # Package initializer file.
 │   └── other_handlers.py                         # File with handler for /delmenu, /restore_menu commands
 │                                                 
 ├── 📁 keyboards/                                 # Directory with keyboards and bot menu
 │   ├── __init__.py                               # Package initializer file.                      
 │   └── set_menu.py                               # File with function to set up the bot's main menu
 │ 
 ├── 📁 lexicon/                                   # Directory to store bot dictionaries.
 │   ├── __init__.py                               # Package initializer file.                      
 │   └── lexicon_ru.py                             # Module with a dictionary of command mappings and displayed texts.
 ```
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Метод set_my_commands добавляет нужные нам команды, которые будут показаны при нажатии на кнопку Menu

Telegram бот, который предоставляет главное меню с различными командами для пользователей и удаление/восстановление 
кнопки 'Меню'. 

## Описание проекта:

#### Назначение проекта:
Этот проект создан для обеспечения пользователей Telegram ботом, который предоставляет главное меню с командами для 
получения справки, поддержки, контактной информации и информации о платежах.

#### Команды бота:
/help: Команда для получения справки по работе бота.
/support: Команда для получения поддержки.
/contacts: Команда для отображения дополнительных способов связи.
/payments: Команда для получения информации о платежах.

#### Интерактивное взаимодействие: 
Пользователи могут как вручную прописать "/" и ввести название команды (например, /help), так и нажать на кнопку меню, 
соответствующую желаемой команде (например, кнопку "Справка" для команды /help). Таким образом, предоставляется удобный 
способ взаимодействия с ботом.

Для удаления главного меню предусмотрена команда /delmenu. Для его восстановления - /restore_menu.

#### Структура проекта:
 ```bash
 📁 telegram_bot_menu_button/                      # Директория проекта, основной файл бота.
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
 ├──  📁 config_data/                               # Директория с модулем конфигурации бота.
 │    ├── __init__.py                               # Файл-инициализатор пакета. 
 │    └── config_data.py                            # Модуль для конфигурации бота.
 │ 
 ├── 📁 handlers/                                  # Директория с хэндлерами.
 │   ├── __init__.py                               # Файл-инициализатор пакета.
 │   └── other_handlers.py                         # Файл с обработчиком команды /delmenu, /restore_menu
 │                                                 
 ├── 📁 keyboards/                                 # Директория с клавиатурами и меню бота
 │   ├── __init__.py                               # Файл-инициализатор пакета.                      
 │   └── set_menu.py                               # Файл с функцией настройки главного меню бота
 │ 
 ├── 📁 lexicon/                                   # Директория для хранения словарей бота.
 │   ├── __init__.py                               # Файл-инициализатор пакета.                      
 │   └── lexicon_ru.py                             # Модуль со словарем соответствий команд и отображаемых текстов.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
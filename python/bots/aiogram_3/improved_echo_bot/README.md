# This is an echo bot for Telegram utilizing the aiogram library.

## More about the main components:
1. logger_config.py:
    - Implements a custom logger CustomLogger with various methods for logging.
    - Utilizes the Colorama library for colorizing logs.
    - Configures multiple formatters with colored highlighting for different log levels.
    - Adds handlers for logging to both files and the console.
2. config_data/config.py:
    - Loads bot configuration data from environment variables (.env).
    - Utilizes the Environs library for handling environment variables.
    - Stores tokens and other sensitive data.
3. handlers:
    - Implements the main logic for handling updates.
    - Utilizes aiogram routers instead of handling directly.
    - Separates user handlers from other handlers.
4. lexicon/lexicon.py:
    - Simple dictionary for storing bot response texts to avoid code duplication.
5. bot.py:
    - Launches and configures the application.
    - Registers routers in the dispatcher.
    - Handles errors during startup.

### Additionally, other best practices are employed:
- requirements.txt file for dependencies.
- gitignore to exclude unnecessary files from the repository.
- Example .env file for environment setup.

6. Project Structure:
    ```bash
    📁 improved_echo_bot/                            # Project directory, main bot file.
    │
    ├── .env                                          # Configuration and secrets file.
    │
    ├── .env.example                                  # Example .env file for other developers.
    │
    ├── .gitignore                                    # File for version control system to ignore specified files.
    │
    ├── bot.py                                        # Main project file, entry point.
    │
    ├── requirements.txt                              # Project dependencies file.
    │
    ├── logger_config.py                              # Logger configuration.
    │
    ├── README.md                                     # Project description file.
    │
    ├── 📁 config_data/                               # Package with configuration data.
    │   ├── __init__.py                               # File indicating that the directory is a Python package.
    │   └── config.py                                 # Module with configuration data.
    │ 
    ├── 📁 handlers/                                  # Package with update handlers.
    │   ├── __init__.py                               # File indicating that the directory is a Python package.
    │   ├── user_handlers.py                          # Module with update handlers from the user with bot logic.
    │   └── other_handlers.py                         # Module to store handler that will process messages.
    │ 
    └── 📁 lexicon/                                   # Package for storing bot lexicons.
        ├── __init__.py                               # File indicating that the directory is a Python package.
        └── lexicon.py                                # Module with a dictionary of command mappings and displayed texts.
    ```
Educational material on Stepik - https://stepik.org/course/120924/syllabus




# Это echo-бот для Telegram, использующий библиотеку aiogram.

## Подробнее про основные компоненты:
1. logger_config.py:
    - реализует кастомный логгер CustomLogger с различными методами для логирования
    - использует библиотеку Colorama для подсветки логов цветом
    - настраивает несколько форматтеров с цветным выделением для разных уровней логов
    - добавляет обработчики для логирования в файл и в консоль
2. config_data/config.py:
    - загружает данные о конфигурации бота из переменных окружения (.env)
    - использует библиотеку Environs для работы с переменными окружения
    - хранит токен и другие секретные данные
3. handlers:
    - реализуют основную логику обработки апдейтов
    - используют роутеры aiogram вместо хендлеров напрямую
    - отдельно вынесены хендлеры от пользователя и все остальные
4. lexicon/lexicon.py:
    - простой словарь для хранения текстов ответов бота чтобы не дублировать тексты по коду
5. bot.py:
    - запускает и конфигурирует приложение
    - регистрирует роутеры в диспетчере
    - обрабатывает ошибки при запуске
   
### Также используются другие best practices:
    - файл требований requirements.txt
    - gitignore для исключения ненужных файлов из репозитория
    - пример файла окружения .env.example

6. Структура проекта:
    ```bash
    📁 improved_echo_bot/                            # Директория проекта, основной файл бота.
    │
    ├── .env                                          # Файл с конфигурацией и секретами.
    │
    ├── .env.example                                  # Пример файла .env для других разработчиков.
    │
    ├── .gitignore                                    # Файл для игнорирования файлов системой контроля версий.
    │
    ├── bot.py                                        # Основной файл проекта, точка входа.
    │
    ├── requirements.txt                              # Файл с зависимостями проекта.
    │
    ├── logger_config.py                              # Конфигурация логгера.
    │
    ├── README.md                                     # Файл с описанием проекта.
    │
    ├── 📁 config_data/                               # Пакет с конфигурационными данными.
    │   ├── __init__.py                               # Файл, обозначающий, что директория является пакетом Python.
    │   └── config.py                                 # Модуль с конфигурационными данными.
    │ 
    ├── 📁 handlers/                                  # Пакет с обработчиками апдейтов.
    │   ├── __init__.py                               # Файл, обозначающий, что директория является пакетом Python.
    │   ├── user_handlers.py                          # Модуль с обработчиками апдейтов от пользователя с логикой бота
    │   └── other_handlers.py                         # Модуль для хранения хэндлера, который будет обрабатывать сообщения
    │ 
    └── 📁 lexicon/                                   # Пакет для хранения словарей бота
        ├── __init__.py                               # Файл, обозначающий, что директория является пакетом Python.
        └── lexicon.py                                # Модуль со словарем соответствий команд и отображаемых текстов
    ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
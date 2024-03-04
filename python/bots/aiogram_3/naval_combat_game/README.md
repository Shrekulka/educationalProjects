# Truncated Naval Combat - Telegram Bot

## Game Description

The game is implemented using an inline keyboard with an 8x8 grid.

### Each cell on the grid can be in one of three states:
0 - empty cell (no shot has been taken)
1 - miss (denoted by "🔵")
2 - sunk ship (denoted by "💥")

### There are 9 ships on the grid:
2 three-deckers
3 two-deckers
4 one-deckers

### Before the game starts, the ships are randomly placed for each player using the generate_ships() function, ensuring:
- Ships do not overlap
- Ships do not touch diagonally
- 
After initialization, each player receives a message with the game grid and a keyboard for making moves. The game 
continues until one player sinks all the opponent's ships. Upon completion, a message indicating the winning player is 
displayed.

### Data Storage
Data about the state of each cell for the user is stored in users[user_id]['field'] as an 8x8 matrix of numbers:
0 - cell not revealed (no shot taken)
1 - miss
2 - ship sunk

### Data about ship placement is stored in users[user_id]['ships']:
0 - no ship
1 - ship present

### Main Functions
- generate_ships(): Generates a random ship placement on the grid.
- get_field_keyboard(): Forms an inline keyboard to display the grid.
- reset_field(): Resets the user's game grid.

### Request Handlers
- process_start_command(): Initializes the game for the user.
- process_category_press(): Handles button presses on the grid.

Thus, the bot generates the grid and ships for each player, allows them to make moves, tracks the grid's state, and 
determines the winner.

## Project Structure:
```bash
📁 naval_combat_game                        # Root directory of the project
 │
 ├── .env                                   # Environment variables file for bot configuration (contains secret data).
 │
 ├── .env.example                           # Example secrets file for GitHub
 │
 ├── .gitignore                             # File informing Git about files and directories to ignore
 │
 ├── game_bot.py                            # Main executable file - entry point of the bot
 │
 ├── requirements.txt                       # File with project dependencies
 │
 ├── logger_config.py                       # Logger configuration
 │
 ├── README.md                              # Project description file
 │
 ├── 📁 config_data/                        # Directory with bot configuration module
 │   ├── __init__.py                        # Package initializer file
 │   └── game_config_data.py                # Module for bot configuration
 │
 ├── 📁 database/                           # Package for database operations
 │   ├── __init__.py                        # Package initializer file
 │   └── game_database.py                   # Module with database template
 │
 ├── 📁 filters/                            # Package with user-defined filters
 │   ├── __init__.py                        # Package initializer file
 │   └── game_filters.py                    # Module with filters written for specific bot tasks
 │ 
 ├── 📁 handlers/                           # Package with request handlers
 │   ├── __init__.py                        # Package initializer file
 │   └── user_handlers.py                   # Module with user handlers, primary update handlers of the bot
 │                                                 
 ├── 📁 keyboards/                          # Package with bot keyboards
 │   ├── __init__.py                        # Package initializer file            
 │   └── game_keyboard.py                   # Module with keyboards for the bot   
 │ 
 ├── 📁 lexicon/                            # Directory for storing bot lexicons      
 │   ├── __init__.py                        # Package initializer file                      
 │   └── game_lexicon.py                    # Module for storing bot lexicons
 │ 
 ├── 📁 models/                             # Directory with data models for the bot
 │   ├── __init__.py                        # Package initializer file                      
 │   └── game_models.py                     # Module with models for the bot
 │ 
 └── 📁 services/                           # Directory for auxiliary tools     
     ├── __init__.py                        # Package initializer file                       
     └── game_services.py                   # Module with service functions for the bot  
```




# Усеченный морской бой - телеграм-бот

## Описание игры
Игра реализована с использованием инлайн-клавиатуры размером 8х8 клеток.

### Каждая клетка на поле может находиться в одном из трех состояний:
0 - пустая клетка (выстрела еще не было)
1 - промах (обозначается символом "🔵")
2 - потопленный корабль (обозначается символом "💥")
### На поле располагается 9 кораблей:
- 2 трехпалубных
- 3 двухпалубных
- 4 однопалубных

### Перед началом игры для каждого игрока генерируется случайная расстановка кораблей функцией generate_ships() с 
### соблюдением правил их размещения:
- Корабли не могут перекрываться
- Корабли не могут соприкасаться по диагонали

После инициализации каждому игроку отправляется сообщение с игровым полем и клавиатурой для совершения ходов.
Игра продолжается до тех пор, пока один из игроков не потопит все корабли противника. При завершении игры выводится 
сообщение о победе игрока.

### Хранение данных
Данные о состоянии каждой клетки поля для пользователя хранятся в users[user_id]['field'] в виде матрицы 8х8 из чисел:
0 - клетка не открыта (выстрела не было)
1 - промах
2 - потоплен корабль

### Данные о расположении кораблей хранятся в users[user_id]['ships']:
0 - нет корабля
1 - есть корабль

### Основные функции
- generate_ships() - генерирует случайную расстановку кораблей на поле.
- get_field_keyboard() - формирует инлайн-клавиатуру для отображения поля.
- reset_field() - сбрасывает игровое поле пользователя.

### Обработчики запросов
- process_start_command() - инициализирует игру для пользователя.
- process_category_press() - обрабатывает нажатия на кнопки поля.

Таким образом, бот генерирует поле и корабли для каждого игрока, позволяет им совершать ходы, отслеживает состояние 
поля и определяет победителя.


## Структура проекта:
```bash
📁 naval_combat_game                        # Корневая директория всего проекта
 │
 ├── .env                                   # Файл с переменными окружения (секретными данными) для конфигурации бота.
 │
 ├── .env.example                           # Файл с примерами секретов для GitHub
 │
 ├── .gitignore                             # Файл, сообщающий гиту какие файлы и директории не отслеживать
 │
 ├── game_bot.py                            # Основной исполняемый файл - точка входа в бот
 │
 ├── requirements.txt                       # Файл с зависимостями проекта.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта.
 │
 ├── 📁 config_data/                        # Директория с модулем конфигурации бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета. 
 │   └── game_config_data.py                # Модуль для конфигурации бота.
 │
 ├── 📁 database/                           # Пакет для работы с базой данных.
 │   ├── __init__.py                        # Файл-инициализатор пакета.     
 │   └── game_database.py                   # Модуль с шаблоном базы данных.
 │
 ├── 📁 filters/                            # Пакет с пользовательскими фильтрами.
 │   ├── __init__.py                        # Файл-инициализатор пакета.      
 │   └── game_filters.py                    # Модуль с фильтрами, которые мы напишем для конкретных задач бота.
 │ 
 ├── 📁 handlers/                           # Пакет с обработчиками.
 │   ├── __init__.py                        # Файл-инициализатор пакета.
 │   └── user_handlers.py                   # Модуль с обработчиками пользователя. Основные обработчики обновлений бота.
 │                                                 
 ├── 📁 keyboards/                          # Пакет с клавиатурами бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета.            
 │   └── game_keyboard.py                   # Модуль с клавиатурами для бота.   
 │ 
 ├── 📁 lexicon/                            # Директория для хранения словарей бота.      
 │   ├── __init__.py                        # Файл-инициализатор пакета.                      
 │   └── game_lexicon.py                    # Модуль для хранения словарей бота.
 │ 
 ├── 📁 models/                             # Директория с моделями данных для бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета.                      
 │   └── game_models.py                     # Модуль с моделями для бота.
 │ 
 └── 📁 services/                           # Директория для вспомогательных инструментов.     
     ├── __init__.py                        # Файл-инициализатор пакета.                       
     └── game_services.py                   # Модуль с сервисными функциями для бота.  
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
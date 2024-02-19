# Project Description for the "Rock, Paper, Scissors" Bot in Python:

1. In config_data/config_data.py, a Settings class is defined, inherited from BaseModel from the pydantic library, to 
   store the bot's configuration data - the access token for the Telegram API. Also, a nested Config class is defined 
   for setting the loading of environment variables from the .env file. An instance of the config class Settings is 
   created to access this data.
2. In handlers/, handlers for incoming user requests are defined:
   - user_handlers - handling commands /start, /help, responses "Yes" and "No" to play, choosing "Rock", "Scissors", or
     "Paper".
   - other_handlers - handling unexpected messages.
3. The aiogram library is used to handle requests - routers are created and event handlers are connected to it.
4. In keyboards/, keyboards for interacting with the bot are defined - yes_no_kb and game_kb.
5. Texts in Russian for bot responses are stored in lexicon/lexicon_ru.
6. The logic of the game is implemented in services/:
   - game_state - variables for storing the score and a function to reset the score
   - services - functions for choosing a random option by the bot, determining the winner, and updating the score
7. Event logging is implemented in the bot (logger_config.py).
8. The main bot module bot.py initializes and starts the bot - registers request handlers, configures requests to the 
   Telegram API.

# Bot "Rock, Paper, Scissors"
A very simple bot with which you can play the game "Rock, Paper, Scissors". This game is most commonly played between 
two people. Players simultaneously, on the count of three, show a hand signal representing one of three possible moves:
rock (a fist), paper (an open hand), or scissors (a fist with the index and middle fingers extended). If the players 
choose the same shape, the game is tied. In all other cases, the winner is determined by the rules: paper beats rock, 
rock beats scissors, and scissors beat paper.

The bot will be multiplayer, and no user states need to be stored. When a user sends a message with their choice, the 
bot will generate a random response, and a message with the result - who won - will be sent to the chat.

### Project Task Statement
#### What?
Telegram bot to play the game "Rock, Paper, Scissors"

#### Why?
To demonstrate the use of regular buttons and project templates, as well as to have the ability to play a simple game 
with the bot.

#### What should the bot do?
Send the user a keyboard with regular choice buttons: rock, scissors, paper
Generate a random element in the game from the list "rock, scissors, paper"
Handle the user's choice and report who won

#### Additional Features
Not provided

#### Interaction Description with the Bot
1. The user sends the command /start to the bot (or starts it by finding it in the search)
2. The bot greets the user and suggests playing the game "Rock, Paper, Scissors" by sending a keyboard with answers
   "Let's go!" and "Don't want!", and also offers the user to read the detailed rules by sending the command /help
3. At this stage, the user can perform 4 actions:
    - Agree to play with the bot in the game by clicking on the regular button "Let's go!"
    - Refuse to play with the bot by clicking on the regular button "Don't want!"
    - Send the command /help to the chat
    - Send any other message to the chat
4. The user clicks on the regular button "Let's go!":
    a) The bot sends the message "Great! Make your choice!" to the chat
    b) The bot sends a keyboard with choice buttons "Rock", "Scissors", and "Paper" to the chat
    c) At this stage, the user can perform 3 actions:
     - Click on one of the choice buttons ("Rock", "Scissors", or "Paper")
     - Send the command /help to the chat
     - Send any other message to the chat
    d) The user clicks on one of the choice buttons ("Rock", "Scissors", or "Paper"):
     - The bot generates a random response from the same list
     - The bot checks who won
     - The bot informs the user who won
     - The bot sends the user an offer to play again and a keyboard for selection with buttons "Let's go!" and "Don't 
       want!"
5. The user clicks on the "Don't want!" button:
    - The keyboard collapses
    - The bot sends the message "Okay. If you suddenly want to play - open the keyboard and click "Let's go!"
6. The user sends the command /help to the chat:
    - The bot sends the rules of the game, an offer to play, and a keyboard with buttons "Let's go!" and "Don't want!" 
      to the chat
7. The user sends any other message to the chat:
    - The bot sends a message to the chat that it doesn't understand the user

Project Structure:
 ```bash
 📁 improved_echo_bot/                             # Project directory, main bot file.
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
 │   ├── __init__.py                               # Package initializer file. 
 │   └── config_data.py                            # Module for bot configuration.
 │ 
 ├── 📁 handlers/                                  # Directory with handlers.
 │   ├── __init__.py                               # Package initializer file.
 │   ├── user_handlers.py                          # Module with update handlers from the user
 │   └── other_handlers.py                         # Module for storing a handler that will handle messages 
 │                                                 # not covered in the user's interaction with the bot.
 ├── 📁 keyboards/                                 # Directory for storing keyboards sent to the user.
 │   ├── __init__.py                               # Package initializer file.                      
 │   └── keyboards.py                              # Module with keyboards.
 │ 
 ├── 📁 lexicon/                                   # Directory for storing bot dictionaries.
 │   ├── __init__.py                               # Package initializer file.                      
 │   └── lexicon_ru.py                             # Module with a dictionary of command mappings and displayed texts.
 │ 
 └── 📁 services/                                  # Directory for storing bot business logic. 
     ├── __init__.py                               # Package initializer file.
     ├── services.py                               # Module with business logic.                             
     └── game_state.py                             # Module for counting and resetting scores
```
Educational material on Stepik - https://stepik.org/course/120924/syllabus



# Подробное описание проекта бота для игры "Камень, ножницы, бумага" на python:

1. В config_data/config_data.py определен класс Settings, наследуемый от BaseModel из библиотеки pydantic, для хранения
   конфигурационных данных бота - токена доступа к API Telegram. Также определен вложенный класс Config для настройки 
   загрузки переменных окружения из файла .env. Создан экземпляр config класса Settings для доступа к этим данным.
2. В handlers/ определены обработчики входящих запросов пользователя:
   - user_handlers - обработка команд /start, /help, ответов "Да" и "Нет" на предложение сыграть, выбора варианта 
     "Камень", "Ножницы" или "Бумага".
   - other_handlers - обработка непредвиденных сообщений.
3. Для обработки запросов используется библиотека aiogram - создаются router и подключаются к нему обработчики событий.
4. В keyboards/ определены клавиатуры для взаимодействия с ботом - yes_no_kb и game_kb.
5. В lexicon/lexicon_ru хранятся тексты на русском языке для ответов бота.
6. В services/ реализована логика игры:
   - game_state - переменные для хранения счета и функция сброса счета
   - services - функции выбора случайного варианта ботом, определения победителя, изменения счета
7. В боте используется логирование событий (logger_config.py).
8. Главный модуль бота bot.py инициализирует и запускает бота - регистрирует обработчики запросов, настраивает запросы 
   к API Telegram.

# Бот "Камень, ножницы, бумага"
Очень простой бот, с которым можно играть в игру "Камень, ножницы, бумага". Чаще всего в игру играют вдвоем. Игроки 
одновременно, на счет три, показывают рукой какую-нибудь фигуру из трех возможных: камень (кулак), ножницы 
(разъединенные указательный и средний пальцы), бумагу (ладонь). Если фигуры одинаковые - ничья. В остальных случаях - 
бумага побеждает камень, камень побеждает ножницы, а ножницы побеждают бумагу.

Бот будет многопользовательским, причем, никаких состояний пользователей хранить не нужно. В момент, когда пользователь 
отправит сообщение со своим выбором, будет сгенерирован случайный ответ бота и в чат отправлено сообщение с результатом 
- кто победил.

### Постановка задачи
#### Что?
Телеграм-бот, с которым можно играть в игру "Камень, ножницы, бумага"

#### Чтобы что?
Чтобы на примере продемонстрировать работу с обычными кнопками и шаблоном проекта, а также иметь возможность играть с ботом в простую игру.

#### Что бот должен уметь?
Отправлять пользователю клавиатуру с обычными кнопками выбора: камень, ножницы, бумага
Генерировать случайный элемент в игре из списка "камень, ножницы, бумага"
Обрабатывать выбор пользователя и сообщать, кто победил

#### Дополнительный функционал
Не предусмотрен

#### Описание взаимодействия с ботом
1. Пользователь отправляет команду /start боту (или стартует его, найдя в поиске)
2. Бот приветствует пользователя и предлагает сыграть в игру "Камень, ножницы, бумага", отправляя клавиатуру с ответами
   "Давай!" и "Не хочу!", а также предлагает пользователю прочитать подробные правила, отправив команду /help
3. На этом этапе пользователь может совершить 4 действия:
    - Согласиться играть с ботом в игру, нажав на обычную кнопку "Давай!"
    - Не согласиться играть с ботом, нажав на обычную кнопку "Не хочу!"
    - Отправить в чат команду /help
    - Отправить в чат любое другое сообщение
4. Пользователь нажимает на обычную кнопку "Давай!":
    a) Бот присылает в чат сообщение "Отлично! Делай свой выбор!"
    b) Бот отправляет в чат клавиатуру с кнопками выбора "Камень", "Ножницы" и "Бумага"
    c) На этом этапе пользователь может совершить 3 действия:
     - Нажать на одну из кнопок выбора ("Камень", "Ножницы" или "Бумага")
     - Отправить в чат команду /help
     - Отправить в чат любое другое сообщение
    d) Пользователь нажимает на одну из кнопок выбора ("Камень", "Ножницы" или "Бумага"):
     - Бот генерирует случайный ответ из того же списка
     - Бот проверяет кто победил 
     - Бот сообщает пользователю кто победил
     - Бот отправляет пользователю предложение сыграть еще раз и клавиатуру для выбора с кнопками "Давай!" и "Не хочу!"
5. Пользователь нажимает на кнопку "Не хочу!":
    - Клавиатура сворачивается
    - Бот присылает сообщение "Хорошо. Если, вдруг, захочешь сыграть - открой клавиатуру и нажми "Давай!"
6. Пользователь отправляет в чат команду /help:
    - Бот присылает в чат правила игры, предложение сыграть и клавиатуру с кнопками "Давай!" и "Не хочу!"
7. Пользователь отправляет в чат любое другое сообщение:
    - Бот присылает в чат сообщение, что не понимает пользователя

Структура проекта:
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
 │   ├── user_handlers.py                          # Модуль с обработчиками апдейтов от пользователя
 │   └── other_handlers.py                         # Модуль для хранения хэндлера, который будет обрабатывать сообщения, 
 │                                                 # не предусмотренные в рамках общения пользователя с ботом.
 ├── 📁 keyboards/                                 # Директория для хранения клавиатур отправляемые пользователю.
 │   ├── __init__.py                               # Файл-инициализатор пакета.                      
 │   └── keyboards.py                              # Модуль с клавиатурами.
 │ 
 ├── 📁 lexicon/                                   # Директория для хранения словарей бота.
 │   ├── __init__.py                               # Файл-инициализатор пакета.                      
 │   └── lexicon_ru.py                             # Модуль со словарем соответствий команд и отображаемых текстов.
 │ 
 └── 📁 services/                                  # Директория для хранения бизнес-логики бота. 
     ├── __init__.py                               # Файл-инициализатор пакета.
     ├── services.py                               # Модуль с бизнес-логикой.                             
     └── game_state.py                             # Модуль для подсчета и сброса очков
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
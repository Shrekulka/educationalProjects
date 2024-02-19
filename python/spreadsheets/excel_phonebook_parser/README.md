# Project Overview:

## The project entails a simple Telegram bot, crafted utilizing the aiogram platform version 3.3.0. The bot is designed 
## to provide echo responses to user messages.

1. The primary module, bot_telegram.py, initiates the bot using polling. Within this module, bot and dispatcher objects 
   are imported from create_bot.py, along with handlers from handlers/client.py.

2. Event handlers for the bot reside in handlers/client.py. Within this module, the following handlers are defined:
   a) Command Handlers:
      - process_start_command
      - process_help_command
   b) Handlers for Different Types of Media Content:
      - handle_sticker
      - handle_photo
      - handle_video
      - handle_video_note
      - handle_audio
      - handle_voice
      - handle_document
      - handle_location
      - handle_contact
   c) Handlers for Messages with Different Start and End Conditions:
      - handle_exact_hello_message
      - handle_starts_with_hello_message
      - handle_not_starts_with_hello_message
      - handle_not_ends_with_bot_message
      - handle_specific_user
      - handle_admins
      - handle_non_media
   d) Combined Handler:
      - process_send_vovite
   e) Handler for Sending Message Copies:
      - send_copy_message
   f) Handler for Other Text Messages:
      - handle_other_messages
   g) Handlers for Bot Blocking/Unblocking:
      - process_user_blocked_bot
      - process_user_unblocked_bot
### After defining these handlers, they are registered to react to messages of various formats by invoking the 
### register_handlers_client function, which is passed to the main bot_telegram.py module.

### Here is the list of message content types:
    UNKNOWN: Unknown type
    ANY: Any type
    TEXT: Text message
    ANIMATION: Animation (animated sticker)
    AUDIO: Audio message
    DOCUMENT: Document
    PHOTO: Photo
    STICKER: Sticker
    STORY: Story
    VIDEO: Video
    VIDEO_NOTE: Video note
    VOICE: Voice message
    HAS_MEDIA_SPOILER: Message with media spoiler
    CONTACT: Contact
    DICE: Dice
    GAME: Game
    POLL: Poll
    VENUE: Venue (address)
    LOCATION: Location
    NEW_CHAT_MEMBERS: New chat members
    LEFT_CHAT_MEMBER: Left chat member
    NEW_CHAT_TITLE: New chat title
    NEW_CHAT_PHOTO: New chat photo
    DELETE_CHAT_PHOTO: Delete chat photo
    GROUP_CHAT_CREATED: Group chat created
    SUPERGROUP_CHAT_CREATED: Supergroup chat created
    CHANNEL_CHAT_CREATED: Channel chat created
    MESSAGE_AUTO_DELETE_TIMER_CHANGED: Message auto-delete timer changed
    MIGRATE_TO_CHAT_ID: Migrate to chat with specified ID
    MIGRATE_FROM_CHAT_ID: Migrate from chat with specified ID
    PINNED_MESSAGE: Pinned message
    INVOICE: Invoice
    SUCCESSFUL_PAYMENT: Successful payment
    USERS_SHARED: Users shared the bot
    CHAT_SHARED: Chat shared the bot
    CONNECTED_WEBSITE: Connected website
    WRITE_ACCESS_ALLOWED: Write access allowed
    PASSPORT_DATA: Passport data
    PROXIMITY_ALERT_TRIGGERED: Proximity alert triggered
    FORUM_TOPIC_CREATED: Forum topic created
    FORUM_TOPIC_EDITED: Forum topic edited
    FORUM_TOPIC_CLOSED: Forum topic closed
    FORUM_TOPIC_REOPENED: Forum topic reopened
    GENERAL_FORUM_TOPIC_HIDDEN: General forum topic hidden
    GENERAL_FORUM_TOPIC_UNHIDDEN: General forum topic unhidden
    GIVEAWAY_CREATED: Giveaway created
    GIVEAWAY: Giveaway
    GIVEAWAY_WINNERS: Giveaway winners
    GIVEAWAY_COMPLETED: Giveaway completed
    VIDEO_CHAT_SCHEDULED: Video chat scheduled
    VIDEO_CHAT_STARTED: Video chat started
    VIDEO_CHAT_ENDED: Video chat ended
    VIDEO_CHAT_PARTICIPANTS_INVITED: Video chat participants invited
    WEB_APP_DATA: Web app data
    USER_SHARED: User shared

3. The utils directory contains scripts for various auxiliary functions, in this case, client_utils.py.

4. The bot token is stored in the .env file, which is used for configuration.
   Configuration settings, including the token, are loaded using the Config class from the config_data.config module.
   The Config class provides access to bot settings such as the token and other parameters.
   Logging settings are defined in logger.py.

5.  Project Structure:
    ```bash
    📁 simple_echo_bot/       # Main project directory.
    │
    ├── 📁 config_data/       # Package with configuration data.
    │   ├── __init__.py       # File indicating that the directory is a Python package.
    │   └── config.py         # Module with configuration data.
    │
    ├── 📁 handlers/          # Directory with bot event handlers.
    │   ├── __init__.py       # Initialization of the handlers module.
    │   └── client.py         # Client handler module.
    │
    ├── 📁 utils/             # Directory for bot utility functions.
    │   ├── __init__.py       # Initialization of the utility functions module.
    │   └── client_utils.py   # Module for bot utility functions.
    │
    ├── logger.py             # Module for logging.
    │
    ├── bot_telegram.py       # Main Telegram bot module.
    │
    ├── .env                  # File with configuration and secrets.
    │ 
    ├── .env.example          # Example .env file for other developers.
    │
    ├── .gitignore            # File to ignore files by version control system.
    │
    ├── create_bot.py         # Module for creating the bot.
    │
    ├── requirements.txt      # Contains a list of required packages and their versions for the project to work correctly.    
    │
    └── README.md             # Project information.
    ```



# Проект представляет собой простого телеграм-бота, созданного с использованием платформы aiogram версии 3.3.0. 
## Бот предназначен для эхо-ответов на сообщения пользователей.

1. Основной модуль bot_telegram.py запускает бота с использованием polling. В этом модуле импортируются объекты бота и 
   диспетчера из create_bot.py и обработчики из handlers/client.py.

2. Обработчики (хэндлеры) событий бота находятся в handlers/client.py. 
### В этом модуле определены следующие обработчики:
    a) Обработчики команд:
       - process_start_command
       - process_help_command
    b) Обработчики разных типов медиа контента:
       - handle_sticker
       - handle_photo
       - handle_video
       - handle_video_note
       - handle_audio
       - handle_voice
       - handle_document
       - handle_location
       - handle_contact
    c) Обработчики для сообщений с различными условиями начала и окончания:
       - handle_exact_hello_message
       - handle_starts_with_hello_message
       - handle_not_starts_with_hello_message
       - handle_not_ends_with_bot_message
       - handle_specific_user
       - handle_admins
       - handle_non_media
    d) Комбинированный обработчик:
       - process_send_vovite
    e) Обработчик для отправки копий сообщений:
       - send_copy_message
    f) Обработчик других текстовых сообщений:
       - handle_other_messages
    g) Обработчики блокировки/разблокировки бота:
       - process_user_blocked_bot
       - process_user_unblocked_bot
### После чего происходит регистрация хендлеров для реагирования на сообщения различных форматов, с помощью вызова 
### функции register_handlers_client, которая передается в главный модуль bot_telegram.py.

### Этот объект представляет тип содержимого сообщения:
    UNKNOWN = 'unknown'  # Неизвестный тип

    ANY = 'any'  # Любой тип

    TEXT = 'text'  # Текстовое сообщение

    ANIMATION = 'animation'  # Анимация (анимированный стикер)

    AUDIO = 'audio'  # Аудиосообщение

    DOCUMENT = 'document'  # Документ

    PHOTO = 'photo'  # Фотография

    STICKER = 'sticker'  # Стикер

    STORY = 'story'  # История

    VIDEO = 'video'  # Видео

    VIDEO_NOTE = 'video_note'  # Видеозаметка

    VOICE = 'voice'  # Голосовое сообщение

    HAS_MEDIA_SPOILER = 'has_media_spoiler'  # Сообщение с медиа-спойлером

    CONTACT = 'contact'  # Контакт

    DICE = 'dice'  # Игральная кость

    GAME = 'game'  # Игра

    POLL = 'poll'  # Опрос

    VENUE = 'venue'  # Местоположение (адрес)

    LOCATION = 'location'  # Геопозиция

    NEW_CHAT_MEMBERS = 'new_chat_members'  # Новые участники чата

    LEFT_CHAT_MEMBER = 'left_chat_member'  # Покинувший чат участник

    NEW_CHAT_TITLE = 'new_chat_title'  # Новое название чата

    NEW_CHAT_PHOTO = 'new_chat_photo'  # Новое фото чата

    DELETE_CHAT_PHOTO = 'delete_chat_photo'  # Удаление фото чата

    GROUP_CHAT_CREATED = 'group_chat_created'  # Создание группового чата

    SUPERGROUP_CHAT_CREATED = 'supergroup_chat_created'  # Создание супергруппового чата

    CHANNEL_CHAT_CREATED = 'channel_chat_created'  # Создание канала

    MESSAGE_AUTO_DELETE_TIMER_CHANGED = 'message_auto_delete_timer_changed'  # Изменение таймера автоматического 
                                                                               удаления сообщений
    MIGRATE_TO_CHAT_ID = 'migrate_to_chat_id'  # Миграция в чат с указанным ID

    MIGRATE_FROM_CHAT_ID = 'migrate_from_chat_id'  # Миграция из чата с указанным ID

    PINNED_MESSAGE = 'pinned_message'  # Закрепленное сообщение

    INVOICE = 'invoice'  # Счет

    SUCCESSFUL_PAYMENT = 'successful_payment'  # Успешная оплата

    USERS_SHARED = 'users_shared'  # Пользователи, которые поделились ботом

    CHAT_SHARED = 'chat_shared'  # Чат, который поделился ботом

    CONNECTED_WEBSITE = 'connected_website'  # Подключенный веб-сайт

    WRITE_ACCESS_ALLOWED = 'write_access_allowed'  # Разрешение на запись

    PASSPORT_DATA = 'passport_data'  # Паспортные данные

    PROXIMITY_ALERT_TRIGGERED = 'proximity_alert_triggered'  # Сработало предупреждение о близости

    FORUM_TOPIC_CREATED = 'forum_topic_created'  # Создана тема форума

    FORUM_TOPIC_EDITED = 'forum_topic_edited'  # Отредактирована тема форума

    FORUM_TOPIC_CLOSED = 'forum_topic_closed'  # Закрыта тема форума

    FORUM_TOPIC_REOPENED = 'forum_topic_reopened'  # Повторно открыта тема форума

    GENERAL_FORUM_TOPIC_HIDDEN = 'general_forum_topic_hidden'  # Скрыта общая тема форума

    GENERAL_FORUM_TOPIC_UNHIDDEN = 'general_forum_topic_unhidden'  # Открыта общая тема форума

    GIVEAWAY_CREATED = 'giveaway_created'  # Создан розыгрыш

    GIVEAWAY = 'giveaway'  # Розыгрыш

    GIVEAWAY_WINNERS = 'giveaway_winners'  # Победители розыгрыша

    GIVEAWAY_COMPLETED = 'giveaway_completed'  # Завершен розыгрыш

    VIDEO_CHAT_SCHEDULED = 'video_chat_scheduled'  # Запланирован видеочат

    VIDEO_CHAT_STARTED = 'video_chat_started'  # Начат видеочат

    VIDEO_CHAT_ENDED = 'video_chat_ended'  # Завершен видеочат

    VIDEO_CHAT_PARTICIPANTS_INVITED = 'video_chat_participants_invited'  # Приглашены участники видеочата

    WEB_APP_DATA = 'web_app_data'  # Данные веб-приложения

    USER_SHARED = 'user_shared'  # Пользователь, который поделился

3. В каталоге utils находятся скрипты для различных вспомогательных функций, в нашем случае - это client_utils.py.

4. Токен бота хранится в файле .env, который используется для конфигурации.
   Настройки конфигурации, включая токен, загружаются с помощью класса Config из модуля config_data.config.
   Класс Config обеспечивает доступ к настройкам бота, таким как токен, и другим параметрам.
   Настройки логирования определены в logger.py.
 

5. Структура проекта:
    ```bash
    📁 simple_echo_bot/       # Основной каталог проекта.
    │
    ├── 📁 config_data/       # Пакет с конфигурационными данными.
    │   ├── __init__.py       # Файл, обозначающий, что директория является пакетом Python.
    │   └── config.py         # Модуль с конфигурационными данными.
    │
    ├── 📁 handlers/          # Каталог с обработчиками событий бота.
    │   ├── __init__.py       # Инициализация модуля обработчиков.
    │   └── client.py         # Модуль обработчика клиентов.
    │
    ├── 📁 utils/             # Каталог вспомогательных функций для бота
    │   ├── __init__.py       # Инициализация модуля вспомогательных функций
    │   └── client_utils.py   # Модуль вспомогательных функций для бота
    │
    ├── logger.py             # Модуль для логирования.
    │
    ├── bot_telegram.py       # Основной модуль телеграм-бота.
    │
    ├── .env                  # Файл с конфигурацией и секретами.
    │ 
    ├── .env.example          # Пример файла .env для других разработчиков.
    │
    ├── .gitignore            # Файл для игнорирования файлов системой контроля версий.
    │
    ├── create_bot.py         # Модуль для создания бота.
    │
    ├── requirements.txt      # Содержит список пакетов и их версий, необходимых для корректной работы проекта.    
    │
    └── README.md             # Информация о проекте.
    ```

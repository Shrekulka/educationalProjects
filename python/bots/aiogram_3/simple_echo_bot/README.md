# Project Overview

## The project is a simple Telegram bot created using the aiogram platform version 3.3.0. The bot is designed to provide
## echo responses to user messages.

1. The main module, bot_telegram.py, launches the bot using polling. This module imports bot and dispatcher objects from 
   create_bot.py and handlers from handlers/client.py.
2. Event handlers for the bot are located in handlers/client.py.
## In this module, the following handlers are defined:
    - cmd_start: Handler for the "/start" command, which sends a welcome message with the user's name and deletes the
      /start command from the chat.
    - process_help_command: Handler for the "/help" command, which sends an informational message.
    - handle_sticker: Handler for stickers.
    - handle_photo: Handler for photos.
    - handle_video: Handler for videos.
    - handle_video_note: Handler for video notes.
    - handle_audio: Handler for audio files.
    - handle_voice: Handler for voice messages.
    - handle_document: Handler for documents.
    - handle_location: Handler for locations.
    - handle_contact: Handler for contacts.
    - send_copy_message: Handler to send a copy of the message, regardless of content type (Audio, Video, Sticker,
      Animation, Document, Voice).
    - handle_other_messages: Handler for all other text messages.
    - register_handlers_client: Registration of all handlers and passing them to the bot_telegram file.
3. The bot token is stored in config.py, and logging settings are defined in logger.py.

4. Project Structure:
    ```bash
    ai_checklist_guardian/   # Main project folder.
    │
    ├── handlers/             # Folder containing event handlers for the bot.
    │   ├── __init__.py       # Module initialization.
    │   └── client.py         # Module for client handlers.
    │
    ├── logger.py             # Module for logging.
    │
    ├── bot_telegram.py       # Main module for the Telegram bot.
    │
    ├── config.py             # Configuration file.
    │
    ├── create_bot.py         # Module for creating the bot.
    │
    ├── requirements.txt      # Contains a list of packages and their versions required for the project.
    │
    └── README.md             # Project information.
    ```




# Проект представляет собой простого телеграм-бота, созданного с использованием платформы aiogram версии 3.3.0. 
## Бот предназначен для эхо-ответов на сообщения пользователей.

1. Основной модуль bot_telegram.py запускает бота с использованием polling. В этом модуле импортируются объекты бота и 
   диспетчера из create_bot.py и обработчики из handlers/client.py.

2. Обработчики событий бота находятся в handlers/client.py. 
## В этом модуле определены следующие обработчики:
   - cmd_start: Обработчик команды "/start", который отправляет приветственное сообщение с именем пользователя и удаляет 
     команду /start из чата.
   - process_help_command: Обработчик команды "/help", который отправляет информационное сообщение.
   - handle_sticker: Обработчик стикеров.
   - handle_photo: Обработчик фотографий.
   - handle_video: Обработчик видео.
   - handle_video_note: Обработчик видео-заметок.
   - handle_audio: Обработчик аудиофайлов.
   - handle_voice: Обработчик голосовых сообщений.
   - handle_document: Обработчик документов.
   - handle_location: Обработчик местоположений.
   - handle_contact: Обработчик контактов.
   - send_copy_message: Обработчик для отправки копии сообщения, не зависимо от типа контента (Audio, Video, Sticker, 
     Animation, Document, Voice).
   - handle_other_messages: Обработчик для всех остальных текстовых сообщений.
   - register_handlers_client: Регистрация всех хэндлеров и передача их в файл bot_telegram
3. Токен бота хранится в config.py, а настройки логирования определены в logger.py.

4. Структура проекта:
    ```bash
    ai_checklist_guardian/   # Основная папка проекта.
    │
    ├── handlers/             # Папка с обработчиками событий бота.
    │   ├── __init__.py       # Инициализация модуля обработчиков.
    │   └── client.py         # Модуль обработчика клиентов.
    │
    ├── logger.py             # Модуль для логирования.
    │
    ├── bot_telegram.py       # Основной модуль телеграм-бота.
    │
    ├── config.py             # Конфигурационный файл.
    │
    ├── create_bot.py         # Модуль для создания бота.
    │
    ├── requirements.txt      # Содержит список пакетов и их версий, необходимых для корректной
    │                         # работы проекта.
    │
    └── README.md             # Информация о проекте.
    ```
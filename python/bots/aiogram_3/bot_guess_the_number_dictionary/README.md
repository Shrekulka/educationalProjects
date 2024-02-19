# This code represents a module for working with a dictionary in a Telegram bot for the "Guess the Number" game. It contains functions
# for dictionary initialization, getting and updating user game data, as well as creating default data on
# the first game launch. The code also includes error logging when performing dictionary operations.

## Task Description

## What?
A Telegram bot with which you can play the "Guess the Number" game.

# Why?
To be able to play a simple game with the bot.

## What should the bot be able to do?
1. Generate a random number from 1 to 100.
2. Maintain the state ("in-game", "not in-game").
3. Count the number of attempts remaining for the user.
4. Compare user answers with the guessed number.

## Additional functionality
- The bot can show user game statistics upon request.

## Interaction Description with the Bot
1. The user sends the /start command to the bot (or starts it by finding it in the search).
2. The bot greets the user and suggests playing the "Guess the Number" game, also suggests the user to read detailed 
   rules by sending the /help command.
3. At this stage, the user can take 5 actions:
   a) Agree to play the game with the bot by sending "Yes" or "Let's go" or "Play" etc.
   b) Decline to play by sending "No" or "I don't want to" or "Another time" etc.
   c) Send the /help command to the chat.
   d) Send the /stat command to the chat.
   e) Send any other message to the chat.
4. The user agrees to play the game:
   a) The bot informs the user that it is very glad to play and saves a random number from 1 to 100.
   b) The bot saves information that the user is in the "Game" state.
   c) The bot sets the user's attempt counter to the default value.
   d) At this stage, the user can perform 3 actions:
      - Send a number from 1 to 100 to the chat.
      - Send the /cancel command to the chat.
      - Send anything other than these 2 points.
   e) The user sends a number from 1 to 100 to the chat:
      - The bot compares the number sent by the user with the guessed one.
      - If the numbers match:
        - The bot congratulates the user on winning.
        - The bot changes the state from "Game" to "Not in-game".
        - The bot sends the user a message suggesting to play again.
        - The bot increases the user's game counter by 1.
        - The bot increases the user's win counter by 1.
      - If the user's number is less than the guessed one:
        - The bot decreases the user's attempt counter by one.
        - The bot informs the user that the guessed number is greater.
      - If the user's number is greater than the guessed one:
        - The bot decreases the user's attempt counter by one.
        - The bot informs the user that the guessed number is smaller.
   f) The user sends the /cancel command to the chat:
      - The bot changes the state from "Game" to "Not in-game".
      - The bot sends a message to the chat that the game is over.
      - The bot sends a message to the chat that if the user wants to play again, they should send a message 
        "Game" or "Play", or "Let's play" etc.
   g) The user in the "Game" state sends anything other than a number from 1 to 100 or the /cancel command:
      - The bot sends the user a message that according to the game rules, the user can only send numbers 
        from 1 to 100 or the /cancel command to the chat.
   h) If the user runs out of attempts:
      - The bot informs the user that they lost.
      - The bot informs the user what the guessed number was.
      - The bot changes the state from "Game" to "Not in-game".
      - The bot increases the user's game counter by 1.
      - The bot sends the user a message suggesting to play again.
5. The user declines to play the game:
   a) The bot sends the user a message like "Too bad :(" and instructions on what the user needs to do if they still 
      want to play.
6. The user sends the /help command to the chat:
   a) The bot sends the user game rules and command descriptions.
7. The user sends the /stat command to the chat:
   a) The bot sends the user game statistics (how many games were played in total and how many of them the user won).
   b) The bot sends the user a message suggesting to play.
8. The user sends any other message to the chat:
   a) The bot informs that it doesn't understand the user and suggests playing the game again.

9. Project Structure:
   ```bash
   ai_checklist_guardian/   # Main project folder.
   │
   ├── handlers/             # Folder with bot event handlers.
   │   ├── __init__.py       # Initialization of the handlers module.
   │   └── client.py         # Module for client handlers.
   │
   ├── utils/                # Directory for bot's auxiliary functions.
   │   ├── __init__.py       # Initialization module for auxiliary functions.
   │   └── client_utils.py   # Module for bot's auxiliary functions.
   │
   ├── logger.py             # Module for logging.
   │
   ├── bot_telegram.py       # Main Telegram bot module.
   │
   ├── config.py             # Configuration file.
   │
   ├── create_bot.py         # Module for creating the bot.
   │
   ├── requirements.txt      # Contains a list of packages and their versions required for the project to run correctly.
   │
   └── README.md             # Project information.
   ```
Educational material on Stepik - https://stepik.org/course/120924/syllabus



# Данный код представляет собой модуль для работы с словарем в Telegram боте для игры "Угадай число". Он содержит функции 
# для инициализации словаря, получения и обновления данных игры пользователя, а также создания данных по умолчанию при 
# первом запуске игры. Код также включает логирование ошибок при выполнении операций со словарем.


## Постановка задачи

## Что?
Телеграм-бот, с которым можно играть в игру "Угадай число"

## Чтобы что?
Чтобы можно было сыграть в простую игру с ботом

## Что бот должен уметь?
1. Генерировать случайное число от 1 до 100
2. Хранить состояние ("в игре", "не в игре")
3. Считать количество попыток, оставшихся у пользователя
4. Сравнивать ответы пользователя с загаданным числом

## Дополнительный функционал
 - Бот может показывать статистику игр пользователя по запросу

## Описание взаимодействия с ботом
1. Пользователь отправляет команду /start боту (или стартует его, найдя в поиске)
2. Бот приветствует пользователя и предлагает сыграть в игру "Угадай число", также предлагает пользователю прочитать 
   подробные правила, отправив команду /help
3. На этом этапе пользователь может совершить 5 действий:
   a) Согласиться поиграть с ботом в игру, отправив в чат "Да" или "Давай", или "Сыграем" и т.п.
   b) Не согласиться играть, отправив в чат "Нет" или "Не хочу", или "В другой раз" и т.п.
   с) Отправить в чат команду /help
   d) Отправить в чат команду /stat
   e) Отправить в чат любое другое сообщение
4. Пользователь отправляет в чат согласие играть в игру:
   a) Бот сообщает пользователю, что очень рад поиграть и сохраняет рандомное число от 1 до 100
   b) Бот сохраняет информацию о том, что пользователь находится в состоянии "Игра"
   с) Бот устанавливает счетчик попыток пользователя в значение по умолчанию
   d) Пользователь на этом этапе может совершить 3 действия:
     - Прислать в чат число от 1 до 100
     - Прислать в чат команду /cancel
     - Прислать что-то отличное от этих 2-х пунктов
   e) Пользователь присылает в чат число от 1 до 100:
     - Бот сравнивает число, присланное пользователем, с загаданным
     - Если числа совпадают:
        - Бот поздравляет пользователя с победой
        - Бот переводит состояние из "Игра" в "Не игра"
        - Бот присылает пользователю сообщение с предложением сыграть еще раз
        - Бот увеличивает счетчик игр пользователя на 1
        - Бот увеличивает счетчик побед пользователя на 1
     - Если число пользователя меньше загаданного:
        - Бот уменьшает количество попыток пользователя на одну
        - Бот сообщает пользователю, что загаданное число больше
     - Если число пользователя больше загаданного:
        - Бот уменьшает количество попыток пользователя на одну
        - Бот сообщает пользователю, что загаданное число меньше
   f) Пользователь присылает в чат команду /cancel:
     - Бот переводит состояние из "Игра" в "Не игра"
     - Бот отправляет в чат сообщение о том, что игра закончилась
     - Бот отправляет в чат сообщение о том, что если пользователь захочет снова сыграть, то пусть отправит сообщение 
      "Игра" или "Сыграть", или "Давай сыграем" и т.п.
   g) Пользователь в состоянии "Игра" присылает в чат что-то отличное от числа от 1 до 100 или команды /cancel:
     - Бот отправляет пользователю сообщение о том, что по правилам игры пользователь может присылать в чат только числа 
      от 1 до 100 или команду /cancel
   h) Если у пользователя заканчивается количество попыток:
     - Бот сообщает пользователю, что тот проиграл
     - Бот сообщает пользователю, что загаданное число было таким-то
     - Бот меняет состояние "Игра" на "Не игра"
     - Бот увеличивает счетчик игр пользователя на 1
     - Бот оправляет пользователю сообщение с предложением сыграть еще раз
5. Пользователь отправляет в чат отказ играть в игру:
   a) Бот отправляет пользователю сообщение, типа, "Жаль :(" и инструкцию что нужно сделать пользователю, если он все-
      таки захочет поиграть
6. Пользователь отправляет в чат команду /help:
   a) Бот присылает пользователю правила игры и описание команд
7. Пользователь отправляет в чат команду /stat:
   a) Бот присылает пользователю статистику по играм (сколько всего было игр и в скольких из них пользователь выиграл)
   b) Бот присылает пользователю сообщение с предложением сыграть
8. Пользователь отправляет в чат любое другое сообщение:
   a) Бот сообщает, что не понимает пользователя и снова предлагает сыграть в игру


4. Структура проекта:
    ```bash
    ai_checklist_guardian/   # Основная папка проекта.
    │
    ├── handlers/             # Папка с обработчиками событий бота.
    │   ├── __init__.py       # Инициализация модуля обработчиков.
    │   └── client.py         # Модуль обработчика клиентов.
    │
    ├── utils/                # Каталог вспомогательных функций для бота
    │   ├── __init__.py       # Инициализация модуля вспомогательных функций
    │   └── client_utils.py   # Модуль вспомогательных функций для бота
    │
    ├── logger.py             # Модуль для логирования.
    │
    ├── bot_telegram.py       # Основной модуль телеграм-бота.
    │
    ├── config.py             # Конфигурационный файл.
    │
    ├── create_bot.py         # Модуль для создания бота.
    │
    ├── requirements.txt      # Содержит список пакетов и их версий, необходимых для корректной работы проекта.
    │
    └── README.md             # Информация о проекте.
    ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
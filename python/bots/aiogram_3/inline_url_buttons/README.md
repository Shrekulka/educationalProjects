# This is a Telegram bot with functionality to respond to the /start command and use URL buttons.

## The main logic works as follows:
- Upon receiving the /start command
- Corresponding texts are taken from the lexicon dictionary
- A response message is formed using data from the data dictionary
- A response message is sent with an attached keyboard containing URL buttons
- Configuration is placed in a separate package config_data, logging is configured in logger_config.

Thus, the bot is capable of responding to the /start command by sending a keyboard with useful links to the user.

### Each inline button should include one mandatory parameter - text. As you might guess, this is the text that 
### will be displayed on the button itself.

### And besides the mandatory parameter, each button should have only one optional parameter from the list:
1. text. The text parameter is the text that will be displayed on the button itself. This text usually contains
   a description or the name of the action that will be performed when the button is pressed.
2. url. URL buttons are inline buttons, clicking on which will take us to the browser via the link associated with
   this button, or to some internal resource of Telegram (channel, group, etc.) also by link. They are responsible
   for the url attribute of the InlineKeyboardButton class.
   As a parameter in url, not only http:// and https:// links can be specified, but also tg:// links. The latter
   opens in the Telegram app, just like links like https://t.me/.
   Pressing on inline buttons with the url parameter does not generate any updates that could be processed.
3. callback_data. The callback_data parameter is used to pass user data as a string when the button is clicked.
   This parameter can be used to determine further action or process information in the application.
4. web_app. The web_app parameter allows you to launch a web application or open a website in the Telegram built-in 
   browser.
5. login_url. The login_url parameter is used to create a button for logging in via Telegram Login. When the button is
   pressed, the user can authorize on an external website using their Telegram account.
6. switch_inline_query. The switch_inline_query parameter allows you to initiate an inline search in a Telegram chat or 
   channel when the button is pressed.
7. switch_inline_query_current_chat. The switch_inline_query_current_chat parameter also initiates an inline search,
   but only in the current chat.
8. switch_inline_query_chosen_chat. The switch_inline_query_chosen_chat parameter allows you to initiate an inline 
   search in a specific chat chosen by the user.
9. callback_game. The callback_game parameter is used to create a button that initiates a game process.
10. pay. The pay parameter is used to create a button that initiates a payment through Telegram.

As you can see, there are no such parameters as contact and location.

### Project Structure:
```bash
 📁 improved_echo_bot/                             # Project directory, main bot file.
 │
 ├── .env                                          # File with configuration and secrets.
 │
 ├── .env.example                                  # File with examples of secrets for GitHub
 │
 ├── .gitignore                                    # File telling git which files and directories not to track
 │
 ├── bot.py                                        # Main executable file - entry point to the bot
 │
 ├── requirements.txt                              # File with project dependencies.
 │
 ├── logger_config.py                              # Logger configuration.
 │
 ├── README.md                                     # File with project description.
 │
 ├── 📁 config_data/                               # Directory with bot configuration module.
 │   ├── __init__.py                               # Package initializer file. 
 │   └── config_data.py                            # Module for bot configuration.
 │ 
 ├── 📁 handlers/                                  # Directory with handlers.
 │   ├── __init__.py                               # Package initializer file.
 │   └── user_handlers.py                          # Module with handlers for user updates
 │                                                
 ├── 📁 keyboards/                                 # Directory for storing keyboards sent to the user.
 │   ├── __init__.py                               # Package initializer file.                      
 │   └── keyboards.py                              # Module with keyboards.
 │ 
 └── 📁 lexicon/                                   # Directory for storing bot dictionaries.
     ├── __init__.py                               # Package initializer file.            
     ├── data.py                                   # Module with project-related data.
     ├── urls.py                                   # Module with URLs and links.
     └── lexicon_ru.py                             # Module with a dictionary of command mappings and displayed texts.
```
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Это телеграм-бот с функционалом ответа на команду /start и используя URL-кнопки.

## Основная логика работы заключается в следующем:
- При получении команды /start
- Из словаря lexicon берутся соответствующие тексты
- Формируется текст ответного сообщения quando с использованием данных из словаря data
- Отправляется ответное сообщение с прикрепленной из keyboards клавиатурой с url-кнопками
- Конфигурация вынесена в отдельный пакет config_data, логирование настроено в logger_config.

Таким образом, бот умеет отвечать на команду /start, отправляя клавиатуру с полезными ссылками для пользователя.

### Каждая инлайн-кнопка должна включать один обязательный параметр - text. Как не сложно догадаться - это текст, 
### который будет отображаться на самой кнопке.

### И помимо обязательного параметра у каждой кнопки должен быть только один необязательный из списка:
1. text.  Параметр text представляет собой текст, который будет отображаться на самой кнопке. Этот текст обычно содержит
   описание или название действия, которое будет выполнено при нажатии на кнопку.
2. url. URL-кнопки - это такие инлайн-кнопки, нажатие на которые переводит нас в браузер по ссылке, связанной с этой 
   кнопкой, или на какой-то внутренний ресурс самого Телеграм (канал, группу и т.п.) тоже по ссылке. За них отвечает 
   атрибут url класса InlineKeyboardButton.
   В качестве параметра в url могут быть указаны не только ссылки http:// и https://, но и tg://. Последние открываются 
   в самом приложении Telegram, также как и ссылки вида https://t.me/. 
   Нажатие на инлайн-кнопки с параметром url не генерирует никаких апдейтов, которые можно было бы обработать.
3. callback_data. Параметр callback_data используется для передачи пользовательских данных в виде строки при нажатии на 
   кнопку. Этот параметр может быть использован для определения дальнейшего действия или обработки информации в 
   приложении.
4. web_app. Параметр web_app позволяет запускать веб-приложение или открывать веб-сайт во встроенном браузере Telegram.
5. login_url. Параметр login_url используется для создания кнопки входа через Telegram Login. При нажатии на кнопку 
   пользователь может авторизоваться на внешнем сайте с использованием своего аккаунта Telegram.
6. switch_inline_query. Параметр switch_inline_query позволяет инициировать встроенный поиск в чате или канале Telegram 
   при нажатии на кнопку.
7. switch_inline_query_current_chat. Параметр switch_inline_query_current_chat также инициирует встроенный поиск, но 
   только в текущем чате.
8. switch_inline_query_chosen_chat. Параметр switch_inline_query_chosen_chat позволяет инициировать встроенный поиск в 
9. определенном чате, выбранном пользователем.
9. callback_game. Параметр callback_game используется для создания кнопки, которая инициирует игровой процесс.
10. pay. Параметр pay используется для создания кнопки, которая инициирует платеж через Telegram.

Как видно, таких параметров - как контакт и локация - попросту нет.

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
 │   └── user_handlers.py                          # Модуль с обработчиками апдейтов от пользователя
 │                                               
 ├── 📁 keyboards/                                 # Директория для хранения клавиатур отправляемые пользователю.
 │   ├── __init__.py                               # Файл-инициализатор пакета.                      
 │   └── keyboards.py                              # Модуль с клавиатурами.
 │ 
 └── 📁 lexicon/                                   # Директория для хранения словарей бота.
     ├── __init__.py                               # Файл-инициализатор пакета.            
     ├── data.py                                   # Модуль с данными, связанными с проектом.
     ├── urls.py                                   # Модуль с URL-адресами и ссылками.
     └── lexicon_ru.py                             # Модуль со словарем соответствий команд и отображаемых текстов.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
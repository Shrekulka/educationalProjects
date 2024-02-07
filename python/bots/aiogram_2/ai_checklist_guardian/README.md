# Test Task:

This test task is designed to evaluate your Python programming skills and understanding of working with the aiogram 
(version 2.25) and OpenAI libraries. Your task is to create a simple Telegram bot that will send a welcome message to 
users upon their first interaction with the bot. Afterward, the bot should allow the user to choose one of 5 locations 
(Location 1, Location 2, Location 3, Location 4, Location 5) and fill out a checklist. The checklist should include 5 
items with the option to choose either "All clear" or "Leave a comment." After providing a comment, the user should have
the option to upload a photo and save its link. Once the checklist is completed, a report should be generated and sent
to OpenAI for analysis by artificial intelligence. The analyzed report should then be sent to the user.

## Technical Requirements:

### Bot Creation:

- Create a new bot on Telegram using BotFather.
- Configure the bot using the aiogram library.
- 
### Welcome Message:
The bot should send a welcome message to the user upon their first interaction. The message can be a simple text, for 
example: "Hello! Let's get started."

Use the OpenAI library to analyze the generated report.

### Sending Text Version:
After analysis, the bot should send the analyzed text to the user as a text message in Telegram.

### Additional Requirements:
- The code should be clear and well-structured.
- Use comments to explain key parts of the code.
- Implement error handling to manage possible exceptions during the bot's operation.

## Project Structure:
```bash
ai_checklist_guardian/   # Main project folder.
│
├── data_base/                              
│   ├── __init__.py                          # Initialization of the database module.
│   └── sqlite_db.py                         # Module for working with the SQLite database.
│
├── docs/                              
│   └── Test _ Python Developer.docx        # Project documentation.
│    
├── handlers/                       
│   ├── __init__.py                         # Initialization of the handlers module.
│   ├── client.py                           # Module for handling client interactions.
│
├── keyboards/
│   ├── __init__.py                         # Initialization of the keyboards module.
│   └── client_kb.py                        # Module for client keyboards.
│
├── models/
│   ├── __init__.py                         # Initialization of the models module.
│   └── user_data.py                        # Module for working with user data.
│ 
├── services/
│   ├── __init__.py                         # Initialization of the services module.
│   └── openai_service.py                   # Module for OpenAI service.
│
├── logger.py                               # Module for logging.
│
├── bot_telegram.py                         # Main Telegram bot module.
│
├── config.py                               # Configuration file.
│
├── create_bot.py                           # Module for bot creation.
│
├── states.py                               # Module for defining bot states.
│
├── requirements.txt                        # Contains a list of packages and their versions required for the project.
└── README.md                               # Project information.
```
The code implements a Telegram bot that allows users to send reports on the status of different objects and analyze them
using OpenAI GPT-3.5-Turbo. The main goal of the bot is to facilitate user interaction with checklist systems and 
automate the process of analyzing received reports.

## Below is a brief description of key parts of the code:

1. SQLite Database Module (ai_checklist_guardian/data_base/sqlite_db.py):
   This module is responsible for working with the SQLite database. It includes functions for initializing the database,
   adding new reports, retrieving a specific report, reading all reports, deleting a report, and more. It uses an 
   asynchronous approach for efficiency and handles errors during database interaction.
2. Telegram Message Handlers (ai_checklist_guardian/handlers/client.py):
   These handlers interact with messages and commands from users. They use states (UserSteps) to determine the current 
   context of user input. The handlers also display keyboards for selecting locations and checklists, managing the 
   entire process of creating and sending reports.
3. Keyboards for Selecting Locations and Checklists (ai_checklist_guardian/keyboards/client_kb.py):
   This module creates various types of keyboards that help users choose locations, checklist options, and other 
   features by pressing buttons.
4. UserData Class (ai_checklist_guardian/models/user_data.py):
   This class represents an object containing user data, such as location, selected checklist option, user comment, link
   to a photo, and the report itself. It is used for convenient creation and sending of reports.
5. OpenAI Service Module (ai_checklist_guardian/services/openai_service.py):
   This module contains a class that interacts with the OpenAI API for analysis and obtaining responses to reports. It 
   also provides preprocessing of the report before sending it to OpenAI.
6. Main Bot File (ai_checklist_guardian/bot_telegram.py):
   This file initializes the Telegram bot, sets up message handlers, and handles the processing and storage of reports 
   in the database and OpenAI. It also contains a start function that is called when the bot is launched.
7. Logging Configuration File (logger.py):
   In this file, the logging system is configured to track events and errors. It uses colors for better differentiation 
   of different log levels.
8. User States File (ai_checklist_guardian/states.py):
   This module defines the UserSteps class, which is used to manage user states during data input and interaction with 
   the bot.




# Тестове завдання:
Це тестове завдання спрямоване на оцінку ваших навичок у програмуванні на Python та розуміння роботи з бібліотеками 
aiogram ( версія 2.25 ) та OpenAI. Ваше завдання полягає у створенні простого Telegram-бота, який буде відправляти 
вітальне повідомлення користувачам при їх першому зверненні до бота, після чого, бот має дати можливість користувачу  
обрати одну з 5 локацій ( Локація 1, Локація 2, Локація 3, Локація 4, Локація 5) та заповнити чек-лист. В чек-лист 
необхідно включити  5 пунктів з можливістю обрати варіант:  "Все чисто" або "Залишити коментар". Після коментаря, має 
бути можливість завантажити фотографію та зберегти посилання на неї. Після завершення чек-листа, має сформуватись звіт,
який відправиться на OpenAI для аналізу штучним інтелектом. Проаналізований звіт відправити користувачу. 

### Технічні вимоги:
Створення бота:
Створіть новий бот у Telegram через BotFather.
Налаштуйте бота за допомогою бібліотеки aiogram.

### Вітальне повідомлення:
Бот повинен відправляти вітальне повідомлення користувачу при першому зверненні до бота. Повідомлення може бути простим 
текстом, наприклад: "Привіт! Почнімо працювати."

### Використовуйте бібліотеку OpenAI для аналізу сформованого звіту.

### Надсилання текстової версії:
Після аналізу , бот повинен надсилати цей текст користувачу у вигляді текстового повідомлення в Telegram.

### Додаткові вимоги:
Код має бути чітким та добре структурованим.
Використовуйте коментарі для пояснення ключових частин коду.
Використовуйте обробку помилок для управління можливими винятками під час роботи бота.



Структура проекта:
```bash
ai_checklist_guardian/   # Основна папка проекту.
│
├── data_base/                              
│   ├── __init__.py                          # Ініціалізація модуля бази даних.
│   └── sqlite_db.py                         # Модуль для роботи з базою даних SQLite.
│
├── docs/                              
│   └── Тестове _ Python Developer.docx     # Документація проекту.
│    
├── handlers/                       
│   ├── __init__.py                         # Ініціалізація модуля обробників.
│   ├── client.py                           # Модуль обробника клієнтів.
│
├── keyboards/
│   ├── __init__.py                        # Ініціалізація модуля клавіш.
│   └── client_kb.py                       # Модуль клавіш клієнта.
│
├── models/
│   ├── __init__.py                        # Ініціалізація модуля моделей.
│   └── user_data.py                       # Модуль для роботи з даними користувачів.
│ 
├── services/
│   ├── __init__.py                        # Ініціалізація модуля сервісів.
│   └── openai_service.py                  # Модуль сервісу OpenAI.
│
├── logger.py                              # Модуль для логування.
│
├── bot_telegram.py                        # Основний модуль телеграм-бота.
│
├── config.py                              # Конфігураційний файл.
│
├── create_bot.py                          # Модуль для створення бота.
│
├── states.py                              # Модуль для визначення станів бота.
│
├── requirements.txt                       # Містить список пакетів та їх версій, які необхідно встановити для коректної
│                                          # роботи проекту.
└── README.md                              # Інформація про проект.
```
Код представляє реалізацію Telegram-бота, який дозволяє користувачеві надсилати звіти про стан різних об'єктів та 
аналізувати їх за допомогою OpenAI GPT-3.5-Turbo. Основна мета бота - забезпечити взаємодію користувача з системою чек-
листів та автоматизацію процесу аналізу отриманих звітів.

## Нижче наведено короткий опис ключових частин коду:
1. Модуль бази даних SQLite (ai_checklist_guardian/data_base/sqlite_db.py):
   Цей модуль відповідає за роботу з базою даних SQLite. У ньому реалізовані функції для старту бази даних, додавання 
   нових звітів, отримання конкретного звіту, читання всіх звітів, видалення звіту та інші. Використовує асинхронний 
   підхід для ефективності та оброблює помилки під час взаємодії з базою даних.

2. Обробники повідомлень Telegram (ai_checklist_guardian/handlers/client.py):
   Ці обробники взаємодіють із повідомленнями та командами від користувачів. Вони використовують стани (UserSteps), щоб 
   визначити поточний контекст введення даних від користувача. Обробники також виводять клавіатури для вибору локацій та
   чек-листів, а також керують весь процес створення та відправлення звітів.

3. Клавіатури для вибору локацій та чек-листів (ai_checklist_guardian/keyboards/client_kb.py):
   У цьому модулі створюються різні види клавіатур, які допомагають користувачеві вибирати локації, чек-листи та інші 
   опції шляхом натискання кнопок.

4. Клас UserData (ai_checklist_guardian/models/user_data.py):
   Цей клас представляє об'єкт, що містить дані користувача, такі як локація, обрана опція чек-листу, коментар 
   користувача, посилання на фотографію та сам звіт. Його використовують для зручного створення та відправлення звітів.

5. Сервіс OpenAI (ai_checklist_guardian/services/openai_service.py):
   У цьому модулі міститься клас, який взаємодіє з OpenAI API для аналізу та отримання відповідей на звіти. Він також 
   забезпечує попередню обробку звіту перед відправленням його до OpenAI.

6. Основний файл бота (ai_checklist_guardian/bot_telegram.py):
   Цей файл ініціалізує телеграм-бота, встановлює обробники повідомлень та забезпечує обробку та збереження звітів в 
   базу даних та OpenAI. Також містить функцію старту, яка викликається при запуску бота.

7. Файл налаштувань логування (logger.py):
   У цьому файлі налаштовується система логування для відстеження подій та помилок. Використовує кольори для кращого 
   розрізнення різних рівнів логів.

8. Файл зі станами користувача (ai_checklist_guardian/states.py):
   Цей модуль визначає клас UserSteps, який використовується для керування станами користувача під час введення даних та
   взаємодії з ботом.
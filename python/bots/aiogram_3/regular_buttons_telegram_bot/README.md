# The project showcases the capabilities of the aiogram library for creating Telegram bots with button menus.

## Project Goal:

The goal of the project is to demonstrate various methods of creating and placing buttons, as well as some special 
features of buttons in aiogram.

### Within the project, 8 bot examples are implemented, demonstrating:
1. automatically_placing_buttons_using_method_add.py
    - Demonstrates the use of the add() method for automatic button placement.
    - Creates a keyboard with 5 buttons with width=4 and adds 10 more buttons using the add() method.
    - Buttons are added to the current row until space runs out (up to 8 buttons).
2. automatically_placing_buttons_using_method_adjust.py
    - Shows the use of the adjust() method to specify the number of buttons in each row.
    - Creates a keyboard with 8 buttons and uses adjust() to set 1 button in the first row and 3 buttons in the second 
      row.
3. automatically_placing_buttons_using_method_row.py
    - Demonstrates automatic button placement using the row() method.
    - First, 6 buttons are added in a row with width=4, then 4 more buttons with width=3.
    - Buttons are automatically moved to a new row.
4. creation_and_placement_of_buttons.py
    - Shows the creation of simple buttons and placing them on the keyboard.
    - Creates a 3x3 keyboard of buttons using loops and list comprehensions.
5. deletes_the_keyboard_when_the_button_is_pressed.py
    - Demonstrates deleting the keyboard after pressing a button.
    - When any of the 4 buttons is pressed, a message is sent and the keyboard is deleted.
6. hide_the_keyboard_when_the_button_is_pressed.py
    - Shows hiding the keyboard after the first button press.
    - Uses one_time_keyboard=True parameter when creating the keyboard.
7. special_regular_buttons.py
    - Example of creating special buttons: for sending a phone number, location, starting polls.
8. the_input_field_showed_a_hint_line.py
    - Demonstration of displaying a hint in the input field using the input_field_placeholder parameter.
   
For all bots, a unified configuration and logging system based on the environs and logging libraries is implemented.

Configuration (Telegram API access tokens) is loaded from the .env environment file.

Logging is implemented with colorful formatting and the ability to write to a file.

Project Structure:
```bash
📁 regular_buttons_telegram_bot/                           # Project directory, main bot file.
│
├── .env                                                   # Configuration and secrets file.
│
├── .env.example                                           # Example .env file for other developers.
│
├── .gitignore                                             # File to ignore version control system files.
│
├── automatically_placing_buttons_using_method_add.py      # Automatic button placement using the add() method.
│
├── automatically_placing_buttons_using_method_adjust.py   # Automatic button placement using the adjust() method.
│
├── automatically_placing_buttons_using_method_row.py      # Automatic button placement using the row() method.
│
├── creation_and_placement_of_buttons.py                   # Creation and placement of buttons.
│
├── deletes_the_keyboard_when_the_button_is_pressed.py     # Deleting the keyboard on button press.
│
├── hide_the_keyboard_when_the_button_is_pressed.py        # Hiding the keyboard on button press.
│
├── special_regular_buttons.py                             # Special buttons.
│
├── the_input_field_showed_a_hint_line.py                  # Input field hint.
│
├── requirements.txt                                       # Project dependencies file.
│
├── logger_config.py                                       # Logger configuration.
│
├── README.md                                              # Project description file.
│
└──  📁 config_data/                                       # Package with configuration data.
    ├── __init__.py                                        # File indicating that the directory is a Python package.
    └── config.py                                          # Module with configuration data.
```
Thus, the project demonstrates various capabilities of the aiogram library for creating Telegram bots with advanced 
button functionality.
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Это проект демонстрирует возможности библиотеки aiogram по созданию Telegram ботов с использованием кнопочных меню.

## Цель проекта - показать различные способы создания и размещения кнопок, а также некоторые специальные возможности 
## кнопок в aiogram.

### В рамках проекта реализовано 8 примеров ботов, демонстрирующих:
1. automatically_placing_buttons_using_method_add.py
    - Демонстрирует использование метода add() для автоматического размещения кнопок.
    - Создается клавиатура из 5 кнопок с параметром width=4 и дополнительно добавляется 10 кнопок методом add().
    - Кнопки добавляются в текущий ряд, пока в нем не закончится место (до 8 шт.)
2. automatically_placing_buttons_using_method_adjust.py
    - Показывает использование метода adjust() для указания количества кнопок в каждом ряду.
    - Создается клавиатура из 8 кнопок и с помощью adjust() задается 1 кнопка в первом ряду и 3 кнопки во втором.
3. automatically_placing_buttons_using_method_row.py
    - Демонстрирует авторазмещение кнопок с помощью метода row().
    - Сначала добавляется 6 кнопок в row с width=4, затем еще 4 кнопки с width=3.
    - Кнопки автоматически переносятся на новый ряд.
4. creation_and_placement_of_buttons.py
    - Показывает создание простых кнопок и размещение их в клавиатуре.
    - Создается клавиатура 3x3 из кнопок в цикле и генераторах списков.
5. deletes_the_keyboard_when_the_button_is_pressed.py
    - Демонстрирует удаление клавиатуры после нажатия на кнопку.
    - По нажатию на любую из 4 кнопок отправляется сообщение и удаляется клавиатура.
6. hide_the_keyboard_when_the_button_is_pressed.py
    - Показывает скрытие клавиатуры после первого нажатия на кнопку.
    - Используется параметр one_time_keyboard=True при создании клавиатуры.
7. special_regular_buttons.py
    - Пример создания специальных кнопок: для отправки номера телефона, геолокации, запуска опросов.
8. the_input_field_showed_a_hint_line.py
    - Демонстрация отображения подсказки в поле ввода с помощью параметра input_field_placeholder.
    - Для всех ботов реализована единая система конфигурирования и логирования на основе библиотек environs и logging.
   
Конфигурация (токены доступа к API Telegram) загружается из файла окружения .env.

Логирование реализовано с красивым цветным оформлением c возможностью записи в файл.

Структура проекта:
```bash
📁 regular_buttons_telegram_bot/                           # Директория проекта, основной файл бота.
│
├── .env                                                   # Файл с конфигурацией и секретами.
│
├── .env.example                                           # Пример файла .env для других разработчиков.
│
├── .gitignore                                             # Файл для игнорирования файлов системой контроля версий.
│
├── automatically_placing_buttons_using_method_add.py      # Авторазмещение кнопок методом add.
│
├── automatically_placing_buttons_using_method_adjust.py   # Авторазмещение кнопок методом adjust.
│
├── automatically_placing_buttons_using_method_row.py      # Авторазмещение кнопок методом row.
│
├── creation_and_placement_of_buttons.py                   # Создание и размещение кнопок.
│
├── deletes_the_keyboard_when_the_button_is_pressed.py     # Удаление клавиатуры по кнопке.
│
├── hide_the_keyboard_when_the_button_is_pressed.py        # Скрытие клавиатуры по кнопке.  
│
├── special_regular_buttons.py                             # Специальные кнопки.
│
├── the_input_field_showed_a_hint_line.py                  # Подсказка в поле ввода.
│
├── requirements.txt                                       # Файл с зависимостями проекта.
│
├── logger_config.py                                       # Конфигурация логгера.
│
├── README.md                                              # Файл с описанием проекта.
│
└──  📁 config_data/                                       # Пакет с конфигурационными данными.
    ├── __init__.py                                        # Файл, обозначающий, что директория является пакетом Python.
    └── config.py                                          # Модуль с конфигурационными данными.
```
Таким образом, проект демонстрирует разнообразные возможности библиотеки aiogram для создания Telegram ботов с 
продвинутой работой с кнопками.
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
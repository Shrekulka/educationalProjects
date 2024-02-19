# This project is the "Numbers API Explorer" program, allowing the user to interact with the Numbers API, requesting 
# various interesting facts and information about numbers. The project consists of two main files: main.py and 
# numbers_menu.py.

## API requests are made to http://numbersapi.com/
- for math - 'numbersapi.com/your_number/math'
- for trivia - 'numbersapi.com/your_number'
- for date - 'numbersapi.com/your_month/your_day/date'
- for random - 'numbersapi.com/random'

1. main.py:
- The file contains the main() function, which is the main entry point of the program.
- Inside main(), an instance of the NumbersMenu class is created, and an infinite loop for user interaction is initiated.
- The user sees the main menu, chooses a category, and the program processes their choice by interacting with the 
  NumbersMenu class.

2.numbers_menu.py:
- Contains the NumbersMenu class designed to manage user interaction.
- The class has methods for displaying the menu, getting user choices, processing choices, sending API requests, 
  building URLs for requests, displaying results, and handling errors.
- Utilizes the requests library for making HTTP requests and colorama for styling text in the console.
- The class also includes several helper methods, such as checking if the category is "date" and error handling.

## General flow of the program:
The user selects a category from the menu, enters necessary parameters (e.g., a number or a date).
The program constructs a URL for the request based on the user's choice.
An HTTP request is made to the Numbers API, and the result is displayed on the screen.
The project also includes error handling, including error message output and logging.

## Project structure:
  ```bash
  numbers_api_explorer/      # Main project folder.
  │
  ├── logger.py              # Module for logging events in the project.
  │
  ├── config.py              # File with settings for the project.
  │
  ├── requirements.txt       # File specifying dependencies (libraries and their versions) for the project. This can
  │                          # be used for easy deployment of the project on other systems.
  ├── main.py                # Entry point of the application. File containing code to create and run the application.
  │
  ├── numbers_menu.py        # Module containing the NumbersMenu class responsible for user interaction.
  │
  ├── README.md              # File with project description and instructions for usage.
  ```
Educational material on Stepik - https://stepik.org/course/120924/syllabus



# Данный проект представляет собой программу "Numbers API Explorer", которая позволяет пользователю взаимодействовать с 
# Numbers API, запрашивая различные интересные факты и информацию о числах. Проект состоит из двух основных файлов: 
# main.py и numbers_menu.py.

## Запрос к API осуществляется http://numbersapi.com/
- для math - 'numbersapi.com/your_number/math'
- для trivia - 'numbersapi.com/your_number'
- для date - 'numbersapi.com/your_month/your_day/date'
- для random - 'numbersapi.com/random'

1. main.py:
- Файл содержит функцию main(), которая является основной точкой входа в программу.
- Внутри main(), создается экземпляр класса NumbersMenu и запускается бесконечный цикл взаимодействия с пользователем.
- Пользователь видит основное меню, выбирает категорию, и программа обрабатывает его выбор, взаимодействуя с классом 
  NumbersMenu.
2.numbers_menu.py
- Содержит класс NumbersMenu, предназначенный для управления взаимодействием с пользователем.
- Класс имеет методы для отображения меню, получения выбора пользователя, обработки выбора, отправки запроса к API, 
  построения URL для запроса, отображения результата и обработки ошибок.
- Использует библиотеки requests для выполнения HTTP-запросов и colorama для стилизации текста в консоли.
- Класс также содержит несколько вспомогательных методов, таких как проверка категории на "date" и обработка ошибок.

## Общий ход выполнения программы:
Пользователь выбирает категорию из меню, вводит необходимые параметры (например, число или дату).
Программа формирует URL для запроса на основе выбора пользователя.
Выполняется HTTP-запрос к Numbers API, и результат отображается на экране.
Проект также предусматривает обработку ошибок, включая вывод сообщений об ошибке и логирование.

## Структура проекта:
  ```bash
  numbers_api_explorer/      # Основная папка проекта.
  │
  ├── logger.py              # Модуль для логирования событий в проекте.
  │
  ├── config.py              # Файл с настройками для проекта.
  │
  ├── requirements.txt       # Файл, где указаны зависимости (библиотеки и их версии) для проекта. Это может                        
  │                          # использоваться для легкого разворачивания проекта на других системах.
  ├── main.py                # Точка входа в приложение. Файл, где находится код для создания и запуска приложения.
  │
  ├── numbers_menu.py        # Модуль, содержащий класс NumbersMenu, отвечающий за взаимодействие с пользователем.        
  │
  ├── README.md              # Файл с описанием проекта и инструкциями по его использованию.
  ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus
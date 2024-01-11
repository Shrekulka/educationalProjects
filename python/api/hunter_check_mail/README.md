*Task:*
Select any service and create a client for it; 2-3 endpoints will be sufficient. Also, add a service that accepts some 
values and saves the results. Saving can be done simply in a local variable.

As an example:
https://hunter.io/api-documentation/v2
Implement sending a request for email checking and verification in the client.
And add an email checking service + CRUD for results, for storage, you can use a variable. Upload it to GitHub and 
package it.

Type hints are mandatory.
Use this linter: https://github.com/wemake-services/wemake-python-styleguide
setup.cfg https://gist.github.com/dfirst/0957711a40d640d335e128eec4c17f21

*Solution:*

Description of an email verification solution using the Hunter.io API:

1. A basic client has been implemented for sending HTTP requests to the Hunter.io API. It includes authentication logic,
   error handling, retry mechanisms, and more.
2. Separate clients have been created for different API endpoints: domain search, email search, verification, and 
   counting the number of emails.
3. To store query results, a local SQLite database is utilized. The result of each query is saved as a separate record 
   in the database for later viewing and analysis.
4. A text-based menu is implemented for user interaction with the application:
   - Selecting the type of API request
   - Inputting necessary parameters
   - Displaying the query results
   - Viewing saved results by ID or email
   - Deleting results
5. The application integrates with the Hunter.io API using the Requests library.
6. Basic practices such as logging, error handling, and retry mechanisms have been implemented.

In summary, a simple console application has been created for checking and analyzing emails through the Hunter.io service.

**Project Structure:**
```bash
hunter_check_mail/                      # Root directory of the project
│
├── app.py                              # Main application file
│                                       # (Your main file, likely containing the entry point to the application)
│      
├── README.md                           # Project description file                           
│                                       # (Your project description and instructions for usage)
│     
├── requirements.txt                    # File listing project dependencies. This file can be used 
│                                       # to install necessary libraries using pip install -r requirements.txt.      
├── setup.py                            # File for packaging the project into a distribution (e.g., tar.gz) and its                             
│                                       # distribution.
│         
├── MANIFEST.in                         # File for including or excluding files when creating a distribution   
│         
├── dist/                               # Directory for storing packaged distributions
│   └── hunter_check_mail-0.2.tar.gz    # Represents a packaged distribution of the project in tar.gz format.      
│ 
├── hunter_check_mail.egg-info/         # Directory with package information (metadata such as version, author, etc.)
│    
├── venv/                               # Directory with the Python virtual environment
│     
├── api_clients/                        # Package for modules related to API clients
│   ├── __init__.py                     # Empty file indicating that this is a Python package
│   ├── base_client.py                  # Base class for API clients
│   ├── hunter_client_factory.py        # Factory for creating instances of Hunter clients
│   ├── client_domain_search.py         # Module for searching domain information
│   ├── client_email_finder.py          # Module for finding email addresses
│   ├── client_email_verifier.py        # Module for verifying email addresses    
│   ├── client_email_count.py           # Module for obtaining information about the number of email accounts
│   └── client_account_information.py   # Module for obtaining information about an account
│                               
├── menu/                               # Package for modules related to menus
│   ├── __init__.py                     # Empty file indicating that this is a Python package
│   ├── main_menu.py                    # Module for the main menu
│   └── request_menu.py                 # Module for request menus
│
├── data_base/                          # Package for modules related to the database
│   ├── __init__.py                     # Empty file indicating that this is a Python package
│   └── data_base_service.py            # Module for working with the database
│
├── utils/                              # Package for utility modules
│   ├── __init__.py                     # Empty file indicating that this is a Python package
│   ├── config.py                       # Module for configuration settings
│   ├── logger.py                       # Module for configuring and using the logger
│   ├── DB/                             # Directory for storing the database
│   │   └── my_database.db              # SQLite database file
│   ├── LOG/                            # Directory for storing logs
│   │   └── logs.txt                    # Application log file
```






*Задание:*
Выберете любой сервис и сделайте для него клиент, 2-3 ендпоинта будет достаточно + добавить сервис, который принимает 
какие-то значения и сохраняет результаты, сохранять можно просто в локальную переменную.

Как пример:
https://hunter.io/api-documentation/v2
Реализовать в клиенте отправку запроса на проверку и верификацию е-мейла.
И добавить сервис проверки е-мейла + CRUD для результатов, для хранилища можно использовать переменную. Выложить на 
github, оформить пакетом.

Типизация обязательна.
Пользоваться вот этим линтером: https://github.com/wemake-services/wemake-python-styleguide
setup.cfg https://gist.github.com/dfirst/0957711a40d640d335e128eec4c17f21

*Решение:*

Краткое описание решения для проверки и верификации электронной почты с использованием API Hunter.io:
1. Реализован базовый клиент для отправки HTTP-запросов к API Hunter.io. Он включает в себя логику аутентификации, 
   обработки ошибок, повторных запросов и т.д.
2. Созданы отдельные клиенты для разных эндпоинтов API: поиск по домену, поиск электронной почты, верификация и подсчет 
   количества электронной почты.
3. Для сохранения результатов запросов используется локальная БД SQLite. Результат каждого запроса сохраняется в БД в 
   виде отдельной записи для последующего просмотра и анализа.
4. Реализовано текстовое меню для взаимодействия пользователя с приложением:
    - Выбор типа запроса к API
    - Ввод необходимых параметров
    - Отображение результата запроса
    - Просмотр сохраненных результатов по ID или электронной почте
    - Удаление результатов
5. Приложение интегрируется с API Hunter.io при помощи библиотеки Requests.
6. Используются базовые практики: логгирование, обработка ошибок, повторные запросы.

В целом получилось простое консольное приложение для проверки и анализа электронной почты через сторонний сервис 
Hunter.io.

**Структура проекта:**
```bash
hunter_check_mail/                      # Корневая директория проекта
│
├── app.py                              # Основной файл приложения
│      
├── README.md                           # Файл с описанием проекта                           
│     
├── requirements.txt                    # Файл, в котором перечислены зависимости проекта. Этот файл можно использовать 
│                                       # для установки необходимых библиотек с помощью pip install -r requirements.txt.      
├── setup.py                            # Файл для упаковки проекта в дистрибутив (например, в формате tar.gz) и его                             
│                                       # распространения.         
├── MANIFEST.in                         # Файл для включения или исключения файлов при создании дистрибутива   
│         
├── dist/                               # Директория для хранения упакованных дистрибутивов
│   └── hunter_check_mail-0.2.tar.gz    # Представляет собой упакованный дистрибутив проекта в формате tar.gz.      
│ 
├── hunter_check_mail.egg-info/         # Директория с информацией о пакете (метаданные, такие как версия, автор и др.)
│    
├── venv/                               # Директория с виртуальным окружением Python
│     
├── api_clients/                        # Пакет для модулей, связанных с API-клиентами
│   ├── __init__.py                     # Пустой файл, указывающий, что это Python-пакет
│   ├── base_client.py                  # Базовый класс API-клиента
│   ├── hunter_client_factory.py        # Фабрика для создания экземпляров Hunter-клиентов
│   ├── client_domain_search.py         # Модуль для поиска информации о домене
│   ├── client_email_finder.py          # Модуль для поиска электронной почты
│   ├── client_email_verifier.py        # Модуль для проверки электронной почты    
│   ├── client_email_count.py           # Модуль для получения информации о количестве электронных ящиков
│   └── client_account_information.py   # Модуль для получения информации об аккаунте
│                               
├── menu/                               # Пакет для модулей, связанных с меню
│   ├── __init__.py                     # Пустой файл, указывающий, что это Python-пакет
│   ├── main_menu.py                    # Модуль для основного меню
│   └── request_menu.py                 # Модуль для меню запросов
│
├── data_base/                          # Пакет для модулей, связанных с базой данных
│   ├── __init__.py                     # Пустой файл, указывающий, что это Python-пакет
│   └── data_base_service.py            # Модуль для работы с базой данных
│
├── utils/                              # Пакет для утилитарных модулей
│   ├── __init__.py                     # Пустой файл, указывающий, что это Python-пакет
│   ├── config.py                       # Модуль для конфигурационных настроек
│   ├── logger.py                       # Модуль для настройки и использования логгера
│   ├── DB/                             # Директория для хранения базы данных
│   │   └── my_database.db              # Файл базы данных SQLite
│   ├── LOG/                            # Директория для хранения логов
│   │   └── logs.txt                    # Файл логов приложения
```
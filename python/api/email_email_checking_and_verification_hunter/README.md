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
"email_email_checking_and_verification_hunter" is a console application for checking and verifying email addresses using
the Hunter API.

Project workflow:
- The user enters the Hunter API key in the main program (main.py).
- The program initializes a Hunter client object (HunterClient) with the provided API key.
- The main loop of the program presents a text menu (Menu) to the user with options for performing operations such as 
  domain search, email search, email verification, and others.
- The results of operations are saved locally using the local storage service (LocalStorageService).
- Appropriate messages are displayed in case of errors or exceptions, and the program continues to run.

Packaging and distribution:
The project supports packaging in the tar.gz format for further installation via pip.
It provides a requirements.txt file with dependencies for installing necessary packages.
The project offers a simple interface for using the Hunter API functionality, and the code structure is divided into 
modules for readability and maintainability.

This page provides information about the version, project description, metadata, and other details of your package, 
along with a link for installation via pip.
https://pypi.org/project/email-email-checking-and-verification-hunter/0.1/

**Project Structure:**
```bash
email_email_checking_and_verification_hunter/   # Main project folder.
│
├── config.py                 # Module for storing configuration parameters, such as console colors.
│ 
│      
├── hunter_client.py          # Module containing the HunterClient class, which provides an interface for interacting
│                             # with the Hunter API, including methods for domain search, email search, and others.
│                               
├── local_storage_service.py  # Module where the LocalStorageService class is defined, providing a service for 
│                             # saving and retrieving verification results in local storage.
│                               
├── logger.py                 # Module where the Logger class is defined for logging events and errors in the application.
│
│
├── main.py                   # Main file containing the entry point of the application (main()), which initializes 
│                             # objects, sets the API key, and launches the main menu.
│
├── menu.py                   # Module where the Menu class is defined, providing an interface for interacting with the
│                             # user through the console. Contains methods for displaying the menu and handling user
│                             # choices.
├── README.md                 # File containing the project description, installation, running, and usage instructions.
│
│
├── request_manager.py        # Module containing the RequestManager class, which provides the make_request method for 
│                             # performing HTTP requests with error handling.
│
├── requirements.txt          # File listing project dependencies. This file can be used to install the required  
│                             # libraries using pip install -r requirements.txt.
│
├── setup.py                  # File for packaging the project into a distribution (e.g., tar.gz) and its distribution.
│
│
├── utils.py                  # Module providing functions and utilities for processing verification results and 
│                             # displaying data nicely in the console.
│
├── email_email_checking_and_verification_hunter.egg-info/  # Directory created during package installation via setup.py, 
│                                                           # containing metadata about the package.  
│
├── dist/
│   └── email_email_checking_and_verification_hunter-0.1.tar.gz  # Represents a packaged distribution of the project in 
│                                                                # tar.gz format.
```
**Installation:**
You can use the following command in the command line:

```bash
pip install email_email_checking_and_verification_hunter-0.1.tar.gz
```
This command will install the package specified in the archive in your Python environment. After installation, you can 
import modules from this project into your code and use their functionality.




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
"email_email_checking_and_verification_hunter", представляет собой консольное приложение для проверки и верификации 
электронных адресов с использованием Hunter API.

Описание работы проекта:
- Пользователь вводит API-ключ Hunter в основной программе (main.py).
- Программа инициализирует объект клиента Hunter (HunterClient) с предоставленным API-ключом.
- Основной цикл программы предоставляет пользователю текстовое меню (Menu) с опциями для выполнения операций, таких как 
  поиск домена, поиск электронного адреса, верификация электронного адреса и другие.
- Результаты операций сохраняются локально с использованием сервиса локального хранения (LocalStorageService).
- При возникновении ошибок или исключений выводятся соответствующие сообщения, а программа продолжает работу.

Упаковка и распространение:
Проект поддерживает упаковку в формате tar.gz для дальнейшей установки через pip.
Предоставляет файл requirements.txt с зависимостями для установки необходимых пакетов.
Проект предоставляет простой интерфейс для использования функционала Hunter API, а структура кода разделена на модули, 
что способствует его читаемости и сопровождаемости.

Эта страница предоставляет информацию о версии, описании проекта, метаданных и других деталях моего пакета, а также 
ссылку для установки через pip.
https://pypi.org/project/email-email-checking-and-verification-hunter/0.1/

**Структура проекта:**
```bash
email_email_checking_and_verification_hunter/   # Основна папка проекту.
│
├── config.py                 # Модуль для хранения конфигурационных параметров, в нашем случае такие  как цвета консоли   
│ 
│      
├── hunter_client.py          # Модуль, содержащий класс HunterClient, который предоставляет интерфейс для 
│                             # взаимодействия с API Hunter, включая методы для поиска доменов, поиска email и других.
│                               
├── local_storage_service.py  # Модуль, в котором определен класс LocalStorageService, предоставляющий сервис для 
│                             # сохранения и получения результатов верификации в локальном хранилище.
│                               
├── logger.py                 # Модуль, в котором определен класс Logger для логирования событий и ошибок в приложении.
│
│
├── main.py                   # Основной файл, содержащий точку входа в приложение (main()), который инициализирует 
│                             # объекты, устанавливает API-ключ, и запускает главное меню.
│
├── menu.py                   # Модуль, в котором определен класс Menu, предоставляющий интерфейс для взаимодействия с 
│                             # пользователем через консоль. Содержит методы для отображения меню и обработки выбора 
│                             # пользователя.
├── README.md                 # Файл, содержащий описание проекта, инструкции по установке, запуску и использованию.
│
│
├── request_manager.py        # Модуль, содержащий класс RequestManager, который предоставляет метод make_request для 
│                             # выполнения HTTP-запросов с обработкой ошибок.
│
├── requirements.txt          # Файл, в котором перечислены зависимости проекта. Этот файл можно использовать для 
│                             # установки необходимых библиотек с помощью pip install -r requirements.txt.
│
├── setup.py                  # Файл для упаковки проекта в дистрибутив (например, в формате tar.gz) и его 
│                             # распространения.
│
├── utils.py                  # Модуль, предоставляющий функции и утилиты для обработки результатов верификации и 
│                             # красивого вывода данных в консоль.
│
├── email_email_checking_and_verification_hunter.egg-info/  # Директория, создаваемая при установке пакета через 
│                                                           # setup.py, содержащая метаданные о пакете.  
│
├── dist/
│   └── email_email_checking_and_verification_hunter-0.1.tar.gz  # Представляет собой упакованный дистрибутив проекта в 
│                                                                # формате tar.gz.
```
**Установка:**
Вы можете использовать следующую команду в командной строке:
```bash
pip install email_email_checking_and_verification_hunter-0.1.tar.gz
```
Данная команда установит пакет, указанный в архиве, в вашем окружении Python. После установки вы сможете импортировать 
модули из этого проекта в своем коде и использовать их функционал.
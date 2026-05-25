# Telegram and Planfix Integration Project

## Project Overview:

This project aims to integrate the Telegram messenger with the project and task management system, Planfix.

### Main Objective:
Facilitate bidirectional message exchange between Telegram users and the Planfix system for convenient task management.

### Project Specifics:
- Utilizes the Python Telethon library for Telegram API interactions.
- Implements the Flask framework with asynchronous support for the web component.
- Converts the WSGI Flask application to ASGI using the asgiref library.
- Application deployment is done using the uvicorn server.

### Project Functionality:
- Telegram user registration in the Planfix system.
- Sending messages from Telegram to Planfix as new tasks.
- Sending notifications about new tasks and comments on tasks from Planfix to Telegram.

### User Identification Data:
- Phone number
- Telegram username
- Unique chat ID

### Advantages:
- Convenient task management in Planfix through the familiar Telegram interface.
- Quick communication among team members regarding tasks through Telegram.
- Instant notifications in Telegram about new tasks and comments in Planfix.

## Project Structure:

  ```bash
  telegram_planfix_integration/       # Main project folder
  ├── config.py                       # Configuration and environment variable file
  ├── logger.py                       # Logging configuration
  ├── main.py                         # Application startup
  ├── README.md                       # Project description
  ├── requirements.txt                # Project dependencies
  ├── docs/
      └── ТЗ.pdf                      # Technical specification
  ```

In essence, this solution enhances task and project management efficiency by integrating a popular messenger into the 
corporate task management system.

### Integration Approach:
In this article, a method for using the Telethon library to interact with the Telegram API in a Flask web application is
found.

### Key Points:
- Flask operates on the WSGI standard, while Telethon supports only asynchronous ASGI servers. Hence, an asynchronous 
  version of Flask with ASGI support needs to be installed.
- The asgiref library is used to convert WSGI to ASGI. A Flask application instance is created, converted to ASGI using 
  the WsgiToAsgi function.
- The resulting ASGI application is launched using an asynchronous web server, such as hypercorn or uvicorn.
- The standard procedure follows - importing Telethon, creating a client, defining event handlers.
- The outcome is a hybrid solution, incorporating asynchronous Telethon functions into a Flask web application through \
  conversion and the use of asynchronous servers.

This enables the utilization of Telethon in synchronous WSGI frameworks like Flask.




# Это проект по интеграции мессенджера Telegram с системой управления проектами и задачами Planfix.

## Основная задача, которую решает этот проект - наладить двусторонний обмен сообщениями между пользователями Telegram и 
## системой Planfix для удобства работы с задачами.

### Специфика проекта заключается в следующем:
- Используется Python библиотека Telethon для работы с API Telegram
- Для веб-части используется фреймворк Flask с поддержкой асинхронности
- Преобразование WSGI-приложения Flask в ASGI с помощью библиотеки asgiref
- Запуск приложения осуществляется с помощью сервера uvicorn

### Функционал проекта:
- Регистрация пользователя Telegram в системе Planfix
- Отправка сообщений из Telegram в Planfix как новые задачи
- Отправка уведомлений о новых задачах и комментариях к задачам из Planfix в Telegram

### Для идентификации пользователей используются такие данные:
- Номер телефона
- Имя пользователя Telegram
- Уникальный ID чата

### Преимущества:
- Удобство работы с задачами в Planfix через привычный Telegram интерфейс
- Быстрая коммуникация между сотрудниками по задачам через Telegram
- Моментальные уведомления в Telegram о новых задачах и комментариях в Planfix

## Структура проекта:
  ```bash
  telegram_planfix_integration/       # Основна папка проекта
  ├── config.py                       # Файл с конфигурацией и переменными окружения
  ├── logger.py                       # Настройка логирования  
  ├── main.py                         # Запуск приложения
  ├── README.md                       # Описание проекта
  ├── requirements.txt                # Зависимости проекта   
  ├── docs/
      └── ТЗ.pdf                      # Техническое задание
  ```

В целом, данное решение позволяет сделать работу с задачами и проектами более эффективной и мобильной за счет интеграции
популярного мессенджера в корпоративную систему управления задачами.

## В этой статьи (https://www.cloudkp.com/2023/02/how-to-run-telethon-in-flask-site.html) нашел способ использования 
## библиотеки Telethon для работы с Telegram API в веб-приложении на Flask.

### Основные моменты:
- Flask работает по стандарту WSGI, а Telethon поддерживает только асинхронные серверы ASGI. Поэтому нужно установить 
  асинхронную версию Flask с поддержкой ASGI.
- Для преобразования WSGI в ASGI используется библиотека asgiref. Создается экземпляр приложения Flask, конвертируется в
  ASGI при помощи функции WsgiToAsgi.
- Запуск полученного ASGI-приложения происходит с помощью асинхронного веб-сервера, например hypercorn или uvicorn.
- Далее идет стандартная работа - импорт Telethon, создание клиента, обработчики событий.
- В итоге получается гибридное решение - асинхронные функции Telethon в веб-приложении Flask за счет конвертации и 
  использования асинхронных серверов.
Таким образом реализуется возможность использовать Telethon в синхронных WSGI-фреймворках вроде Flask.



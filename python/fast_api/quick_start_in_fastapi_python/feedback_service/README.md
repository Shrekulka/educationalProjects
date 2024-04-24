# Task:
Extend the existing FastAPI application by creating a POST endpoint that allows users to submit feedback.
The endpoint should accept JSON data containing the user's name and feedback message.

1. Define a Pydantic model named "Feedback" with the following fields:
   - `name` (str)
   - `message` (str)
2. Create a new POST route "/feedback" that accepts JSON data according to the `Feedback` model.
3. Implement a function to handle incoming feedback data and respond with a success message.
4. Store the feedback data in a list or data store to track all received feedback.
   Example:
   JSON Request:
   ```bash
   {
       "name": "Alice",
       "message": "Great course! I'm learning a lot."
   }
   ```
   JSON Response:
   ```bash
   {
    "message": "Feedback received. Thank you, Alice!"
   }
   ```
Please test your implementation using tools such as "curl", Postman, or any other API client to submit feedback and 
verify the response.

## Solution Description:
In the models.py file, a Pydantic model named Feedback was defined to describe the data structure for storing feedback 
information, including the user's name and message.
In the main.py file, a function create_app() was created, which creates a FastAPI instance and sets up routes to handle
requests. This function includes routes to get feedback and add new feedback. 
Feedback data is stored in a list to track all received feedback.

## Steps to test our application using Postman:

### POST Verification Algorithm:
1. Start your FastAPI application.
2. Open Postman and create a new request.
3. Set the request type to POST.
4. Enter the URL of your route /feedback, for example, http://127.0.0.1:5080/feedback.
5. Select the Body tab, then select raw, and ensure that JSON format is selected.
6. In the request body, enter JSON data representing feedback, for example:
   ```bash
   {
       "name": "Alice",
       "message": "Great course! I'm learning a lot."
   }
   ```
7. Click the "Send" button.
8. You should receive a JSON response from your application confirming receipt of the feedback, for example:
9. This is how you can add data to our database.

### GET Verification Algorithm:
1. Set the request type to GET.
2. Enter the URL of your route /feedback, for example:
   ```bash
   http://127.0.0.1:5080/feedback
   ```
3. Click the "Send" button.
4. You should receive a JSON response from your application containing a list of all feedback stored in the database.
Example response:
   ```bash
   [
       {
           "name": "Alice",
           "message": "Great course! I'm learning a lot."
       },
       {
           "name": "Bob",
           "message": "Excellent material! Very informative."
       },
       ...
   ]
   ```
## Project Structure:
```bash
📁 feedback_service/              # Root directory of the entire project
│
├── README.md                     # Project description file
│
├── requirements.txt              # File listing project dependencies
│
└── 📁 src/                       # Main directory containing the application source code
    │
    ├── logger_config.py          # Module for configuring logging
    │
    ├── main.py                   # Main module containing the FastAPI application code
    │
    └── models.py                 # Module containing the Pydantic model for feedback
```





# Задание:
Расширьте существующее приложение FastAPI, создав конечную точку POST, которая позволяет пользователям отправлять отзывы.
Конечная точка должна принимать данные JSON, содержащие имя пользователя и сообщение обратной связи.

1. Определите Pydantic модель с именем "Feedback" (обратная связь) со следующими полями:
   - `name` (str)
   - `message` (str)
2. Создайте новый маршрут публикации "/feedback", который принимает данные JSON в соответствии с моделью `Feedback`.
3. Реализуйте функцию для обработки входящих данных обратной связи и ответа сообщением об успешном завершении.
4. Сохраните данные обратной связи в списке или хранилище данных, чтобы отслеживать все полученные отзывы.
   Пример:
   Запрос JSON:
   ```bash
   {
       "name": "Alice",
       "message": "Great course! I'm learning a lot."
   }
   ```
   Ответ JSON:
   ```bash
   {
       "message": "Feedback received. Thank you, Alice!"
   }
   ```
Пожалуйста, протестируйте свою реализацию с помощью таких инструментов, как "curl", Postman или любой другой клиент API,
чтобы отправить отзыв и проверить ответ

## Описание решения:

В файле models.py была определена Pydantic модель Feedback, которая описывает структуру данных для хранения информации 
об отзыве, включая имя пользователя и текст сообщения.

В файле main.py была создана функция create_app(), которая создает экземпляр FastAPI и настраивает маршруты для 
обработки запросов. Эта функция включает маршруты для получения отзывов и добавления нового отзыва. 
Данные обратной связи сохраняются в списке для отслеживания всех полученных отзывов.


## Шаги для тестирования нашего приложения через Postman:

### Алгоритм проверки "POST": 
1. Запустите ваше приложение FastAPI.
2. Откройте Postman и создайте новый запрос.
3. Укажите тип запроса как POST.
4. Введите URL вашего маршрута /feedback, например, http://127.0.0.1:5080/feedback.
5. Выберите вкладку Body, затем выберите raw, и убедитесь, что выбран формат JSON.
6. В теле запроса введите JSON-данные, представляющие отзыв, например:
    ```bash
    {
        "name": "Alice",
        "message": "Great course! I'm learning a lot."
    }
    ```
7. Нажмите кнопку "Send" (Отправить).

8. Вы должны получить ответ от вашего приложения в формате JSON, подтверждающий получение отзыва, например:
    ```bash
    {
        "message": "Feedback received. Thank you, Alice!"
    }
    ```
9. Так можно добавлять данные в нашу базу данных.

## Алгоритм проверки "GET": 
1. Укажите тип запроса как GET.
2. Введите URL вашего маршрута /feedback, например:
    ```bash
    http://127.0.0.1:5080/feedback
    ```
3. Нажмите кнопку "Send" (Отправить).
4. Вы должны получить ответ от вашего приложения в формате JSON, содержащий список всех отзывов, сохраненных в 
   базе данных. Пример ответа:
    ```bash
    [
        {
            "name": "Alice",
            "message": "Great course! I'm learning a lot."
        },
        {
            "name": "Bob",
            "message": "Excellent material! Very informative."
        },
        ...
    ]
    ``` 
   
## Структура проекта:
```bash
📁 feedback_service/              # Корневая директория всего проекта
│
├── README.md                     # Файл с описанием проекта
│
├── requirements.txt              # Файл с перечнем зависимостей проекта
│
└── 📁 src/                       # Основная директория с исходным кодом приложения
    │
    ├── logger_config.py          # Модуль для настройки логирования
    │
    ├── main.py                   # Основной модуль, содержащий код FastAPI приложения
    │
    └── models.py                 # Модуль, содержащий Pydantic модель для отзыва
```
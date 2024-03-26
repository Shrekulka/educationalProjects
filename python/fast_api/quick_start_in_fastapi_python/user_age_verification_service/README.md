# Task:

Your task is to extend the existing FastAPI application by adding a new POST endpoint that accepts JSON data 
representing a user and returns the same data with an additional field indicating whether the user is an adult or not.
1. Define a Pydantic model named "User" with the following fields:
   - `name` (str)
   - `age` (int)
2. Create a new route `/user`, which accepts POST requests and takes JSON payload containing user data matching the 
   `User` model.
3. Implement a function to check whether the user is an adult (age >= 18) or a minor (age < 18).
4. Return the user data along with an additional field `is_adult` in the JSON response, indicating whether the user is 
   an adult (True) or a minor (False).
    #### Example:
    JSON request:
    ```bash
    {
        "name": "John Doe",
        "age": 25
    }
    ```
    #### JSON response:
    ```bash
    {
        "name": "John Doe",
        "age": 25,
        "is_adult": true
    }
    ```
Please test your implementation using tools such as "curl", Postman, or any other API client.


# Solution:

## Your solution consists of the following parts:

1. Definition of the Pydantic model "User":
   In the models.py file, we defined the Pydantic model User.
   This model has three fields: name (string), age (integer), and is_adult (boolean type, default False).
2. Creating a new route /user for POST requests:
   In the main.py file, we added a new route /user to handle POST requests with user data.
   This function accepts user data in JSON format, matching the User model.
3. Implementing the user adulthood check:
   Inside the create_user function, we implemented logic to determine whether the user is an adult or a minor:
    ```bash
    is_adult: bool = user_data.age >= 18
    
    # Assign the obtained is_adult value to a new field of the user_data object named is_adult
    user_data.is_adult = is_adult
    ```
   If the user's age (user_data.age) is greater than or equal to 18, then the variable is_adult will have a value of 
   True; otherwise, it will be False. Then this value is assigned to the is_adult field of the user_data object.
4. Returning user data with an additional is_adult field:
   On the server side, the create_user function returns the updated user_data object in JSON format as a response, 
   including the is_adult field with a value of True or False.
   Finally, the create_user function returns the updated user_data object in JSON format as a response:
    ```bash
    return user_data
    ```
   Thus, the response will contain all fields, including the new is_adult field indicating whether the user is an adult
   or a minor.
5. Handling the response on the client and formatting the output:
   The following logic is executed in the JavaScript code on the client side:
    ```bash
    .then(data => {
        // Check if the is_adult property exists in the data object
        const isAdult = data.hasOwnProperty('is_adult') ? (data.is_adult ? 'Adult' : 'Minor') : 'Status unknown';
    
        // Update the content of the result container
        document.getElementById('result').innerHTML = `User Data: <br> Name: ${data.name}, Age: ${data.age}, ${isAdult}`;
    })
    ```
   Here, we check the presence of the is_adult property in the server response. If the property is present, its value 
   (true or false) is used to assign the corresponding string ("Adult" or "Minor") to the isAdult variable. If the 
   is_adult property is absent, the isAdult variable is assigned the string "Status unknown". Then this string (isAdult) 
   is displayed in the result container along with the user's name and age.
   ### Example of request and response:
   #### Request (in JSON format):
    ```bash
    {
        "name": "John Doe",
        "age": 25
    }
    ```
    #### Server response (in JSON format):
    ```bash
    {
        "name": "John Doe",
        "age": 25,
        "is_adult": true
    }
    ```
    #### Output on the client:
    
    ```bash
    User Data:
    Name: John Doe, Age: 25, Adult
    ```
   Thus, on the server side, we return the is_adult value as true or false, and on the client side, we format this value
   into a more understandable text ("Adult" or "Minor") before displaying it.

## Project Structure:
```bash
📁 fastapi_project_skeleton/   # Root directory of the entire project
│
│
├── 📁 src/                    # Main directory with the source code of the application
│   │
│   ├── logger_config.py       # Logger configuration.
│   │ 
│   ├── main.py                # Main script to run the application.
│   │ 
│   └── models.py              # File with global models
│
├── README.md                  # File with project description.
│
└── requirements.txt           # File with project dependencies.
```
Educational material on Stepik - https://stepik.org/course/179694/syllabus






# Задание:

Ваша задача состоит в том, чтобы расширить существующее приложение FastAPI, добавив новую конечную точку POST, которая
принимает данные JSON, представляющие пользователя, и возвращает те же данные с дополнительным полем, указывающим, 
является ли пользователь взрослым или нет.

1. Определите Pydantic модель с именем "Пользователь" ("User") со следующими полями:
   - `name` (str)
   - `age` (int
2. Создайте новый маршрут `/user`, который принимает запросы POST и принимает полезную нагрузку JSON, содержащую 
   пользовательские данные, соответствующие модели `User`.
3. Реализуйте функцию для проверки того, является ли пользователь взрослым (возраст >= 18) или несовершеннолетним 
   (возраст < 18).
4. Верните пользовательские данные вместе с дополнительным полем `is_adult` в ответе JSON, указывающим, является ли 
   пользователь взрослым (True) или несовершеннолетним (False).

#### Пример:
Запрос в формате JSON:
```bash
{
    "name": "John Doe",
    "age": 25
}
```
#### Ответ в формате JSON:
```bash
{
    "name": "John Doe",
    "age": 25,
    "is_adult": true
}
```
Пожалуйста, протестируйте свою реализацию с помощью таких инструментов, как "curl", Postman или любой другой клиент API.


# Решение:

## Ваше состоит из следующих частей:
1. Определение Pydantic модели "User":
   В файле *models.py* мы определили Pydantic модель User.
   Эта модель имеет три поля: name (строка), age (целое число) и is_adult (логический тип, по умолчанию False).
2. Создание нового маршрута /user для POST-запросов:
   В файле *main.py* мы добавили новый маршрут /user для обработки POST-запросов с пользовательскими данными.
   Эта функция принимает данные пользователя в формате JSON, соответствующие модели User.
3. Реализация проверки совершеннолетия пользователя:
   Внутри функции create_user мы реализовали логику для определения, является ли пользователь взрослым или 
   несовершеннолетним:
    ```bash
    is_adult: bool = user_data.age >= 18
    
    # Присваиваем полученное значение is_adult новому полю объекта user_data с именем is_adult
    user_data.is_adult = is_adult
    ```
   Если возраст пользователя (user_data.age) больше или равен 18, то переменная is_adult будет иметь значение True, в 
   противном случае - False. Затем это значение присваивается полю is_adult объекта user_data.
4. Возврат данных пользователя с дополнительным полем is_adult: 
   На стороне сервера функция create_user возвращает обновленный объект user_data в формате JSON в качестве ответа, 
   включая поле is_adult со значением True или False.
   Наконец, функция create_user возвращает обновленный объект user_data в формате JSON в качестве ответа:
    ```bash
    return user_data
    ```
   Таким образом, ответ будет содержать все поля, включая новое поле is_adult, указывающее, является ли пользователь 
   взрослым или несовершеннолетним.

   5. Обработка ответа на клиенте и форматирование вывода: 
      В JavaScript-коде на клиентской стороне выполняется следующая логика:
       ```bash
       .then(data => {
           // Проверяем наличие свойства is_adult в объекте data
           const isAdult = data.hasOwnProperty('is_adult') ? (data.is_adult ? 'Взрослый' : 'Еще малек') : 'Статус неизвестен';
    
           // Обновляем содержимое контейнера с результатом
           document.getElementById('result').innerHTML = `Данные пользователя: <br> Имя: ${data.name}, Возраст: ${data.age}, ${isAdult}`;
       })
       ```
      Здесь выполняется проверка наличия свойства is_adult в ответе сервера. Если свойство присутствует, то его значение 
      (true или false) используется для присвоения соответствующей строки ("Взрослый" или "Еще малек") переменной isAdult. 
      Если свойство is_adult отсутствует, то переменной isAdult присваивается строка "False". Затем эта строка (isAdult) 
      выводится в контейнере с результатом вместе с именем и возрастом пользователя.
   ### Пример запроса и ответа:
   #### Запрос (в формате JSON):
    ```bash
    {
        "name": "John Doe",
        "age": 25
    }
    ```
    #### Ответ сервера (в формате JSON):
    ```bash
    {
        "name": "John Doe",
        "age": 25,
        "is_adult": true
    }
    ```
    #### Вывод на клиенте:
    ```bash
    Данные пользователя:
    Имя: John Doe, Возраст: 25, Взрослый
    ```
Таким образом, на стороне сервера мы возвращаем значение is_adult как true или false, а на стороне клиента мы 
форматируем это значение в более понятный текст ("Взрослый" или "Еще малек") перед выводом.


## Структура проекта:
```bash
📁 fastapi_project_skeleton/   # Корневая директория всего проекта
│
│
├── 📁 src/                    # Основная директория с исходным кодом приложения
│   │
│   ├── logger_config.py       # Конфигурация логгера.
│   │ 
│   ├── main.py                # Основной скрипт для запуска приложения.
│   │ 
│   └── models.py              # Файл с глобальными моделями
│
├── README.md                  # Файл с описанием проекта.
│
└── requirements.txt           # Файл с зависимостями проекта.   
```
Учебный материал на Stepik - https://stepik.org/course/179694/syllabus
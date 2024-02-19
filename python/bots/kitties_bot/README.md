# This code is an example of a simple Telegram bot that retrieves a random animal image from various APIs and sends it 
# to users.

## Key components of the code:
 - get_animal_link: Function to make a GET request to the API and retrieve a link to a photo with an animal. Returns the
   photo link or None in case of an error.
 - handle_empty_response: Function to handle the situation when the image is not found. Outputs a warning to the log.
 - log_error: Function for logging errors in requests.
 - send_animal_photo: Function to send a photo to the user in the chat. Uses requests.get to make a GET request to the 
   Telegram Bot API.
 - send_error_message: Function to send an error message to the user in the chat. Uses requests.get to send a text 
   message.
 - main: The main function of the program representing the loop of receiving updates and sending photos. Uses getUpdates 
   to receive updates and calls the process_updates function to handle them.
 - process_updates: Function to process a list of updates. For each update, a random API is selected to retrieve a photo,
   and then get_animal_link is called to obtain the photo link. If the link is obtained successfully, send_animal_photo 
   is called; otherwise, send_error_message is called.

Please note that the bot is limited by the maximum number of attempts (MAX_ATTEMPTS), which is useful for testing and
prevents an infinite loop.

Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Данный код представляет собой пример простого телеграм-бота, который получает случайное изображение животного от 
# различных API и отправляет его пользователям.

## Основные компоненты кода:
 - get_animal_link: Функция для выполнения GET-запроса к API и получения ссылки на фото с животным. Возвращает ссылку
   на фото или None в случае ошибки.
 - handle_empty_response: Функция для обработки ситуации, когда изображение не найдено. Выводит предупреждение в лог.
 - log_error: Функция для логирования ошибок в запросах.
 - send_animal_photo: Функция для отправки фото пользователю в чате. Использует requests.get для выполнения GET-
   запроса к Telegram Bot API.
 - send_error_message: Функция для отправки сообщения об ошибке пользователю в чате. Использует requests.get для 
   отправки текстового сообщения.
 - main: Основная функция программы, представляющая цикл получения обновлений и отправки фото. Использует getUpdates 
   для получения обновлений и вызывает функцию process_updates для их обработки.
 - process_updates: Функция для обработки списка обновлений. Для каждого обновления выбирается случайный API для 
   получения фото, и затем вызывается get_animal_link для получения ссылки на фото. Если ссылка получена успешно, 
   вызывается send_animal_photo, иначе вызывается send_error_message.

Обратите внимание, что бот ограничен максимальным количеством попыток (MAX_ATTEMPTS), что полезно при тестировании и 
предотвращает бесконечный цикл.

Учебный материал на Stepik - https://stepik.org/course/120924/syllabus

# kitties_bot/requests_via_requests/direct_requests_via_requests.py
import random
import time
import traceback
from typing import Optional, Dict, List, Union

import requests

from config import API_URL, BOT_TOKEN, ERROR_TEXT, ANIMALS, DELAY_BETWEEN_REQUESTS, MAX_ATTEMPTS
from logger import logger


# Функция для получения ссылки на фото с животным
def get_animal_link(api_url: str, session: requests.Session) -> Optional[str]:
    """
        Function to retrieve a link to a photo with an animal from the specified API.

        :param api_url: API URL for retrieving the photo
        :param session: Session object for making requests
        :return: Link to the photo with the animal
    """
    try:
        # Выполнение GET-запроса к API
        response = session.get(api_url)
        # Проверка наличия ошибок при выполнении запроса
        response.raise_for_status()
    except requests.RequestException as error:
        log_error(error)
        return None

    # Если запрос успешен
    if response.status_code == 200:
        # Разбор JSON-ответа
        data = response.json()

        # Если ответ представляет собой словарь
        if isinstance(data, dict):
            for key in ['url', 'image', 'fileSizeBytes']:
                # Если в словаре есть ключ 'url', 'image' или 'fileSizeBytes'
                if key in data:
                    logger.info(f'Successfully obtained a link to the photo with an animal from {api_url}')
                    return data[key]

        # Если ответ представляет собой список
        elif isinstance(data, list):
            # Если список не пуст и в первом элементе есть ключ 'url'
            if data and 'url' in data[0]:
                # Получение данных о животном
                animal_data = data[0]
                logger.info(f'Successfully obtained a link to the photo with an animal from {api_url}')
                return animal_data['url']
        else:
            logger.warning(f'Unexpected response format from {api_url}')
            handle_empty_response(api_url)
    else:
        logger.warning(f'Failed to send the photo. Response code: {response.status_code}')
    return None


# Функция для обработки ситуации, когда изображение не найдено
def handle_empty_response(api_url: str) -> None:
    """
        Function to handle the situation when the image is not found.

        :param api_url: API URL where the image was not found
    """
    logger.warning(f'No images found at {api_url}')


# Функция для логирования ошибки
def log_error(error: Exception) -> None:
    """
        Function for logging an error.

        :param error: Exception representing the request error
    """
    detailed_error_traceback = traceback.format_exc()
    logger.error(f"Request failed: {error}\n{detailed_error_traceback}")


# Функция для отправки фото пользователю в чате
def send_animal_photo(chat_id: int, photo_link: str) -> None:
    """
        Function for sending a photo to a user in a chat.

        :param chat_id: Chat identifier
        :param photo_link: Link to the photo
    """
    try:
        # Выполнение GET-запроса к Telegram Bot API с параметрами chat_id и photo_link
        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto',
                     params={'chat_id': chat_id, 'photo': photo_link}).raise_for_status()
    except requests.RequestException as error:
        logger.error(f"Request failed: {error}")


# Функция для отправки сообщения об ошибке пользователю в чате
def send_error_message(chat_id: int) -> None:
    """
        Function for sending an error message to a user in a chat.

        :param chat_id: Chat identifier
    """
    try:
        # Выполнение GET-запроса для отправки текстового сообщения об ошибке в чат
        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage',
                     params={'chat_id': chat_id, 'text': ERROR_TEXT}).raise_for_status()
    except requests.RequestException as error:
        log_error(error)


# Основная функция программы
def main() -> None:
    """
    Main function of the program for receiving updates and sending photos.

    The main loop of the program where requests are made to receive updates,
    processing the received updates, and sending photos to chats.
    """
    # Инициализация счетчика попыток
    counter = 0

    # Использование сессии для выполнения нескольких запросов
    with requests.Session() as session:
        # Запуск цикла с ограничением по количеству попыток
        while counter < MAX_ATTEMPTS:
            print('attempt =', counter)
            try:
                # Выполнение запроса на получение обновлений
                response = session.get(f'{API_URL}{BOT_TOKEN}/getUpdates')
                # Проверка наличия ошибок при выполнении запроса
                response.raise_for_status()
                # Разбор JSON-ответа
                updates = response.json()
            except requests.RequestException as error:
                logger.error(f"Request failed: {error}")
                continue

            logger.info(f"Updates: {updates}")

            # Обработка полученных обновлений
            process_updates(updates, session)

            # Пауза между запросами
            time.sleep(DELAY_BETWEEN_REQUESTS)
            # Увеличение счетчика попыток
            counter += 1


# Функция для обработки списка обновлений
def process_updates(updates: Dict[str, List[Dict[str, Union[int, Dict[str, Union[int, str]]]]]],
                    session: requests.Session) -> None:
    """
        Function for processing a list of updates.

        :param updates: List of updates
        :param session: Session object for making requests
    """
    # Если есть новые обновления
    if updates['result']:
        logger.info(f'Processing {len(updates["result"])} updates.')
        # Для каждого результата в полученных обновлениях
        for result in updates['result']:
            # Получение идентификатора чата
            chat_id = int(result['message']['from']['id'])

            # Выбор случайного API для получения фото животного
            api_url = random.choice(ANIMALS)

            # Получение ссылки на фото животного
            animal_link = get_animal_link(api_url, session)

            # Если есть ссылка на фото
            if animal_link:
                # Отправка фото в чат
                send_animal_photo(chat_id, animal_link)
            else:
                # Отправка сообщения об ошибке в чат
                send_error_message(chat_id)

    logger.info('Updates processed successfully.')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# non_functional telegram_planfix_integration/app/services/planfix_client.py

import logging
from json.decoder import JSONDecodeError

import requests

from config import Config

print("planfix_client.py")


def get_planfix_user(token):
    """Отримання користувача з Planfix за токеном."""
    try:
        url = f'https://api.planfix.com/user/{token}'
        response = requests.get(url)
        response.raise_for_status()  # Поднимает исключение в случае ошибки HTTP (status_code >= 400)

        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during Planfix API request: {e}")
    except JSONDecodeError as e:
        logging.error(f"Error decoding JSON from Planfix response: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return None


def send_planfix_message(token_planfix, user_id, text):
    """Відправлення повідомлення в Planfix."""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token_planfix}'
        }
        payload = {
            'user_id': user_id,
            'text': text
        }
        response = requests.post(Config.planfix_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Поднимает исключение в случае ошибки HTTP (status_code >= 400)

        if response.status_code == 200:
            logging.info("Сообщение успешно отправлено в Planfix")
            return True
        else:
            logging.warning(
                f"Неудачный запрос в Planfix. Код ответа: {response.status_code}, Текст ответа: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API Planfix: {e}")
        return False
    except Exception as e:
        logging.error(f"Непредвиденная ошибка: {e}")
        return False


def get_planfix_message(token_planfix, limit=10):
    """Отримання всіх нових повідомлень з Planfix."""
    try:
        url = f'https://api.planfix.com/message/{token_planfix}'
        params = {'limit': limit}
        headers = {'Content-Type': 'application/json'}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            messages = response.json()
            return messages
        else:
            logging.warning(
                f"Неудачный запрос к Planfix. Код ответа: {response.status_code}, Текст ответа: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API Planfix: {e}")
        return []
    except Exception as e:
        logging.error(f"Непредвиденная ошибка: {e}")
        return []

# /pythonProject/my_planfix.py
import requests

from config import planfix_api_url, planfix_api_key
from telegram_integration_planfix import send_response_to_telegram

#
# def handle_planfix_response(client_data, planfix_message_id):
#     # Получите ответ из Planfix по идентификатору сообщения
#     response_text = get_planfix_response(planfix_message_id)
#
#     # Отправьте ответ в Telegram
#     send_response_to_telegram(client_data, response_text, client_data)
#
#
# def send_message_to_planfix(client_data, message):
#     headers = {
#         "Authorization": f"Bearer {planfix_api_key}"
#     }
#
#     data = {
#         "client_id": client_data["id"],
#         "message": message
#     }
#
#     response = requests.post(
#         f"{planfix_api_url}/messages",
#         headers=headers,
#         json=data
#     )
#
#     try:
#         response.raise_for_status()
#         return response.json()["id"]
#     except requests.exceptions.HTTPError as errh:
#         raise Exception(f"HTTP Error: {errh}")
#     except requests.exceptions.ConnectionError as errc:
#         raise Exception(f"Error Connecting: {errc}")
#     except requests.exceptions.Timeout as errt:
#         raise Exception(f"Timeout Error: {errt}")
#     except requests.exceptions.RequestException as err:
#         raise Exception(f"Request Error: {err}")
#
#
# def get_planfix_response(message_id):
#     headers = {
#         "Authorization": f"Bearer {planfix_api_key}"
#     }
#
#     response = requests.get(
#         f"{planfix_api_url}/messages/{message_id}",
#         headers=headers
#     )
#
#     if response.status_code == 200:
#         return response.json()["text"]
#     else:
#         raise Exception("Failed to get response")

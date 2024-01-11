# email_email_checking_and_verification_hunter/main.py

from typing import NoReturn

import requests

from config import RED, RESET_ALL, YELLOW, MAGENTA
from menu import Menu



def main() -> NoReturn:
    """
       Основная функция программы email_email_checking_and_verification_hunter.

       Эта функция предлагает пользователю ввести свой API-ключ Hunter, инициализирует объект Menu,
       устанавливает API-ключ и отображает основное меню для взаимодействия с API Hunter.

       Исключения:
           NoReturn: Эта функция не возвращает значение; она запускает основную программу.

       """
    # Запрос у пользователя ввода API-ключа Hunter
    api_key = input(f"{MAGENTA}Введите ваш API-ключ Hunter: {RESET_ALL}")

    # Инициализация объекта Menu
    menu = Menu()

    # Установка API-ключа
    menu.set_api_key(api_key)

    # Отображение основного меню для взаимодействия с API Hunter
    menu.display_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{YELLOW}Program interrupted by user{RESET_ALL}")
    except requests.exceptions.RequestException as req_error:
        print(f"{RED}An error occurred during a request: {req_error}{RESET_ALL}")
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET_ALL}")



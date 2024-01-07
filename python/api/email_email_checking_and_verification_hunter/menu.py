# email_email_checking_and_verification_hunter/menu

import json

import requests

from config import RESET_ALL, RED, CYAN, YELLOW
from hunter_client import HunterClient
from local_storage_service import LocalStorageService
from logger import Logger
from utils import _handle_verification_result


class Menu:
    """
        Класс, представляющий меню программы email_email_checking_and_verification_hunter.

        Атрибуты:
            hunter_client (HunterClient): Экземпляр HunterClient для взаимодействия с Hunter API.
            storage_service (LocalStorageService): Экземпляр LocalStorageService для управления локальным хранилищем.
            logger (Logger): Экземпляр Logger для записи событий.

        Методы:
            set_api_key(provided_api_key: str) -> None:
                Устанавливает API-ключ для HunterClient и проверяет его на валидность.

            display_menu() -> None:
                Отображает главное меню и обрабатывает ввод пользователя.

            domain_search_menu() -> None:
                Обрабатывает опцию меню поиска домена.

            email_finder_menu() -> None:
                Обрабатывает опцию меню поиска электронной почты.

            email_verification_menu() -> None:
                Обрабатывает опцию меню верификации электронной почты.

            email_count_menu() -> None:
                Обрабатывает опцию меню подсчета электронной почты.

            account_information_menu() -> None:
                Обрабатывает опцию меню информации об аккаунте.

        """
    def __init__(self):
        """
        Инициализирует объект Menu.

        Параметры:
            hunter_client (HunterClient): Объект HunterClient для взаимодействия с Hunter API.
            storage_service (LocalStorageService): Объект LocalStorageService для управления локальным хранилищем
            результатов верификации.
            logger (Logger): Логгер для записи событий.

        """
        self.hunter_client = None                             # Создаем экземпляр клиента Hunter
        self.storage_service = LocalStorageService()          # Создаем сервис локального хранения данных
        self.logger = Logger("Menu")                          # Создаем логгер для класса Menu с именем "Menu"

    def set_api_key(self, provided_api_key: str) -> None:
        """
        Меню для обработки опции установки API-ключа для экземпляра HunterClient.

        Параметры:
            provided_api_key (str): Предоставленный API-ключ.

        Возвращает:
            None
        """
        # Создаем экземпляр HunterClient, используя предоставленный API ключ
        self.hunter_client = HunterClient(provided_api_key)

        # Проверяем, является ли предоставленный API ключ действительным
        verification_result = self.hunter_client.email_verifier("test@dummy.com", raw=True)

        if "error" in verification_result:
            self.logger.warning(f"Invalid API key: {provided_api_key}")
            print(f"{RED}Invalid API key: {provided_api_key}{RESET_ALL}")

            # Завершаем программу, так как API ключ недействителен
            exit()

    def display_menu(self) -> None:
        """
        Меню для отображения основного меню и обработки ввода пользователя.

        Параметры:
            None

        Возвращает:
            None
        """
        while True:
            print(f"{RED}---------- Menu ------------{RESET_ALL}")
            print(f"{CYAN}1. Domain Search{RESET_ALL}")
            print(f"{CYAN}2. Email Finder{RESET_ALL}")
            print(f"{CYAN}3. Email Verification{RESET_ALL}")
            print(f"{CYAN}4. Email Count{RESET_ALL}")
            print(f"{CYAN}5. Account Information{RESET_ALL}")
            print(f"{CYAN}6. Exit{RESET_ALL}")

            choice = input(f"{YELLOW}Select an option (1-6): {RESET_ALL}")
            if choice == "1":
                self.domain_search_menu()
            elif choice == "2":
                self.email_finder_menu()
            elif choice == "3":
                self.email_verification_menu()
            elif choice == "4":
                self.email_count_menu()
            elif choice == "5":
                self.account_information_menu()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                self.logger.warning("Invalid input. Please choose an option from 1 to 6.")
                print(f"{RED}Invalid input. Please choose an option from 1 to 6.{RESET_ALL}")

    def domain_search_menu(self) -> None:
        """
        Меню для обработки опции меню поиска домена. Предлагает пользователю ввести данные, вызывает
        соответствующий метод Hunter API и обрабатывает результат.

        Параметры:
            None

        Возвращает:
            None
        """
        # Запрашиваем у пользователя домен для поиска
        domain_to_search = input(f"{CYAN}Enter the domain to search: {RESET_ALL}")
        # Запрашиваем у пользователя название компании (опционально)
        company_name = input(f"{YELLOW}Enter the company name (optional): {RESET_ALL}")

        try:
            # Выполняем поиск домена, используя HunterClient
            result = self.hunter_client.domain_search(
                domain=domain_to_search,
                company=company_name,
                raw=True
            )
            # Преобразуем ответ от сервера в формат JSON
            result_data = result.json()

            # Формируем ключ для сохранения результатов поиска
            key = f"{domain_to_search or company_name}_search"

            # Сохраняем результаты поиска в локальном хранилище
            self.storage_service.save_verification(key, result_data)

            # Обрабатываем и выводим результаты поиска
            _handle_verification_result(result_data)

        # Выводим предупреждение в лог и на экран в случае ошибки HTTP
        except requests.exceptions.HTTPError as http_error:
            self.logger.warning(f"{RED}HTTP Error: {http_error.response.status_code}{RESET_ALL}")
            print(f"{RED}HTTP Error: {http_error.response.status_code}{RESET_ALL}")
        # Выводим предупреждение в лог и на экран в случае ошибки значения
        except ValueError as ve:
            self.logger.warning(f"Method domain_search_menu:\nError: {ve}")
            print(f"{RED}Ошибка: {ve}{RESET_ALL}")
        # Выводим предупреждение в лог и на экран в случае ошибки запроса
        except requests.exceptions.RequestException as req_err:
            self.logger.warning(f"{RED}An error occurred during the request: {req_err}{RESET_ALL}")
            print(f"{RED}An error occurred during the request: {req_err}{RESET_ALL}")
        # Выводим предупреждение в лог и на экран в случае неожиданной ошибки
        except Exception as unexpected_err:
            self.logger.warning(f"{RED}An unexpected error occurred: {unexpected_err}{RESET_ALL}")
            print(f"{RED}An unexpected error occurred: {unexpected_err}{RESET_ALL}")

    def email_finder_menu(self) -> None:
        """
        Меню для обработки опции меню поиска электронной почты. Предлагает пользователю ввести данные,
        вызывает соответствующий метод Hunter API и обрабатывает результат.

        Параметры:
            None

        Возвращает:
            None
        """
        # Получаем значения для поиска Email
        domain_value = input(f"{CYAN}Enter the domain to search for Email: {RESET_ALL}")
        company_value = input(f"{YELLOW}Enter the company name (optional): {RESET_ALL}")
        first_name_value = input(f"{CYAN}Enter the first name: {RESET_ALL}")
        last_name_value = input(f"{CYAN}Enter the last name: {RESET_ALL}")
        full_name_value = input(f"{YELLOW}Enter the full name (optional): {RESET_ALL}")
        max_duration_value = input(
            f"{YELLOW}Enter the maximum duration of the request (3 to 20 seconds, optional): {RESET_ALL}")

        # Проверка на пустые строки
        if not any([domain_value, company_value, first_name_value, last_name_value]):
            self.logger.warning(
                "You must fill in at least one of the fields (domain, company name, first name, last name).")
            print(f"{RED}Error: You must fill in at least one of the fields "
                  f"(domain, company name, first name, last name).{RESET_ALL}")
            return

        # Проверка корректности ввода максимальной длительности запроса
        if max_duration_value and not max_duration_value.isdigit():
            self.logger.warning("Maximum duration of the request must be a number.")
            print(f"{RED}Error: Maximum duration of the request must be a number.{RESET_ALL}")
            return

        # Преобразование строки максимальной длительности запроса в число
        if max_duration_value:
            max_duration_value = int(max_duration_value)
            if not (3 <= max_duration_value <= 20):
                self.logger.warning("Maximum duration of the request must be from 3 to 20 seconds.")
                print(f"{RED}Error: Invalid value for maximum duration of the request. "
                      f"Please enter a number from 3 to 20.{RESET_ALL}")
                return

        try:
            # Выполнение запроса к Hunter API для поиска Email
            result = self.hunter_client.email_finder(
                domain=domain_value,
                company=company_value,
                first_name=first_name_value,
                last_name=last_name_value,
                full_name=full_name_value,
                max_duration=max_duration_value,
                raw=True
            )

            # Проверка наличия ошибок в ответе от сервера
            if isinstance(result, dict) and "error" in result:
                print(f"{RED}Error: {result['error']}{RESET_ALL}")
                return

            # Проверка статуса ответа
            if not isinstance(result, requests.Response) or result.status_code != 200:
                print(f"{RED}Result.status_code != 200: {result.status_code}{RESET_ALL}")
                return

            # Преобразование ответа от сервера в формат JSON
            result_data = result.json()

            # Проверка наличия ключа 'data' в ответе
            if 'data' in result_data:
                # Формирование уникального ключа для сохранения результата
                key = f"{domain_value or company_value}_{first_name_value}_{last_name_value}_search"
                # Сохранение результата в локальное хранилище
                self.storage_service.save_verification(key, result_data['data'])
                # Обработка и вывод результатов
                _handle_verification_result(result_data['data'])
            else:
                # В случае некорректного формата ответа от сервера
                print(f"{RED}Invalid response format{RESET_ALL}")

        # В случае ошибки при выполнении запроса
        except requests.exceptions.RequestException as request_exception:
            self.logger.warning(f"Error during request execution: {request_exception}")
            print(f"{RED}Error during request execution: {request_exception}{RESET_ALL}")
        # В случае ошибки валидации данных
        except ValueError as validation_error:
            self.logger.warning(f"Data validation error: {validation_error}")
            print(f"{RED}Data validation error: {validation_error}{RESET_ALL}")
        # В случае ошибки HTTP при выполнении запроса
        except requests.exceptions.HTTPError as http_error:
            self.logger.warning(f"{RED}HTTP Error: {http_error.response.status_code}{RESET_ALL}")
            print(f"{RED}HTTP Error: {http_error.response.status_code}{RESET_ALL}")
        # В случае непредвиденной ошибки
        except Exception as unexpected_error:
            self.logger.warning(f"Unexpected error: {unexpected_error}")
            print(f"{RED}Unexpected error: {unexpected_error}{RESET_ALL}")

    def email_verification_menu(self) -> None:
        """
        Меню для верификации электронной почты. Запрашивает у пользователя Email для верификации, вызывает
        соответствующий метод Hunter API и обрабатывает результат.

        Возвращает:
            None

        """
        # Получаем Email для верификации от пользователя
        email_to_verify = input(f"{CYAN}Enter the Email to verify: {RESET_ALL}")
        # Выполняем запрос на верификацию Email
        result = self.hunter_client.email_verifier(email_to_verify, raw=True)

        # Проверка, является ли результат словарем
        if isinstance(result, dict):  # Check if the result is a dictionary
            # Если результат - словарь, проверяем наличие ключа 'error'
            print(f"{RED}Error: {result.get('error', 'Unknown error')}{RESET_ALL}")
            return

        # Пытаемся преобразовать ответ от сервера в формат JSON
        try:
            # Преобразуем ответ от сервера в формат JSON
            result_data = result.json()
            # Формируем ключ для сохранения результата в локальное хранилище
            key = f"{email_to_verify}_verification"
            # Сохраняем результат верификации в локальное хранилище
            self.storage_service.save_verification(key, result_data)
            # Обрабатываем результат верификации
            _handle_verification_result(result_data)

        # В случае ошибки декодирования JSON=
        except json.JSONDecodeError:
            self.logger.warning("JSON decoding error.")
            print(f"{RED}JSON decoding error.{RESET_ALL}")

    def email_count_menu(self) -> None:
        """
        Меню для подсчета количества Email по домену или компании. Запрашивает у пользователя данные
        для подсчета, вызывает соответствующий метод Hunter API и обрабатывает результат.

        Возвращает:
            None

        """
        # Получаем данные от пользователя: домен для подсчета Email и опциональное название компании
        domain_to_count = input(f"{CYAN}Enter the domain to count Email: {RESET_ALL}")
        company_to_count = input(f"{YELLOW}Enter the company name (optional): {RESET_ALL}")
        try:
            # Выполняем запрос к Hunter API для подсчета Email
            result = self.hunter_client.email_count(domain=domain_to_count, company=company_to_count, raw=True)
            # Преобразуем ответ от сервера в формат JSON
            result_data = result.json()
            # Формируем ключ для сохранения результата в локальное хранилище
            key = f"{domain_to_count or company_to_count}_email_count"
            # Сохраняем результат подсчета Email в локальное хранилище
            self.storage_service.save_verification(key, result_data)
            # Обрабатываем результат подсчета Email
            _handle_verification_result(result_data)

        # Обрабатываем ошибку, если она возникает в процессе выполнения запроса
        except ValueError as ve:
            self.logger.warning(f"Method email_count_menu:\nError: {ve}")
            print(f"{RED}Error: {ve}{RESET_ALL}")

    def account_information_menu(self) -> None:
        """
        Меню для получения информации об аккаунте. Вызывает соответствующий метод Hunter API и обрабатывает результат.

        Возвращает:
            None

        """
        # Выполняем запрос к Hunter API для получения информации об аккаунте
        result = self.hunter_client.account_information(raw=True)
        # Преобразуем ответ от сервера в формат JSON
        result_data = result.json()
        # Задаем ключ для сохранения результата в локальное хранилище
        key = "account_info"
        # Если в данных присутствует информация о запросах, переименовываем ключ 'requests' в 'calls'
        if 'requests' in result_data['data']:
            result_data['data']['calls'] = result_data['data'].pop('requests')
        # Сохраняем результат запроса в локальное хранилище
        self.storage_service.save_verification(key, result_data)
        # Обрабатываем и выводим результат запроса
        _handle_verification_result(result_data)

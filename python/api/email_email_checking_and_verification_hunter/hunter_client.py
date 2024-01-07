# email_email_checking_and_verification_hunter/hunter_client.py

# email_email_checking_and_verification_hunter/hunter_client.py

import requests

from config import RED, RESET_ALL
from logger import Logger
from request_manager import RequestManager


class HunterClient:
    """
    Класс HunterClient для взаимодействия с Hunter API в программе email_email_checking_and_verification_hunter.

    Методы:
        domain_search(domain: str, company: str, limit: int, offset: int, email_type: str, seniority: str,
                      department: str, required_field: str, raw: bool) -> requests.Response or dict:
            Выполняет запрос к API Hunter для поиска информации о домене.

        email_finder(domain: str, company: str, first_name: str, last_name: str, full_name: str,
                     max_duration: int, raw: bool) -> requests.Response or dict:
            Выполняет запрос к API Hunter для поиска электронного адреса.

        email_verifier(email: str, raw: bool) -> requests.Response or dict:
            Выполняет запрос к API Hunter для верификации электронного адреса.

        email_count(domain: str, company: str, raw: bool) -> requests.Response or dict:
            Выполняет запрос к API Hunter для получения количества электронных адресов.

        account_information(raw: bool) -> requests.Response or dict:
            Выполняет запрос к API Hunter для получения информации о текущем аккаунте.

    Атрибуты:
        api_key (str): API ключ Hunter.
        base_url (str): Базовый URL для API Hunter.
        logger (Logger): Логгер для записи событий.
        request_manager (RequestManager): Менеджер запросов для обработки HTTP-запросов.

    """

    def __init__(self, provided_api_key: str):
        """
        Инициализирует объект HunterClient.

        Параметры:
            provided_api_key (str): Предоставленный API ключ Hunter.

        """
        self.api_key = provided_api_key  # Интерфейс для доступа к ключу API Hunter.
        self.base_url = "https://api.hunter.io/v2/"  # Базовый URL для взаимодействия с API Hunter.
        self.logger = Logger("HunterClient")  # Логгер для записи событий.
        self.request_manager = RequestManager()  # Менеджер запросов для обработки HTTP-запросов.

    def domain_search(self, domain: str = None, company: str = None, limit: int = 10, offset: int = 0,
                      email_type: str = None, seniority: str = None, department: str = None, required_field: str = None,
                      raw: bool = False) -> requests.Response or dict:
        """
        Выполняет запрос к API Hunter для поиска информации о домене.

        Параметры:
            domain (str): Домен для поиска.
            company (str): Название компании для поиска.
            limit (int): Максимальное количество результатов.
            offset (int): Смещение в результатах.
            email_type (str): Тип электронной почты.
            seniority (str): Уровень должности.
            department (str): Отдел.
            required_field (str): Обязательное поле.
            raw (bool): Формат ответа (сырой или нет).

        Возвращает:
            requests.Response or dict: Объект Response в случае успешного запроса,
            словарь с ключами 'error' и 'response' в случае ошибки.

        """
        # Проверяем, что указан хотя бы домен или компания.
        if not domain and not company:
            raise ValueError("At least a domain name or company name must be specified.")
        # Составление URL и параметров запроса для метода domain-search
        url = self.base_url + "domain-search"

        # Параметры запроса, включая домен, компанию, ограничение, смещение, тип email, старшинство, отдел,
        # обязательное поле и другие.
        params = {
            "domain": domain,
            "company": company,
            "limit": limit,
            "offset": offset,
            "type": email_type,
            "seniority": seniority,
            "department": department,
            "required_field": required_field,
            "api_key": self.api_key,
            "raw": raw
        }
        try:
            # Выполняем запрос к API Hunter для поиска информации о домене.
            return self.request_manager.make_request(url, params)
        except requests.exceptions.RequestException as error:
            return {"error": str(error)}

    def email_finder(self, domain: str = None, company: str = None, first_name: str = None, last_name: str = None,
                     full_name: str = None, max_duration: int = None, raw: bool = False) -> requests.Response or dict:
        """
        Выполняет запрос к API Hunter для поиска электронного адреса.

        Параметры:
            domain (str): Домен для поиска.
            company (str): Название компании для поиска.
            first_name (str): Имя.
            last_name (str): Фамилия.
            full_name (str): Полное имя.
            max_duration (int): Максимальная длительность поиска.
            raw (bool): Формат ответа (сырой или нет).

        Возвращает:
            requests.Response or dict: Объект Response в случае успешного запроса,
            словарь с ключами 'error' и 'response' в случае ошибки.

        """
        # Если не указано ни доменное имя, ни название компании, генерируем предупреждение и вызываем ValueError.
        if not domain and not company:
            self.logger.warning("At least a domain name or company name must be specified.")
            raise ValueError(f"{RED}At least a domain name or company name must be specified.{RESET_ALL}")

        # Если не указаны ни имя и фамилия, ни полное имя, генерируем предупреждение и вызываем ValueError.
        if not (first_name and last_name) and not full_name:
            self.logger.warning("At least first name and last name, or full name must be specified.")
            raise ValueError(f"{RED}At least first name and last name, or full name must be specified.{RESET_ALL}")

        # Составление URL и параметров запроса для метода email-finder
        url = self.base_url + "email-finder"
        # Параметры запроса, включая домен, компанию, имя, фамилию, полное имя, максимальную длительность и другие.
        params = {
            "domain": domain,
            "company": company,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "max_duration": max_duration,
            "api_key": self.api_key,
            "raw": raw
        }
        try:
            # Выполняем запрос к API Hunter для поиска email.
            return self.request_manager.make_request(url, params)
        except requests.exceptions.RequestException as error:
            return {"error": str(error)}

    def email_verifier(self, email: str, raw: bool = False) -> requests.Response or dict:
        """
        Выполняет запрос к API Hunter для верификации электронного адреса.

        Параметры:
            email (str): Электронный адрес для верификации.
            raw (bool): Формат ответа (сырой или нет).

        Возвращает:
            requests.Response or dict: Объект Response в случае успешного запроса,
            словарь с ключами 'error' и 'response' в случае ошибки.

        """
        # Формируем URL для запроса к API Hunter для верификации email.
        url = self.base_url + "email-verifier"

        # Параметры запроса, включая email, API ключ и флаг raw.
        params = {
            "email": email,
            "api_key": self.api_key,
            "raw": raw
        }

        try:
            # Выполняем запрос к Hunter API для верификации email.
            return self.request_manager.make_request(url, params)
        except requests.exceptions.RequestException as error:
            error_response = {"error": str(error)}
            return error_response

    def email_count(self, domain: str = None, company: str = None, raw: bool = False) -> requests.Response or dict:
        """
        Выполняет запрос к API Hunter для получения количества электронных адресов.

        Параметры:
            domain (str): Домен для поиска.
            company (str): Название компании для поиска.
            raw (bool): Формат ответа (сырой или нет).

        Возвращает:
            requests.Response or dict: Объект Response в случае успешного запроса,
            словарь с ключами 'error' и 'response' в случае ошибки.

        """
        # Проверяем, что указан хотя бы домен или компания.
        if not domain and not company:
            self.logger.warning("At least a domain name or company name must be specified.")
            raise ValueError(f"{RED}At least a domain name or company name must be specified.{RESET_ALL}")

        # Формируем URL для запроса к API Hunter для получения количества email.
        url = self.base_url + "email-count"
        # Параметры запроса, включая домен, компанию, API ключ и флаг raw.
        params = {
            "domain": domain,
            "company": company,
            "api_key": self.api_key,
            "raw": raw
        }
        try:
            # Выполняем запрос к API Hunter для получения количества email.
            return self.request_manager.make_request(url, params)
        except requests.exceptions.RequestException as error:
            return {"error": str(error)}

    def account_information(self, raw: bool = False) -> requests.Response or dict:
        """
        Выполняет запрос к API Hunter для получения информации о текущем аккаунте.

        Параметры:
            raw (bool): Формат ответа (сырой или нет).

        Возвращает:
            requests.Response or dict: Объект Response в случае успешного запроса,
            словарь с ключами 'error' и 'response' в случае ошибки.

        """
        # Формируем URL для запроса к API Hunter для получения информации об аккаунте.
        url = self.base_url + "account"

        # Параметры запроса, включая API ключ и флаг "raw".
        params = {
            "api_key": self.api_key,
            "raw": raw
        }
        try:
            # Выполняем запрос к API Hunter для получения информации об аккаунте.
            return self.request_manager.make_request(url, params)
        except requests.exceptions.RequestException as error:
            return {"error": str(error)}

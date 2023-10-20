import configparser
import functools
import traceback
from typing import List, Dict, Union


def config_access(func):
    """
    Декоратор для автоматической загрузки и сохранения конфигурации при вызове методов.

    :param func: Функция для декорирования
    :return: Обернутая функция
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            self.load_config()
            result = func(self, *args, **kwargs)
        finally:
            self.save_config()
        return result

    return wrapper


class DNSConfigManager:
    def __init__(self, config_file: str):
        """
        Инициализирует объект DNSConfigManager.

        :param config_file: Путь к файлу конфигурации
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        # Загрузка конфигурации при инициализации
        self.load_config()

    def load_config(self) -> bool:
        """
        Загружает конфигурацию из файла.

        :return: True, если загрузка прошла успешно, False в противном случае
        """
        print(f"Loading config from {self.config_file}")
        try:
            self.config.read(self.config_file)
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            traceback.print_exc()
            return False

    def get_config_value(self, section: str, key: str) -> str:
        """
        Получает значение из конфигурации.

        :param section: Название секции в конфигурации
        :param key: Ключ параметра
        :return: Значение параметра
        """
        return self.config[section][key]

    def read_config_file(self) -> None:
        """
        Читает файл конфигурации.

        :return: None
        """
        self.config.read(self.config_file)

    def section_exists(self, section: str) -> bool:
        """
        Проверяет существование секции в конфигурации.

        :param section: Название секции
        :return: True, если секция существует, False в противном случае
        """
        return section in self.config

    def get_all_sections(self) -> List[str]:
        """
        Получает список всех секций в конфигурации.

        :return: Список названий секций
        """
        return self.config.sections()

    def get_default_blocked_response(self) -> Dict[str, str]:
        """
        Получает настройки ответа по умолчанию для заблокированных доменов.

        :return: Словарь с настройками ответа по умолчанию
        """
        response_code = self.config['custom_responses']['default_blocked_response_code']
        response_text = self.config['custom_responses']['default_blocked_response_text']
        return {"response_code": response_code, "response_text": response_text}

    def get_blacklist(self) -> List[str]:
        """
        Получает список доменов в черном списке.

        :return: Список доменов
        """
        return [domain.strip() for domain in self.config['security']['blacklist_domains'].split(',')]

    def get_blocked_responses(self) -> Dict[str, str]:
        """
        Получает пользовательские ответы на запросы.

        :return: Словарь с пользовательскими ответами
        """
        if 'custom_responses' in self.config:
            return self.config['custom_responses']
        else:
            return {}

    def key_exists(self, section: str, key: str) -> bool:
        """
        Проверяет существование ключа в секции конфигурации.

        :param section: Название секции
        :param key: Ключ
        :return: True, если ключ существует, False в противном случае
        """
        return key in self.config[section]

    def save_config(self) -> None:
        """
        Сохраняет текущую конфигурацию в файл.

        :return: None
        """
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    @config_access
    def update_section(self, section: str, settings: Dict[str, Union[str, None]]) -> None:
        """
        Обновляет секцию конфигурации новыми настройками.

        :param section: Название секции
        :param settings: Новые настройки в виде словаря (ключи и значения)
        :return: None
        """
        if section not in self.config:
            self.config[section] = {}

        for key, value in settings.items():
            if value is None:
                if key in self.config[section]:
                    del self.config[section][key]
            else:
                self.config[section][key] = value
        self.save_config()  # Сохранение конф

    def create_dns_config_file(self) -> None:
        """
        Создает файл конфигурации DNS сервера с настройками по умолчанию.

        :return: None
        """
        if not self.config.has_section('server'):
            self.config.add_section('server')
        # Заполняем параметры сервера
        self.config.set('server', 'ip_address', '127.0.0.1')
        self.config.set('server', 'port', '53')
        self.config.set('server', 'upstream_dns', '8.8.8.8')

        if not self.config.has_section('security'):
            self.config.add_section('security')
        # Заполняем параметры безопасности
        self.config.set('security', 'dns_amplification_protection', 'true')
        self.config.set('security', 'query_logging', 'true')
        self.config.set('security', 'blacklist_domains', '')

        if not self.config.has_section('caching'):
            self.config.add_section('caching')
        # Заполняем параметры кеширования
        self.config.set('caching', 'cache_enabled', 'true')
        self.config.set('caching', 'cache_size', '100')

        if not self.config.has_section('other'):
            self.config.add_section('other')
        # Заполняем остальные разделы аналогичным образом
        self.config.set('other', 'debug_mode', 'false')
        self.config.set('other', 'log_file', '/var/log/dns_server.log')

        if not self.config.has_section('custom_responses'):
            self.config.add_section('custom_responses')
        # Заполняем пользовательские ответы
        self.config.set('custom_responses', 'default_blocked_response_code', 'NOTIMP')
        self.config.set('custom_responses', 'default_blocked_response_text', 'Default blocked response text')

        self.save_config()  # Сохраняем только измененные параметры

    @config_access
    def add_blacklist_domains(self, domains: List[str]) -> None:
        """
        Добавляет домены в черный список.

        :param domains: Список доменов для добавления
        :return: None
        """
        current_blacklist = self.config['security'].get('blacklist_domains', '').split(',')
        current_blacklist.extend(domains)
        self.config['security']['blacklist_domains'] = ','.join(current_blacklist)
        self.save_config()

    @config_access
    def remove_blacklist_domains(self, domains: List[str]) -> None:
        """
        Удаляет домены из черного списка.

        :param domains: Список доменов для удаления
        :return: None
        """
        current_blacklist = self.config['security'].get('blacklist_domains', '').split(',')
        for domain in domains:
            if domain in current_blacklist:
                current_blacklist.remove(domain)
        self.config['security']['blacklist_domains'] = ','.join(current_blacklist)
        self.save_config()

    @config_access
    def add_custom_responses(self, custom_responses: Dict[str, str]) -> None:
        """
        Добавляет пользовательские ответы.

        :param custom_responses: Словарь пользовательских ответов (имя и текст)
        :return: None
        """
        current_custom_responses = self.config['custom_responses']
        current_custom_responses.update(custom_responses)
        self.config['custom_responses'] = current_custom_responses
        self.save_config()

    @config_access
    def remove_custom_responses(self, response_names: List[str]) -> None:
        """
        Удаляет пользовательские ответы по их именам.

        :param response_names: Список имен пользовательских ответов для удаления
        :return: None
        """
        current_custom_responses = self.config['custom_responses']
        for response_name in response_names:
            if response_name in current_custom_responses:
                del current_custom_responses[response_name]
        self.config['custom_responses'] = current_custom_responses
        self.save_config()

    def get_default_blocked_response_text(self) -> str:
        """
        Получает текст ответа по умолчанию для заблокированных доменов.

        :return: Текст ответа по умолчанию
        """
        if 'custom_responses' in self.config:
            return self.config['custom_responses'].get('default_blocked_response_text', 'not resolved')
        else:
            return "not resolved"

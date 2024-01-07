# email_email_checking_and_verification_hunter/utils.py

from prettytable import PrettyTable

from config import RED, RESET_ALL, MAGENTA, CYAN, YELLOW


def _handle_verification_result(result_data: dict) -> None:
    """
    Обработка результата верификации и вывод отформатированной информации.

    Параметры:
        result_data (dict): Данные результата верификации.

    Возвращает:
        None

    """
    # Если в ответе есть поле 'error', выводим сообщение об ошибке запроса
    if 'error' in result_data:
        print(f"{RED}Request error: {result_data['error']}{RESET_ALL}")
        return

    # Если в ответе отсутствует поле 'data', выводим сообщение о отсутствии данных
    if 'data' not in result_data:
        print(f"{RED}No data in the response{RESET_ALL}")
        return

    # Создание объекта PrettyTable для отображения табличных данных
    table = PrettyTable()

    # Установка заголовков полей таблицы с использованием цветов из констант
    table.field_names = [f"{MAGENTA}Параметр{RESET_ALL}", f"{MAGENTA}Значение{RESET_ALL}"]

    # Получение данных из ответа API
    data = result_data["data"]

    # Обработка основных данных из ответа API
    for key, value in data.items():
        # Проверка, что ключ не относится к специальным полям ["calls", "technologies", "emails", "linked_domains"]
        if key not in ["calls", "technologies", "emails", "linked_domains"]:
            # Проверка, что значение не является списком или словарем
            if not isinstance(value, (list, dict)):
                # Добавление строки с данными в таблицу с использованием цветов из констант
                table.add_row([f"{CYAN}{key}{RESET_ALL}", f"{CYAN}{value}{RESET_ALL}"])
    # Вывод таблицы с основными данными в консоль
    print(table)

    # Если есть данные для 'calls', создаем и выводим таблицу
    if 'calls' in data:
        # Создаем объект PrettyTable для отображения данных в виде таблицы
        calls_table = PrettyTable()

        # Устанавливаем заголовки столбцов
        calls_table.field_names = [
            f"{MAGENTA}Request Type{RESET_ALL}",
            f"{MAGENTA}Used{RESET_ALL}",
            f"{MAGENTA}Available{RESET_ALL}"
        ]

        # Заполнение таблицы данными о запросах
        for request_type, call_data in data['calls'].items():
            calls_table.add_row([
                f"{YELLOW}{request_type}{RESET_ALL}",
                f"{YELLOW}{call_data.get('used', '')}{RESET_ALL}",
                f"{YELLOW}{call_data.get('available', '')}{RESET_ALL}"
            ])
        # Вывод таблицы с основными данными в консоль
        print(calls_table)

    # Если есть данные для 'technologies', создаем и выводим таблицу
    if 'technologies' in data:
        # Создаем объект PrettyTable для красивого вывода в консоль
        technologies_table = PrettyTable()

        # Устанавливаем заголовок таблицы
        technologies_table.field_names = [f"{MAGENTA}Technologies{RESET_ALL}"]

        # Заполняем таблицу данными из 'technologies'
        for technology in data['technologies']:
            technologies_table.add_row([f"{CYAN}{technology}{RESET_ALL}"])
        # Выводим таблицу с информацией о технологиях
        print(technologies_table)

    # Если есть данные для 'emails', создаем и выводим таблицу
    if 'emails' in data:
        # Создаем объект PrettyTable для красивого вывода в консоль
        emails_table = PrettyTable()

        # Устанавливаем заголовок таблицы
        emails_table.field_names = [
            f"{MAGENTA}Email{RESET_ALL}",
            f"{MAGENTA}First Name{RESET_ALL}",
            f"{MAGENTA}Last Name{RESET_ALL}"
        ]

        # Заполняем таблицу данными из 'emails'
        for email_info in data['emails']:
            email_value = email_info.get('value', '')
            first_name = email_info.get('first_name', '')
            last_name = email_info.get('last_name', '')
            emails_table.add_row([
                f"{MAGENTA}{email_value}{RESET_ALL}",
                f"{MAGENTA}{first_name}{RESET_ALL}",
                f"{MAGENTA}{last_name}{RESET_ALL}"
            ])

        # Выводим таблицу с информацией об электронных адресах
        print(emails_table)

    # Если есть данные для 'linked_domains', создаем и выводим таблицу
    if 'linked_domains' in data:
        # Создаем объект PrettyTable для красивого вывода в консоль
        linked_domains_table = PrettyTable()

        # Устанавливаем заголовок таблицы
        linked_domains_table.field_names = [f"{MAGENTA}Linked Domains{RESET_ALL}"]

        # Заполняем таблицу данными из 'linked_domains'
        for linked_domain in data['linked_domains']:
            linked_domains_table.add_row([f"{MAGENTA}{linked_domain}{RESET_ALL}"])

        # Выводим таблицу со связанными доменами
        print(linked_domains_table)

    # Проверяем наличие данных для 'verification' и выводим соответствующую таблицу
    if 'verification' in data:
        # Извлекаем данные о верификации
        verification_data = data['verification']

        # Создаем объект PrettyTable для красивого вывода в консоль
        verification_table = PrettyTable()

        # Устанавливаем заголовок таблицы
        verification_table.field_names = [f"{MAGENTA}Parameter{RESET_ALL}", f"{MAGENTA}Value{RESET_ALL}"]

        # Заполняем таблицу данными из 'verification'
        verification_table.add_row(
            [f"{YELLOW}Verification Status{RESET_ALL}", f"{YELLOW}{verification_data.get('status', '')}{RESET_ALL}"])
        verification_table.add_row(
            [f"{YELLOW}Verification Date{RESET_ALL}", f"{YELLOW}{verification_data.get('date', '')}{RESET_ALL}"])

        # Выводим таблицу с данными о верификации
        print(verification_table)

    # Проверяем наличие данных для 'sources'
    if 'sources' in data:
        # Извлекаем данные о источниках
        sources = data['sources']

        # Проверяем, есть ли хотя бы один источник
        if sources:
            # Создаем объект PrettyTable для красивого вывода в консоль
            sources_table = PrettyTable()

            # Устанавливаем заголовок таблицы
            sources_table.field_names = [
                f"{MAGENTA}Domain{RESET_ALL}",
                f"{MAGENTA}URI{RESET_ALL}",
                f"{MAGENTA}Extracted On{RESET_ALL}",
                f"{MAGENTA}Last Seen On{RESET_ALL}",
                f"{MAGENTA}Still On Page{RESET_ALL}"
            ]

            # Заполняем таблицу данными из 'sources'
            for source in sources:
                domain = source.get('domain', '')
                uri = source.get('uri', '')
                extracted_on = source.get('extracted_on', '')
                last_seen_on = source.get('last_seen_on', '')
                still_on_page = source.get('still_on_page', False)

                sources_table.add_row([
                    f"{YELLOW}{domain}{RESET_ALL}",
                    f"{YELLOW}{uri}{RESET_ALL}",
                    f"{YELLOW}{extracted_on}{RESET_ALL}",
                    f"{YELLOW}{last_seen_on}{RESET_ALL}",
                    f"{YELLOW}{still_on_page}{RESET_ALL}"
                ])

            # Выводим таблицу с информацией об источниках
            print(sources_table)
        else:
            # Если источники не найдены, выводим соответствующее сообщение
            print(f"{YELLOW}Sources not found.{RESET_ALL}")

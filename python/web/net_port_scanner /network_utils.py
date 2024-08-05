# net_port_scanner/network_utils.py

"""
Этот модуль содержит вспомогательные функции для работы с сетевыми интерфейсами,
записью результатов сканирования в CSV-файл и логированием результатов сканирования.
"""

import csv
import os
from typing import Optional, List, Tuple

import netifaces

from logger_config import logger


async def get_network_interfaces() -> List[str]:
    """
    Получает список IP-адресов сетевых интерфейсов на текущем хосте.

    Returns:
        List[str]: Список строк, представляющих IP-адреса сетевых интерфейсов.
    """
    # Создаем пустой список для хранения IP-адресов интерфейсов
    interfaces = []
    # Перебираем все сетевые интерфейсы, доступные на хосте
    for interface in netifaces.interfaces():
        # Получаем адреса для текущего интерфейса
        addrs = netifaces.ifaddresses(interface)
        # Проверяем наличие IPv4 адресов в списке адресов интерфейса
        if netifaces.AF_INET in addrs:
            # Если IPv4 адреса найдены, перебираем их
            for link in addrs[netifaces.AF_INET]:
                # Добавляем каждый найденный IP-адрес в список
                interfaces.append(link['addr'])
    # Возвращаем список найденных IP-адресов интерфейсов
    return interfaces


def write_results_to_csv(target: str, ip: str, results: List[Tuple[int, bool, Optional[str]]],
                         output_file: str) -> None:
    """
    Записывает результаты сканирования портов в CSV-файл.

    Args:
        target (str): Целевой хост.
        ip (str): IP-адрес целевого хоста.
        results (List[Tuple[int, bool, Optional[str]]]): Список результатов сканирования портов.
        output_file (str): Путь к CSV-файлу для записи результатов.
    Returns:
        None
    """
    # Фильтруем результаты, оставляя только открытые порты
    open_ports = [(port, service) for port, is_open, service in results if is_open]

    # Проверяем, существует ли уже файл
    file_exists = os.path.isfile(output_file)

    # Открываем файл для добавления данных (если файла нет, он будет создан)
    with open(output_file, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Если файл не существует или пуст, записываем заголовок
        if not file_exists or csvfile.tell() == 0:
            writer.writerow(['Хост', 'IP', 'Порт', 'Статус', 'Сервис'])

        # Создаем множество для хранения уже существующих записей
        existing_ports = set()
        # Перемещаем указатель файла в начало
        csvfile.seek(0)
        reader = csv.reader(csvfile)
        # Читаем существующие записи и добавляем их в множество
        for row in reader:
            if row and row[2].isdigit():
                existing_ports.add((row[0], row[1], row[2]))

        # Формируем новые строки для записи, избегая дублирования
        new_rows = [
            [target, ip, port, 'Открыт', service]
            for port, service in open_ports
            if (target, ip, port) not in existing_ports
        ]

        # Записываем новые строки в CSV-файл
        writer.writerows(new_rows)

    logger.info(f"Результаты добавлены в файл: {output_file}")


def log_scan_results(target: str, ip: str, results: List[Tuple[int, bool, Optional[str]]]) -> None:
    """
    Логирует результаты сканирования портов.

    Args:
        target (str): Целевой хост.
        ip (str): IP-адрес целевого хоста.
        results (List[Tuple[int, bool, Optional[str]]]): Список результатов сканирования портов.
    Returns:
        None
    """
    # Фильтруем открытые порты для логирования
    open_ports = [(port, service) for port, is_open, service in results if is_open]
    # Фильтруем закрытые порты для логирования
    closed_ports = [port for port, is_open, _ in results if not is_open]

    # Логируем заголовок результатов сканирования
    logger.info(f"\n========== Результаты сканирования для {target} ({ip}) ==========")
    logger.info("Открытые порты:")

    # Логируем каждый открытый порт и его сервис
    for port, service in open_ports:
        logger.info(f"Порт {port:>5}: Открыт (Сервис: {service})")

    logger.info(f"\nВсего просканировано портов: {len(results)}")
    logger.info(f"Открытых портов: {len(open_ports)}")

    logger.info(f"Закрытых портов: {len(closed_ports)}")
    logger.info(f"=========================================================")


def print_welcome_message() -> None:
    """
    Печатает приветственное сообщение с инструкциями по использованию сканера портов.

    Returns:
        None
    """
    logger.info("Добро пожаловать в асинхронный сканер портов!")
    logger.info("Для сканирования портов укажите целевой хост.")
    logger.info("Пример использования: python main.py example.com -s 1 -e 1000 -o results.csv")
    logger.info("Для получения справки используйте флаг -h или --help")

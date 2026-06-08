# net_port_scanner/main.py

"""
Этот скрипт является основной точкой входа для асинхронного сканера портов.
Он обрабатывает аргументы командной строки, выполняет сканирование портов и обрабатывает ошибки.
"""

import argparse
import asyncio
import traceback

from config import config
from logger_config import logger
from network_utils import get_network_interfaces
from scanner import port_scanner


async def main() -> None:
    """
    Основная асинхронная функция, которая выполняет сканирование портов в зависимости от предоставленных аргументов командной строки.

    - Если целевой хост не указан, сканируются все сетевые интерфейсы текущего хоста.
    - Если целевой хост указан, сканируется только этот хост.

    Обрабатывает аргументы командной строки, вызывая соответствующие функции для сканирования портов и записи результатов.
    """
    try:
        # Создаем парсер аргументов командной строки
        parser = argparse.ArgumentParser(description="Асинхронный сканер портов")

        parser.add_argument("target", nargs='?', default=None,
                            help="Целевой хост для сканирования (например, example.com или 192.168.1.1)")

        parser.add_argument("-s", "--start", type=int, default=config.DEFAULT_START_PORT,
                            help=f"Начальный порт (по умолчанию: {config.DEFAULT_START_PORT})")

        parser.add_argument("-e", "--end", type=int, default=config.DEFAULT_END_PORT,
                            help=f"Конечный порт (по умолчанию: {config.DEFAULT_END_PORT})")

        parser.add_argument("-o", "--output", default=config.DEFAULT_OUTPUT_FILE,
                            help=f"Файл для сохранения результатов в формате CSV (по умолчанию: {config.DEFAULT_OUTPUT_FILE})")

        # Разбираем аргументы командной строки
        args = parser.parse_args()

        # Если целевой хост не указан, сканируем все сетевые интерфейсы текущего хоста
        if args.target is None:
            # Получаем список IP-адресов всех сетевых интерфейсов
            interfaces = await get_network_interfaces()
            # Сканируем порты на каждом из найденных IP-адресов
            for interface in interfaces:
                await port_scanner(interface, args.start, args.end, args.output)
        else:
            # Если целевой хост указан, сканируем порты на этом хосте
            await port_scanner(args.target, args.start, args.end, args.output)

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
    finally:
        logger.info("Процесс асинхронного сканирования портов завершен")


if __name__ == "__main__":
    try:
        # Запускаем асинхронную функцию main
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Неожиданная ошибка приложения: {error}\n{detailed_error}")

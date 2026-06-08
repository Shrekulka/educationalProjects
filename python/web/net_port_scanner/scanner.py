# net_port_scanner/scanner.py

"""
Этот модуль содержит основные функции для выполнения асинхронного сканирования портов на целевом хосте.
Функции выполняют сканирование портов, проверку состояния порта и запись результатов в CSV-файл.
"""

import asyncio
import concurrent.futures
import socket
from typing import Optional, List, Tuple, Dict

from tqdm.asyncio import tqdm

from config import config
from logger_config import logger
from network_utils import log_scan_results, write_results_to_csv

# Создаем пул потоков для выполнения блокирующих операций, таких как получение имени сервиса по порту
executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.THREAD_POOL_MAX_WORKERS)

# Кэш для хранения имен сервисов по номерам портов
service_cache: Dict[int, str] = {}


async def get_service_name(port: int) -> Optional[str]:
    """
    Получает имя сервиса по номеру порта. Использует кэш для хранения ранее полученных значений.

    Args:
        port (int): Номер порта для получения имени сервиса.

    Returns:
        Optional[str]: Имя сервиса для указанного порта, или "Unknown", если имя сервиса не удалось получить.
    """
    # Проверяем, есть ли имя сервиса в кэше
    if port in service_cache:
        # Если имя сервиса уже есть в кэше, возвращаем его
        return service_cache[port]

    # Получаем текущий цикл событий asyncio, который используется для асинхронного выполнения задач.
    loop = asyncio.get_running_loop()

    # Запускаем цикл попыток для получения имени сервиса по порту.
    for attempt in range(config.MAX_RETRIES):
        try:
            # Получаем имя сервиса, используя пул потоков для выполнения блокирующей операции
            service_name = await loop.run_in_executor(executor, socket.getservbyport, port)
            # Кэшируем полученное имя сервиса
            service_cache[port] = service_name

            # Возвращаем полученное имя сервиса, соответствующее указанному порту.
            return service_name

        except (socket.error, OSError) as e:
            logger.debug(f"Попытка {attempt + 1} не удалась при получении имени сервиса для порта {port}: {str(e)}")

            # Если попытка неудачна и это не последняя попытка, ждем перед повторной попыткой
            if attempt < config.MAX_RETRIES - 1:
                await asyncio.sleep(config.RETRY_DELAY)

    # Если не удалось получить имя сервиса после всех попыток, возвращаем "Unknown"
    logger.debug(f"Не удалось получить имя сервиса для порта {port} после {config.MAX_RETRIES} попыток.")

    # Возвращаем строку "Unknown", если имя сервиса не удалось получить
    return "Unknown"


async def check_port(ip: str, port: int) -> Tuple[int, bool, Optional[str]]:
    """
    Проверяет состояние порта на указанном IP-адресе.

    Args:
        ip (str): IP-адрес для проверки.
        port (int): Номер порта для проверки.

    Returns:
        Tuple[int, bool, Optional[str]]: Кортеж, содержащий номер порта, статус порта (открыт/закрыт),
                                         и имя сервиса, если порт открыт.
    """
    try:
        # Пытаемся установить соединение с портом
        _, writer = await asyncio.wait_for(
            # Асинхронное подключение к порту на IP-адресе
            asyncio.open_connection(ip, port),
            # Тайм-аут ожидания подключения
            timeout=config.CONNECT_TIMEOUT
        )
        # Закрываем соединение
        writer.close()
        # Ожидаем закрытия соединения.
        await writer.wait_closed()
        # Получаем имя сервиса для порта
        service = await get_service_name(port)
        # Возвращаем кортеж, содержащий информацию о проверенном порте.
        # Мы возвращаем три значения:
        # - `port`: номер проверенного порта.
        # - `True`: указывает, что соединение с портом было успешно установлено.
        # - `service`: имя сервиса, связанного с этим портом, которое было получено.
        # Если имя сервиса не удалось получить, будет возвращено значение по умолчанию "Unknown".
        return port, True, service
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        # Если соединение не удалось, возвращаем информацию о закрытом порте
        return port, False, None


async def scan_ports(target: str, start_port: int, end_port: int) -> Tuple[
    str, str, List[Tuple[int, bool, Optional[str]]]]:
    """
    Выполняет сканирование портов на целевом хосте в указанном диапазоне портов.

    Args:
        target (str): Целевой хост для сканирования.
        start_port (int): Начальный порт в диапазоне.
        end_port (int): Конечный порт в диапазоне.

    Returns:
        Tuple[str, str, List[Tuple[int, bool, Optional[str]]]]:
        Кортеж, содержащий целевой хост, IP-адрес и список результатов сканирования портов.
    """
    try:
        # Получаем IP-адрес целевого хоста
        ip_info = await asyncio.get_event_loop().getaddrinfo(target, None)
        # Извлекаем IP-адрес из информации о хосте.
        ip = ip_info[0][4][0]
        logger.info(f"Сканирование {target} ({ip})")

        # Создаем семафор для ограничения количества одновременных задач проверки портов
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_TASKS)

        async def limited_check_port(port: int) -> Tuple[int, bool, Optional[str]]:
            """
            Выполняет проверку порта с учетом семафора для ограничения количества одновременных проверок.

            Args:
                port (int): Номер порта для проверки.

            Returns:
                Tuple[int, bool, Optional[str]]: Результат проверки порта.
            """
            # Выполняем асинхронную проверку порта с использованием семафора для ограничения числа параллельных задач.
            async with semaphore:
                return await check_port(ip, port)

        # Создаем диапазон портов для сканирования
        ports = range(start_port, end_port + 1)

        # Создаем прогресс-бар для отображения прогресса сканирования
        with tqdm(total=len(ports), desc="Сканирование") as pbar:
            async def progress_check_port(port: int) -> Tuple[int, bool, Optional[str]]:
                """
                Выполняет проверку порта и обновляет прогресс-бар.

                Args:
                    port (int): Номер порта для проверки.

                Returns:
                    Tuple[int, bool, Optional[str]]: Результат проверки порта.
                """
                # Выполняем проверку порта и обновляем индикатор прогресса.
                result = await limited_check_port(port)  # Ожидаем результат проверки порта.
                pbar.update(1)                           # Обновляем индикатор прогресса на один шаг.
                return result                            # Возвращаем результат проверки порта.

            # Выполняем сканирование портов и собираем результаты
            results = await asyncio.gather(*(progress_check_port(port) for port in ports))

        # Логируем результаты сканирования
        log_scan_results(target, ip, list(results))
        # Возвращаем цель сканирования, IP-адрес и результаты в виде списка.
        return target, ip, list(results)
    except socket.gaierror:
        # Если не удалось разрешить имя хоста, логируем ошибку и возвращаем пустые результаты
        logger.error(f"Не удалось разрешить имя хоста {target}")
        return target, "", []


async def port_scanner(target: str, start_port: int, end_port: int,
                       output_file: str = config.DEFAULT_OUTPUT_FILE) -> None:
    """
    Выполняет сканирование портов на целевом хосте и сохраняет результаты в CSV-файл.

    Args:
        target (str): Целевой хост для сканирования.
        start_port (int): Начальный порт для сканирования.
        end_port (int): Конечный порт для сканирования.
        output_file (str): Путь к файлу для записи результатов (по умолчанию: config.DEFAULT_OUTPUT_FILE).

    Returns:
        None
    """
    try:
        # Выполняем сканирование портов
        target, ip, results = await scan_ports(target, start_port, end_port)

        # Если нет результатов сканирования, прерываем выполнение функции.
        if not results:
            return

        # Записываем результаты сканирования в CSV-файл
        write_results_to_csv(target, ip, results, output_file)

    except Exception as e:
        # Логируем ошибку, если сканирование не удалось
        logger.error(f"Ошибка при сканировании {target}: {str(e)}")

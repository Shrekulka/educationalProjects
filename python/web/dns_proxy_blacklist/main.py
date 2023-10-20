import logging
import socket
import threading
import time

import dns.message
import dns.query
import dns.rcode
from dnslib import DNSError

from dns_config_manager import DNSConfigManager


def handle_dns_request(request_data: bytes, client_addr: tuple, config_manager: DNSConfigManager) -> None:
    """
       Обрабатывает DNS-запросы от клиентов.

       :param request_data: Данные запроса
       :param client_addr: Адрес клиента
       :param config_manager: Менеджер конфигурации DNS
    """
    try:
        # Попытка разбора DNS-запроса из байтовых данных
        request = dns.message.from_wire(request_data)
    except Exception as inner_e:
        print(f"Error parsing DNS request: {inner_e}")
        return

    # Извлечение домена из запроса
    domain = str(request.question[0].name).lower().strip(".")
    response = None

    # Проверка, находится ли домен в черном списке
    if domain in config_manager.get_blacklist():
        print(f"Domain {domain} is in the blacklist")

        # Получение настроек для блокированных доменов из конфигурации
        default_blocked_response_code = config_manager.config['custom_responses']['default_blocked_response_code']
        default_blocked_response_text = config_manager.config['custom_responses']['default_blocked_response_text']

        print(f"Default Blocked Response Code: {default_blocked_response_code}")
        print(f"Default Blocked Response Text: {default_blocked_response_text}")

        response_config = {}

        # Проверка наличия настроек для данного домена
        if domain in config_manager.get_blocked_responses():
            response_config = config_manager.get_blocked_responses()[domain]
        else:
            # Создание ответа для блокированных доменов
            response = dns.message.make_response(request)
            response.set_rcode(dns.rcode.from_text(default_blocked_response_code))
            response_config['response_text'] = default_blocked_response_text
            response_config['record_type'] = 'TXT'

        # Отправка ответа клиенту
        server_socket.sendto(response.to_wire(), client_addr)

        # Журналирование действий
        unique_id = str(int(time.time()))
        log_message = f"[{unique_id}] Domain {domain} is in the blacklist. Response: {response_config['response_text']}"
        logging.info(log_message)

        print(f"Response for {domain}: {response_config['response_text']}")

    else:
        print(f"Domain {domain} is not in the blacklist")
        # Создание ответа для доменов, не включенных в черный список
        response = dns.message.make_response(request)
        response.set_rcode(dns.rcode.NOERROR)

        try:
            # Получение адреса удаленного DNS-сервера из конфигурации
            upstream_dns_server = config_manager.get_config_value('server', 'upstream_dns')
            # Отправка DNS-запроса на удаленный DNS-сервер
            upstream_response = send_request_to_upstream(request, upstream_dns_server)
        except DNSError as e:
            logging.error(f"Error querying upstream DNS: {e}")
            return

        # Копирование ответа от удаленного DNS-сервера в ответ клиенту
        response.answer = upstream_response.answer
        server_socket.sendto(response.to_wire(), client_addr)


def send_request_to_upstream(request: dns.message.Message, upstream_dns_server: str) -> dns.message.Message:
    """
       Отправляет DNS-запрос к удаленному DNS-серверу.

       :param request: DNS-запрос
       :param upstream_dns_server: Адрес удаленного DNS-сервера
       :return: DNS-ответ
    """
    try:
        upstream_response = dns.query.udp(request, upstream_dns_server)
    except dns.exception.DNSException as e:
        raise DNSError("Error querying upstream DNS") from e

    return upstream_response


def main() -> None:
    """
    Главная функция программы для запуска DNS-прокси-сервера.

    Функция выполняет следующие шаги:
    1. Настройка логирования в файл dns_server.log.
    2. Загрузка конфигурации DNS из файла 'dns_server.conf'.
    3. Получение настроек сервера, таких как IP-адрес и порт, из конфигурации.
    4. Создание сокета для прослушивания DNS-запросов на указанном IP-адресе и порту.
    5. Бесконечный цикл, в котором сервер ожидает запросы от клиентов и обрабатывает их в отдельных потоках.

    :return: None
    """
    # Настройка логирования
    logging.basicConfig(filename='dns_server.log', level=logging.INFO)
    CONFIG_FILE = 'dns_server.conf'
    print(f"CONFIG_FILE: {CONFIG_FILE}")
    print("Before creating DNSConfigManager instance")

    try:
        # Создание экземпляра менеджера конфигурации DNS
        config_manager = DNSConfigManager(CONFIG_FILE)
        print("DNSConfigManager instance created successfully")

        # Загрузка конфигурации из файла
        if not config_manager.load_config():
            print("Config loading failed")
        else:
            print("Config loaded successfully")

        # Получение IP-адреса и порта сервера из конфигурации
        server_ip = config_manager.get_config_value('server', 'ip_address')
        server_port = int(config_manager.get_config_value('server', 'port'))

        print(f"Server IP: {server_ip}")
        print(f"Server Port: {server_port}")

        # Создание и настройка сокета для прослушивания DNS-запросов
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((server_ip, server_port))

        while True:
            try:
                data, addr = server_socket.recvfrom(512)
                client_thread = threading.Thread(target=handle_dns_request, args=(data, addr, config_manager))
                client_thread.start()
            except KeyboardInterrupt:
                print("DNS server interrupted by user (Ctrl+C). Exiting...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("After trying to load the config")


if __name__ == "__main__":
    main()

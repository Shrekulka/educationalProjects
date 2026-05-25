# backend/sim_app/management/commands/get_sim_info.py

"""
Команда Django для получения информации о SIM из SIM-банка
для указанного устройства с помощью UDP-запроса и вывода результатов в формате JSON.
"""

########################################################################################################################
# import socket
# import hashlib
# from datetime import datetime
# import json
# import xmltodict
# from django.core.management.base import BaseCommand
#
# HOST = 'dinstar.dzencode.net'
# PORT = 3030
#
# domain = 'dzencode'
# user = 'testAPI'
# authPwd = 'sdff3432SDFfsd343!3'
#
# def XMLtoJson(data: bytes) -> dict:
#     return xmltodict.parse(data.decode().strip('\x00'))
#
# class Command(BaseCommand):
#     help = 'Get SIM info from sim bank'
#
#     def add_arguments(self, parser):
#         parser.add_argument('device_id', type=int, help='Device ID')
#
#     def handle(self, *args, **kwargs):
#         device_id = kwargs['device_id']
#         sn = str(round(datetime.now().timestamp()))
#         timestamp = datetime.now().timestamp()
#
#         cmd = 'GetSimInfo'
#         str_to_hash = f"request{sn}{domain}{user}{cmd}{timestamp}{authPwd}"
#         authInfo = hashlib.md5(str_to_hash.encode()).hexdigest()
#         request = f"""
#         <?xml version="1.0" encoding="utf-8"?>
#         <simsrv version="1.0" msg_type="request">
#         <header>
#         <param name="SN" value="{sn}" />
#         <param name="Domain" value="{domain}" />
#         <param name="User" value="{user}" />
#         <param name="Cmd" value="{cmd}" />
#         <param name="Retries" value="0" />
#         <param name="Timeout" value="5000" />
#         <param name="Timestamp" value="{timestamp}" />
#         <param name="AuthInfo" value="{authInfo}" />
#         </header>
#         <{cmd}>
#         <param name="DeviceId" value="{device_id}" />
#         <param name="PortType" value="BKP" />
#         <param name="BeginPortNo" value="3" />
#         <param name="MaxGetCount" value="10" />
#         </{cmd}>
#         </simsrv>
#         """
#
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#             s.sendto(request.encode(), 0, (HOST, PORT))
#             response_data = s.recv(81920)
#             response_json = XMLtoJson(response_data)
#             pretty_json = json.dumps(response_json, indent=4, ensure_ascii=False)
#             self.stdout.write(self.style.SUCCESS(pretty_json))
########################################################################################################################

import json

from django.core.management.base import BaseCommand

from sim_app.utils.sim_bank_utils import generate_request, send_request


class Command(BaseCommand):
    """
    Команда Django для получения информации о SIM из SIM-банка.

    Эта команда отправляет запрос на сервер SIM-банка для получения
    информации о SIM для указанного устройства и выводит результат
    в формате JSON.

    Атрибуты:
           help (str): Описание функциональности команды.
    """

    help = 'Получение информации о SIM из SIM-банка'

    def add_arguments(self, parser) -> None:
        """
        Добавляет аргументы командной строки для команды.

        Args:
            parser: Объект парсера аргументов командной строки.

        Возвращает:
            None
        """
        # Добавляет аргумент командной строки для идентификатора устройства.
        parser.add_argument('device_id', type=int, help='Device ID')

    def handle(self, *args: str, **kwargs: dict) -> None:
        """
        Обрабатывает выполнение команды.

        Этот метод отправляет запрос на сервер SIM-банка для получения
        информации о SIM, обрабатывает ответ и выводит результат в
        отформатированном JSON.

        Args:
            *args: Позиционные аргументы (не используются).
            **kwargs: Именованные аргументы. Ожидается 'device_id'.

        Возвращает:
            None
        """
        # Получаем идентификатор устройства из аргументов команды
        device_id = kwargs['device_id']

        # Формируем дополнительные параметры для XML-запроса
        additional_params = f"""
            <param name="DeviceId" value="{device_id}" />   # Устанавливаем идентификатор устройства
            <param name="PortType" value="BKP" />           # Устанавливаем тип порта, здесь это "BKP" (Backup)
            <param name="BeginPortNo" value="3" />          # Устанавливаем начальный номер порта
            <param name="MaxGetCount" value="10" />         # Устанавливаем максимальное количество получаемых элементов
        """

        # Генерируем XML-запрос, используя команду 'GetSimInfo' и дополнительные параметры
        request = generate_request('GetSimInfo', additional_params)

        # Отправляем запрос на сервер и получаем ответ в формате JSON
        response_json = send_request(request)

        # Преобразуем ответ JSON в форматированную строку для удобного отображения
        pretty_json = json.dumps(response_json, indent=4, ensure_ascii=False)

        # Выводим форматированный JSON в консоль
        self.stdout.write(self.style.SUCCESS(pretty_json))

########################################################################################################################
# Для выполнения команды используем:
# python manage.py get_sim_info [int]
########################################################################################################################

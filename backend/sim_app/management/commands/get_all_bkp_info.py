# backend/sim_app/management/commands/get_all_bkp_info.py

"""
Команда Django для получения информации о резервных копиях (BKP) из SIM-банка
для всех портов от 0 до 127 для указанного устройства и вывода результатов в формате JSON.
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
#     help = 'Get Bkp info from sim bank'
#
#     def add_arguments(self, parser):
#         parser.add_argument('device_id', type=int, help='Device ID')
#
#     def handle(self, *args, **kwargs):
#         device_id = kwargs['device_id']
#         sn = str(round(datetime.now().timestamp()))
#         timestamp = datetime.now().timestamp()
#
#         cmd = 'GetBkpInfo'
#         str_to_hash = f"request{sn}{domain}{user}{cmd}{timestamp}{authPwd}"
#         authInfo = hashlib.md5(str_to_hash.encode()).hexdigest()
#         request = f"""
#             <?xml version="1.0" encoding="utf-8"?>
#             <simsrv version="1.0" msg_type="request">
#             <header>
#             <param name="SN" value="{sn}" />
#             <param name="Domain" value="{domain}" />
#             <param name="User" value="{user}" />
#             <param name="Cmd" value="{cmd}" />
#             <param name="Retries" value="0" />
#             <param name="Timeout" value="5000" />
#             <param name="Timestamp" value="{timestamp}" />
#             <param name="AuthInfo" value="{authInfo}" />
#             </header>
#             <{cmd}>
#             <param name="DeviceId" value="{device_id}" /> // Укажите DeviceId устройства
#             <param name="PortType" value="BKP" /> // Тип порта
#             <param name="BeginPortNo" value="0" /> // Номер порта, с которого начинается запрос
#             <param name="MaxGetCount" value="1" /> // Максимальное количество портов для получения информации # count = 28, 32666 bytes
#             </{cmd}>
#             </simsrv>
#             """
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#             s.sendto(request.encode(), 0, (HOST, PORT))
#             response_data = s.recv(81920)
#             response_json = XMLtoJson(response_data)
#             pretty_json = json.dumps(response_json, indent=4, ensure_ascii=False)
#             self.stdout.write(self.style.SUCCESS(pretty_json))
########################################################################################################################
"""
Нужно получить DeviceId, BeginPortNo, PortNo, AdminStatus, RunStatus, WorkStatus, SimNumber, DynamicImei,
BindDeviceId, BindPortType, BindPortNo
"""

import json

from django.core.management.base import BaseCommand

from sim_app.utils.sim_bank_utils import generate_request, send_request

"""
GetGwpInfo - сюда надо передавать только DeviceId Шлюза, если передать сюда DeviceId из GetSimInfo а то получим ошибку
"""


########################################################################################################################
class Command(BaseCommand):
    """
        Команда управления Django для получения информации о резервных копиях (BKP) из SIM-банка.

        Эта команда генерирует XML-запросы для получения информации о резервных копиях
        с сервера SIM-банка, обрабатывает ответы и выводит отформатированное представление
        данных в формате JSON.

        Атрибуты:
            help (str): Описание функциональности команды.
        """

    help = 'Получение информации о резервных копиях из SIM-банка'

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

        Этот метод генерирует запросы для получения информации о резервных копиях
        для указанного устройства, отправляет запросы на сервер SIM-банка, обрабатывает
        ответы, и затем выводит отформатированный JSON с данными о резервных копиях.

        Аргументы:
            *args: Позиционные аргументы, переданные команде (не используются).
            **kwargs: Именованные аргументы, переданные команде. Ожидается, что
                      `kwargs` будет содержать `device_id`.

        Возвращает:
            None
        """
        # Получаем идентификатор устройства из аргументов команды
        device_id = kwargs['device_id']

        # Создаем пустой список для хранения информации о резервных копиях
        all_devices = []

        # Начальный номер порта для запроса
        begin_port_no = 0

        # Запускаем цикл для обработки всех портов до 128 включительно
        while begin_port_no < 128:
            # Формируем дополнительные параметры для XML-запроса
            additional_params = f"""
                <param name="DeviceId" value="{device_id}" /> 
                <param name="PortType" value="BKP" /> 
                <param name="BeginPortNo" value="{begin_port_no}" /> 
                <param name="MaxGetCount" value="1" /> 
                """

            # Генерируем XML-запрос для получения информации о резервных копиях
            request = generate_request('GetBkpInfo', additional_params)

            # Отправляем запрос и получаем ответ от сервера в формате JSON
            response_json = send_request(request)

            # Извлекаем информацию о резервных копиях из ответа сервера
            devices = response_json['simsrv'].get('GetBkpInfo', {}).get('param', [])

            # Преобразуем параметры устройства в словарь для удобного доступа
            device_info = {param['@name']: param['@value'] for param in devices}

            # Добавляем информацию о резервной копии в список
            all_devices.append(
                {
                    'DeviceId': device_info.get('DeviceId'),          # Идентификатор устройства
                    'BeginPortNo': device_info.get('BeginPortNo'),    # Начальный номер порта
                    'PortNo': device_info.get('PortNo'),              # Номер порта
                    'AdminStatus': device_info.get('AdminStatus'),    # Статус администратора
                    'RunStatus': device_info.get('RunStatus'),        # Рабочий статус
                    'WorkStatus': device_info.get('WorkStatus'),      # Рабочее состояние
                    'SimNumber': device_info.get('SimNumber'),        # Номер SIM-карты
                    'DynamicImei': device_info.get('DynamicImei'),    # Динамический IMEI
                    'BindDeviceId': device_info.get('BindDeviceId'),  # Идентификатор связанного устройства
                    'BindPortType': device_info.get('BindPortType'),  # Тип связанного порта
                    'BindPortNo': device_info.get('BindPortNo')       # Номер связанного порта
                }
            )

            # Переходим к следующему номеру порта
            begin_port_no += 1

        # Преобразуем список информации о резервных копиях в формат JSON с красивым выводом
        pretty_json = json.dumps(all_devices, indent=4, ensure_ascii=False)

        # Выводим отформатированный JSON на экран
        self.stdout.write(self.style.SUCCESS(pretty_json))

########################################################################################################################
# Для выполнения команды используем:
# python manage.py get_all_bkp_info 3
########################################################################################################################

# backend/sim_app/management/commands/get_gwp_info.py

"""
Команда Django для получения информации о GWP (Gateway Ports) из SIM-банка
для указанного устройства и вывода результатов в формате JSON.
"""

import json

from django.core.management.base import BaseCommand

from sim_app.utils.sim_bank_utils import generate_request, send_request

"""
GetGwpInfo - сюда надо передавать только DeviceId Шлюза, если передать сюда DeviceId из GetSimInfo а то получим ошибку
"""


class Command(BaseCommand):
    """
       Команда управления Django для получения информации о GWP (Gateway Ports) из SIM-банка.

       Эта команда отправляет запрос на сервер SIM-банка для получения информации
       о портах GWP для указанного устройства, обрабатывает ответ и выводит результат
       в отформатированном JSON.

       Атрибуты:
           help (str): Описание функциональности команды.
       """

    help = 'Получение информации о GWP из SIM-банка'

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

        Этот метод генерирует запрос для получения информации о портах GWP
        для указанного устройства, отправляет запрос на сервер SIM-банка, обрабатывает
        ответ и выводит отформатированный JSON с данными о портах GWP.

        Аргументы:
            *args: Позиционные аргументы, переданные команде (не используются).
            **kwargs: Именованные аргументы, переданные команде. Ожидается, что
                      `kwargs` будет содержать `device_id`.

        Возвращает:
            None
        """
        # Получаем идентификатор устройства из аргументов команды
        device_id = kwargs['device_id']

        # cmd = 'GetGwpInfo'

        # Формируем дополнительные параметры для XML-запроса
        additional_params = f"""
                <param name="DeviceId" value="{device_id}" />
                <param name="PortType" value="GWP" />
                <param name="BeginPortNo" value="0" />
                <param name="MaxGetCount" value="16" />
                """

        # Генерируем XML-запрос для получения информации о портах GWP
        request = generate_request('GetGwpInfo', additional_params)

        # Отправляем запрос и получаем ответ от сервера в формате JSON
        response_json = send_request(request)

        # Извлекаем информацию о портах GWP из ответа сервера
        devices = response_json['simsrv'].get('GetGwpInfo', [])

        # Формируем список словарей
        filtered_devices = [
            {
                'BindPortNo': device['param'][2]['@value'],     # Номер порта GWP
                'AdminStatus': device['param'][7]['@value'],    # Статус администратора порта
                'RunStatus': device['param'][8]['@value'],      # Рабочий статус порта
                'SmsStatus': device['param'][9]['@value'],      # Статус SMS для порта
                'UssdStatus': device['param'][10]['@value'],    # Статус USSD для порта
                'CallStatus': device['param'][11]['@value'],    # Статус звонков для порта
                'SignalLevel': device['param'][16]['@value'],   # Уровень сигнала порта
                'BindDeviceId': device['param'][17]['@value'],  # Идентификатор связанного устройства
                'BindSimImsi': device['param'][21]['@value']    # IMSI SIM-карты, связанной с портом
            }
            for device in devices  # Повторяем для каждого устройства в списке
        ]

        # Преобразуем список информации о портах GWP в формат JSON с красивым выводом
        pretty_json = json.dumps(filtered_devices, indent=4, ensure_ascii=False)

        # Выводим отформатированный JSON на экран
        self.stdout.write(self.style.SUCCESS(pretty_json))

########################################################################################################################
# Для выполнения команды используем:
# python manage.py get_gwp_info 2
########################################################################################################################


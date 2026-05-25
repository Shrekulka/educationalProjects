# backend/sim_app/management/commands/set_bkp_info.py

"""
Команда Django для установки информации BKP (Backup) на указанном устройстве в SIM-банке.
Команда отправляет XML-запрос для изменения состояния порта BKP и выводит ответ от сервера в формате JSON.
"""

########################################################################################################################
# from django.core.management.base import BaseCommand
# import json
# from sim_app.utils.sim_bank_utils import generate_request, send_request
#
# class Command(BaseCommand):
#     help = 'Get GWP info from sim bank'
#
#     def SetBkpInfo(device_id: int):
#
#         cmd = 'SetBkpInfo'
#         str = f"request{sn}{domain}{user}{cmd}{timestamp}{authPwd}"
#         authInfo = hashlib.md5(str.encode()).hexdigest()
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
#             <param name="PortNo" value="126" /> // Номер порта, с которого начинается запрос
#             <param name="AdminStatus" value="DISABLED" /> // Максимальное количество портов для получения информации # count = 28, 32666 bytes
#             </{cmd}>
#             </simsrv>
#             """
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#             s.sendto(request.encode(), (HOST, PORT))
#             print(XMLtoJson(s.recv(81920)))
#выключить порт на симбанке. но тут правда больше функций(не забыть спросить )
########################################################################################################################

from django.core.management.base import BaseCommand
from sim_app.utils.sim_bank_utils import generate_request, send_request


class Command(BaseCommand):
    """
    Django management команда для установки информации BKP на устройстве в SIM-банке.

    Эта команда отправляет XML-запрос на SIM-банк для изменения состояния порта BKP на указанном устройстве.

    Атрибуты:
        help (str): Описание команды.
    """

    help = 'Устанавливает информацию BKP для указанного устройства в SIM-банке'

    def add_arguments(self, parser) -> None:
        """
        Добавляет аргумент командной строки для идентификатора устройства.

        Args:
            parser: Объект парсера аргументов командной строки.

        Возвращает:
            None
        """
        # Добавляем аргумент командной строки для идентификатора устройства (device_id)
        parser.add_argument('device_id', type=int, help='Device ID')

    def handle(self, *args: str, **kwargs: dict) -> None:
        """
        Выполняет основную логику команды.

        Этот метод вызывает метод `set_bkp_info`, передавая в него идентификатор устройства.

        Args:
            *args: Позиционные аргументы (не используются).
            **kwargs: Именованные аргументы. Ожидается 'device_id'.

        Возвращает:
            None
        """
        # Получаем идентификатор устройства из аргументов
        device_id = kwargs['device_id']

        # Вызываем метод для установки информации BKP для данного устройства
        self.set_bkp_info(device_id)

    def set_bkp_info(self, device_id: int) -> None:
        """
        Отправляет запрос на SIM-банк для обновления информации о порте BKP.

        Args:
            device_id (int): Идентификатор устройства, для которого необходимо установить информацию BKP.

        Возвращает:
            None
        """
        # Устанавливаем команду для SIM-банка
        cmd = 'SetBkpInfo'

        # Формируем дополнительные параметры для XML-запроса
        additional_params = f"""
            <param name="DeviceId" value="{device_id}" />  # Устанавливаем идентификатор устройства
            <param name="PortType" value="BKP" />          # Устанавливаем тип порта (BKP)
            <param name="PortNo" value="126" />            # Указываем номер порта
            <param name="AdminStatus" value="DISABLED" />  # Устанавливаем статус администратора (DISABLED)
        """

        # Генерируем XML-запрос, используя команду и дополнительные параметры
        request = generate_request(cmd, additional_params)

        # Отправляем запрос на сервер SIM-банка и получаем ответ в формате словаря
        response = send_request(request)

        # Выводим ответ в консоль в виде JSON
        self.stdout.write(self.style.SUCCESS(response))

########################################################################################################################
# Для выполнения команды используем:
# python manage.py set_bkp_info [device_id]
########################################################################################################################


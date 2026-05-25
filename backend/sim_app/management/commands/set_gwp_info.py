# # backend/sim_app/management/commands/set_gwp_info.py
#
# """
# Команда Django для установки информации о GWP (Gateway Ports) в SIM-банке.
# Отправляет запрос на сервер SIM-банка для изменения состояния порта GWP
# и выводит результат в формате JSON.
# """
#
# from django.core.management.base import BaseCommand
#
# from sim_app.utils.sim_bank_utils import generate_request, send_request
#
#
# class Command(BaseCommand):
#     """
#     Команда Django для установки информации о GWP (Gateway Ports) в SIM-банке.
#
#     Эта команда отправляет XML-запрос на сервер SIM-банка для установки состояния порта GWP,
#     обрабатывает ответ и выводит результат в формате JSON.
#
#     Атрибуты:
#         help (str): Описание функциональности команды.
#     """
#
#     help = 'Установка информации о GWP в SIM-банке'
#
#     def add_arguments(self, parser) -> None:
#         """
#         Добавляет аргументы командной строки для команды.
#
#         Args:
#             parser: Объект парсера аргументов командной строки.
#
#         Возвращает:
#             None
#         """
#         parser.add_argument('device_id', type=int, help='ID устройства (шлюз)')
#         parser.add_argument('port_no', type=int, help='Номер порта на шлюзе')
#         parser.add_argument('bind_device_id', type=int, help='ID устройства (SIM-банк)')
#         parser.add_argument('bind_port_no', type=int, help='Номер порта на SIM-банке')
#         parser.add_argument('bind_port_uuid', type=str, help='UUID порта на SIM-банке')
#
#     def handle(self, *args: str, **kwargs: dict) -> None:
#         """
#         Обрабатывает выполнение команды.
#
#         Этот метод генерирует запрос для установки информации о порте GWP,
#         отправляет запрос на сервер SIM-банка, обрабатывает ответ и выводит
#         отформатированный JSON с результатами.
#
#         Аргументы:
#             *args: Позиционные аргументы, переданные команде (не используются).
#             **kwargs: Именованные аргументы, переданные команде. Ожидается, что
#                       `kwargs` будут содержать `device_id`, `port_no`, `bind_device_id`,
#                       `bind_port_no` и `bind_port_uuid`.
#
#         Возвращает:
#             None
#         """
#         device_id = kwargs['device_id']
#         port_no = kwargs['port_no']
#         bind_device_id = kwargs['bind_device_id']
#         bind_port_no = kwargs['bind_port_no']
#         bind_port_uuid = kwargs['bind_port_uuid']
#
#         # Формируем дополнительные параметры для XML-запроса
#         additional_params = f"""
#             <param name="DeviceId" value="{device_id}" />
#             <param name="PortType" value="GWP" />
#             <param name="PortNo" value="{port_no}" />
#             <param name="AdminStatus" value="DISABLED" />
#             <param name="BindDeviceId" value="{bind_device_id}" />
#             <param name="BindPortType" value="BKP" />
#             <param name="BindPortNo" value="{bind_port_no}" />
#             <param name="BindPortUuid" value="{bind_port_uuid}" />
#             """
#
#         # Генерируем XML-запрос
#         request = generate_request('SetGwpInfo', additional_params)
#
#         # Отправляем запрос и получаем ответ от сервера
#         response = send_request(request)
#
#         # Выводим ответ на экран в формате JSON
#         self.stdout.write(self.style.SUCCESS(response))
#
#
#
# ########################################################################################################################
# # Для выполнения команды используем:
#
# ########################################################################################################################
#

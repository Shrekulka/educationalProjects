#
#
#
# """
#
#     Файл для тестов различных конфигураций, в релизе удалить
#
# """
#
#
#
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
#             filtered_devices = [
#                 {
#                     'DeviceId': device['param'][0]['@value'],
#                     'BeginPortNo': device['param'][2]['@value'],
#                     'PortNo': device['param'][5]['@value'],
#                     'AdminStatus': device['param'][7]['@value'],
#                     'RunStatus': device['param'][8]['@value'],
#                     'WorkStatus': device['param'][9]['@value'],
#                     'SimNumber': device['param'][18]['@value'],
#                     'DynamicImei': device['param'][20]['@value'],
#                     'BindDeviceId': device['param'][22]['@value'],
#                     'BindPortType': device['param'][23]['@value'],
#                     'BindPortNo': device['param'][24]['@value'],
#                 }
#                 for device in devices
#             ]
#
#             pretty_json = json.dumps(response_json, indent=4, ensure_ascii=False)
#             self.stdout.write(self.style.SUCCESS(pretty_json))
#
#
# #   нужно получить DeviceId, BeginPortNo, PortNo, AdminStatus, RunStatus, WorkStatus, SimNumber,
# #   DynamicImei, BindDeviceId, BindPortType, BindPortNo
#
# {
#                 'DeviceId': device['param'][0]['@value'],
#                 'BeginPortNo': device['param'][2]['@value'],
#                 'PortNo': device['param'][5]['@value'],
#                 'AdminStatus': device['param'][7]['@value'],
#                 'RunStatus': device['param'][8]['@value'],
#                 'WorkStatus': device['param'][9]['@value'],
#                 'SimNumber': device['param'][18]['@value'],
#                 'DynamicImei': device['param'][20]['@value'],
#                 'BindDeviceId': device['param'][22]['@value'],
#                 'BindPortType': device['param'][23]['@value'],
#                 'BindPortNo': device['param'][24]['@value'],
#             }
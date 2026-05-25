# backend/sim_app/management/commands/get_device_info.py

"""
Переделать остальные по образу и подобию (учти нужные фильтры)
"""

import json
from django.core.management.base import BaseCommand

from sim_app.utils.sim_bank_utils import generate_request, send_request


class Command(BaseCommand):
    """
       Команда управления Django для получения информации об устройствах из SIM-банка.

       Эта команда генерирует XML-запрос для получения информации об устройствах
       с сервера SIM-банка, обрабатывает ответ и выводит отформатированное
       представление данных об устройствах в формате JSON.

       Атрибуты:
           help (str): Описание функциональности команды.
       """

    help = 'Получение информации об устройствах из SIM-банка'

    def handle(self, *args: str, **kwargs: dict) -> None:
        """
        Обрабатывает выполнение команды.

        Этот метод генерирует запрос для получения информации об устройствах,
        отправляет его на сервер SIM-банка, обрабатывает ответ сервера для
        извлечения и форматирования данных об устройствах, а затем выводит
        отформатированный JSON в консоль.

        Аргументы:
            *args: Позиционные аргументы, переданные команде (не используются).
            **kwargs: Именованные аргументы, переданные команде (не используются).

        Возвращает:
            None
        """
        # Создание XML-запроса для получения информации об устройствах
        request = generate_request('GetDeviceInfo', """
            <param name="BeginDeviceId" value="0" />
            <param name="MaxGetCount" value="16" />
        """)

        # Отправка запроса на сервер и получение ответа
        response_json = send_request(request)

        # Извлечение списка устройств из ответа
        devices = response_json['simsrv'].get('GetDeviceInfo', [])

        # Фильтрация и преобразование данных об устройствах
        filtered_devices = [
            {
                'DeviceId': device['param'][3]['@value'],
                'DeviceAlias': device['param'][5]['@value'],
                'MaxPortCount': device['param'][7]['@value'],
                'AdminStatus': device['param'][8]['@value'],
                'RunStatus': device['param'][9]['@value']
            }
            for device in devices
        ]

        # Преобразование отфильтрованных данных в формат JSON с красивым выводом
        pretty_json = json.dumps(filtered_devices, indent=4, ensure_ascii=False)

        # Вывод отформатированного JSON на экран
        self.stdout.write(self.style.SUCCESS(pretty_json))

########################################################################################################################
# Для выполнения команды используем:
# python manage.py get_device_info
########################################################################################################################

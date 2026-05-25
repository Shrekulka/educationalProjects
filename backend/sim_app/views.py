# backend/sim_app/views.py

from django.http import JsonResponse

from .management.commands.get_device_info import Command as GetDeviceInfoCommand
from .management.commands.get_gwp_info import Command as GetGwpInfoCommand
from .management.commands.get_sim_info import Command as GetSimInfoCommand


# Получение информации об устройстве
########################################################################################################################
def get_device_info_view(request):
    # Создаем экземпляр команды для получения информации об устройстве
    command = GetDeviceInfoCommand()

    # Выполняем команду и получаем ответ
    response = command.handle()

    # Возвращаем ответ в формате JSON
    return JsonResponse({'response': response})


########################################################################################################################

# Получение информации о GWP по ID устройства
########################################################################################################################
def get_gwp_info_view(request, device_id):
    # Создаем экземпляр команды для получения информации о GWP
    command = GetGwpInfoCommand()

    # Выполняем команду, передав ID устройства, и получаем ответ
    response = command.handle(device_id=device_id)

    # Возвращаем ответ в формате JSON
    return JsonResponse({'response': response})


########################################################################################################################

# Получение информации о SIM-карте по ID устройства
########################################################################################################################
def get_sim_info_view(request, device_id):
    # Создаем экземпляр команды для получения информации о SIM-карте
    command = GetSimInfoCommand()

    # Выполняем команду, передав ID устройства, и получаем ответ
    response = command.handle(device_id=device_id)

    # Возвращаем ответ в формате JSON
    return JsonResponse({'response': response})
########################################################################################################################

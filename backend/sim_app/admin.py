# backend/sim_app/admin.py

from django.contrib import admin
from django.shortcuts import render

from .management.commands.get_device_info import Command as GetDeviceInfoCommand
from .management.commands.get_gwp_info import Command as GetGwpInfoCommand
from .management.commands.get_sim_info import Command as GetSimInfoCommand
from .models import DeviceInfo, GwpInfo, SimInfo


@admin.register(DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        command = GetDeviceInfoCommand()
        response = command.handle()
        context = {
            'device_info': response,
        }
        return super().changelist_view(request,'admin/device_info_changelist.html',  extra_context=context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GwpInfo)
class GwpInfoAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # Получаем список всех устройств
        device_command = GetDeviceInfoCommand()
        devices = device_command.handle()

        # Получаем выбранный device_id из GET-параметра или используем первое устройство по умолчанию
        device_id = request.GET.get('device_id', devices[0]['param'][3]['@value'] if devices else None)

        if device_id:
            command = GetGwpInfoCommand()
            response = command.handle(device_id=device_id)
        else:
            response = "Устройства не найдены"

        context = {
            'gwp_info': response,
            'device_id': device_id,
            'devices': devices,
        }
        return render(request, 'admin/gwp_info_changelist.html', context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SimInfo)
class SimInfoAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # Получаем список всех устройств
        device_command = GetDeviceInfoCommand()
        devices = device_command.handle()

        # Получаем выбранный device_id из GET-параметра или используем первое устройство по умолчанию
        device_id = request.GET.get('device_id', devices[0]['param'][3]['@value'] if devices else None)

        if device_id:
            command = GetSimInfoCommand()
            response = command.handle(device_id=device_id)
        else:
            response = "Устройства не найдены"

        context = {
            'sim_info': response,
            'device_id': device_id,
            'devices': devices,
        }
        return render(request, 'admin/sim_info_changelist.html', context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

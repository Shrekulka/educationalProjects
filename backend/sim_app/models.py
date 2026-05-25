# backend/sim_app/models.py

from django.db import models


# Определение модели DeviceInfo
class DeviceInfo(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Информация об устройстве'
        verbose_name_plural = 'Информация об устройствах'



# Определение модели GwpInfo
class GwpInfo(models.Model):
    class Meta:
        managed = False  # Эта модель не будет управляться Django (не будет создавать таблицу в базе данных)
        verbose_name = 'Информация о GWP'         # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'Информация о GWP'  # Человекочитаемое имя модели во множественном числе


# Определение модели SimInfo
class SimInfo(models.Model):
    class Meta:
        managed = False  # Эта модель не будет управляться Django (не будет создавать таблицу в базе данных)
        verbose_name = 'Информация о SIM'         # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'Информация о SIM'  # Человекочитаемое имя модели во множественном числе

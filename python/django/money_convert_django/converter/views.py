# money_convert_django/converter/views.py

import logging
import ssl
from decimal import Decimal, InvalidOperation

import aiohttp
import requests
from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import CurrencyConverterForm
from .models import ConversionHistory

logger = logging.getLogger(__name__)


async def get_currency_rates():
    """
        Асинхронная функция для получения курсов валют с внешнего API.

        Возвращает:
            dict: Словарь с курсами валют, полученный из API.

        Исключения:
            requests.RequestException: В случае ошибки при запросе к API.
    """
    # Асинхронно получаем данные из кэша
    currencies = await sync_to_async(cache.get)('currencies')

    # Если курсы валют не найдены в кэше
    if not currencies:
        # Создаем SSL контекст без проверки сертификатов
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        try:
            # Устанавливаем соединение с API через асинхронную сессию aiohttp
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                # Отправляем GET запрос к API для получения курсов валют
                async with session.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10) as response:
                    # Если запрос успешен (статус 200)
                    if response.status == 200:
                        # Получаем данные в формате JSON
                        data = await response.json()
                        # Извлекаем курсы валют из полученных данных
                        currencies = data.get('rates', {})
                        # Кэшируем курсы валют на 5 минут
                        await sync_to_async(cache.set)('currencies', currencies, 60 * 5)
                    else:
                        # Если запрос неудачен, устанавливаем пустой словарь курсов
                        currencies = {}
        except requests.RequestException as e:
            # Логируем ошибку запроса к API
            logger.error(f"Ошибка при получении курсов валют: {str(e)}")
            # Устанавливаем пустой словарь курсов
            currencies = {}

    # Возвращаем словарь с курсами валют (может быть пустым)
    return currencies


@require_http_methods(["GET", "POST"])
async def money_convert(request):
    """
        Представление для конвертации валют.

        GET-запрос:
            Отображает форму для конвертации валюты.

        POST-запрос:
            Обрабатывает данные формы для конвертации и сохраняет историю конвертации в базу данных.

        Контекст:
            form (CurrencyConverterForm): Форма для конвертации валют.
            currencies (dict): Словарь с текущими курсами валют.
            converted_amount (Decimal or None): Сумма после конвертации, если конвертация прошла успешно.
            from_amount (Decimal or None): Исходная сумма для конвертации.
            from_curr (str or None): Исходная валюта.
            to_curr (str or None): Целевая валюта.

        Возвращает:
            HttpResponse: Отображает шаблон 'converter/currency_converter.html' с контекстом.
    """
    # Получаем текущие курсы валют из внешнего API
    currencies = await get_currency_rates()

    # Если не удалось получить курсы валют, выводим сообщение об ошибке
    if not currencies:
        error_message = "Не удалось получить курсы валют. Пожалуйста, попробуйте позже."
        return await sync_to_async(render)(request, 'converter/currency_converter.html',
                                           {'error_message': error_message})

    # Если запрос пришел методом POST, обрабатываем данные формы конвертации
    if request.method == 'POST':
        # Инициализируем форму конвертации валют с переданными данными POST и текущими курсами
        form = await sync_to_async(CurrencyConverterForm)(request.POST, currencies=currencies)

        # Если форма валидна, проводим конвертацию валют
        if await sync_to_async(form.is_valid)():
            from_amount = form.cleaned_data['from_amount']
            from_curr = form.cleaned_data['from_curr']
            to_curr = form.cleaned_data['to_curr']

            try:
                # Вычисляем конвертированную сумму с точностью до двух знаков
                converted_amount = round((Decimal(currencies[to_curr]) / Decimal(currencies[from_curr]))
                                         * from_amount, 2)

                # Сохраняем историю конвертации в базе данных
                await sync_to_async(ConversionHistory.objects.create)(
                    from_currency=from_curr,
                    to_currency=to_curr,
                    amount=from_amount,
                    converted_amount=converted_amount
                )

                # Очищаем данные формы после успешной конвертации
                form = CurrencyConverterForm(currencies=currencies)

                # Подготавливаем контекст для передачи в шаблон
                context = {
                    'form': form,
                    'currencies': currencies,
                    'converted_amount': converted_amount,
                    'from_amount': from_amount,
                    'from_curr': from_curr,
                    'to_curr': to_curr
                }
            except (KeyError, InvalidOperation, ZeroDivisionError) as e:
                # Если произошла ошибка при конвертации, добавляем сообщение об ошибке в форму
                await sync_to_async(form.add_error)(None, f"Ошибка при конвертации: {str(e)}")
                context = {
                    'form': form,
                    'currencies': currencies
                }
        else:
            # Если форма невалидна, передаем ее в контекст для отображения ошибок
            context = {
                'form': form,
                'currencies': currencies
            }
    else:
        # Если запрос пришел методом GET, инициализируем пустую форму конвертации
        form = await sync_to_async(CurrencyConverterForm)(currencies=currencies)
        context = {
            'form': form,
            'currencies': currencies,
            'converted_amount': None,  # Обнуляем переменные при GET-запросе
            'from_amount': None,
            'from_curr': None,
            'to_curr': None
        }

    # Возвращаем HTML страницу с результатами конвертации или ошибкой
    return await sync_to_async(render)(request, 'converter/currency_converter.html', context)

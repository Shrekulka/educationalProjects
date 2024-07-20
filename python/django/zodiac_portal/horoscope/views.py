# horoscope/views.py

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse

from horoscope.models import ZodiacSigns

# Создаем экземпляр класса ZodiacSigns для работы с знаками зодиака.
zodiac_signs = ZodiacSigns()


def index(request: HttpRequest):
    zodiacs = zodiac_signs.get_all_signs()
    context = {
        'zodiacs': zodiacs
    }
    return render(request, 'horoscope/index.html', context=context)


def get_info_about_sign_zodiac(request: HttpRequest, sign_zodiac: str):
    # Получаем объект знака зодиака по его имени
    description = zodiac_signs.get_sign(sign_zodiac)
    if description:
        data = {
            'description_zodiac': description,
            # 'sign': sign_zodiac,
        }
        # Если знак найден, возвращаем HttpResponse с информацией о знаке
        return render(request, 'horoscope/info_zodiac.html', context=data)
    else:
        # Если знак не найден, возвращаем HttpResponseNotFound с сообщением об ошибке
        return HttpResponseNotFound(f"Неизвестный знак зодиака - {sign_zodiac}")



def get_info_about_sign_zodiac_by_number(request: HttpRequest,
                                         sign_zodiac: int) -> HttpResponseRedirect | HttpResponseNotFound:
    """
        Перенаправляет на страницу с информацией о знаке зодиака по его порядковому номеру.

        Args:
            request: HttpRequest объект.
            sign_zodiac (int): Порядковый номер знака зодиака.

        Returns:
            HttpResponseRedirect or HttpResponseNotFound: Перенаправление на страницу с информацией о знаке зодиака или
            сообщение о неправильном номере.
    """
    # Получаем объект знака зодиака по его порядковому номеру
    sign = zodiac_signs.get_sign_by_number(sign_zodiac)

    # Проверяем, был ли найден знак зодиака
    if sign:
        # Если знак найден, создаем URL для перенаправления на страницу с информацией о знаке
        redirect_url = reverse("horoscope-name", args=[sign.name])
        # Возвращаем HttpResponseRedirect для перенаправления пользователя на новый URL
        return HttpResponseRedirect(redirect_url)
    else:
        # Если знак не найден, возвращаем HttpResponseNotFound с сообщением об ошибке
        return HttpResponseNotFound(f"Неправильный порядковый номер знака зодиака - {sign_zodiac}")


def get_info_by_date(request: HttpRequest, month: int, day: int) -> HttpResponseRedirect | HttpResponseNotFound:
    """
        Перенаправляет на страницу с информацией о знаке зодиака по указанной дате.

        Args:
            request: HttpRequest объект.
            month (int): Месяц.
            day (int): День.

        Returns:
            HttpResponseRedirect or HttpResponseNotFound: Перенаправление на страницу с информацией о знаке зодиака или
            сообщение об ошибке.
    """
    # Получаем знак зодиака для указанной даты
    sign = zodiac_signs.get_sign_by_date(month, day)

    # Проверяем, был ли найден знак зодиака для указанной даты
    if sign:
        # Создаем URL для перенаправления на страницу с информацией о знаке
        redirect_url = reverse("horoscope-name", args=[sign.name])
        # Возвращаем HttpResponseRedirect для перенаправления пользователя на новый URL
        return HttpResponseRedirect(redirect_url)
    else:
        # Если знак зодиака не найден для указанной даты, возвращаем HttpResponseNotFound с сообщением об ошибке
        return HttpResponseNotFound(f"Не удалось определить знак зодиака для даты {day}.{month}")


def get_zodiac_types(request: HttpRequest) -> HttpResponse:
    """
        Возвращает список типов знаков зодиака в виде HTML списка ссылок.

        Args:
            request: HttpRequest объект.

        Returns:
            HttpResponse: Ответ с HTML содержимым страницы со списком типов знаков зодиака.
    """
    # Получаем все типы знаков зодиака
    types = zodiac_signs.get_all_types()
    li_elements = ''
    # Формируем HTML список ссылок для каждого типа знаков зодиака
    for type_name in types:
        redirect_path = reverse("horoscope-element", args=[type_name])
        li_elements += f"<li><a href='{redirect_path}'>{type_name.title()}</a></li>"
    # Формируем HTML ответ с списком типов знаков зодиака
    response = f"<ul>{li_elements}</ul>"
    return HttpResponse(response)


def get_signs_by_element(request: HttpRequest, element: str) -> HttpResponse | HttpResponseNotFound:
    """
        Возвращает список знаков зодиака, относящихся к указанному элементу, в виде HTML списка ссылок.

        Args:
            request: HttpRequest объект.
            element (str): Элемент зодиака ('fire', 'earth', 'air', 'water').

        Returns:
            HttpResponse or HttpResponseNotFound: Ответ с HTML содержимым страницы со списком знаков зодиака или
            сообщение о неизвестном элементе.
    """
    # Получаем список знаков зодиака для указанного элемента
    signs = zodiac_signs.get_signs_by_element(element)

    # Проверяем, были ли найдены знаки зодиака для указанного элемента
    if signs:
        li_elements = ''
        # Формируем HTML список ссылок для каждого знака зодиака
        for sign in signs:
            redirect_path = reverse("horoscope-name", args=[sign.name])
            li_elements += f"<li><a href='{redirect_path}'>{sign.name.title()}</a></li>"
        # Формируем HTML ответ с заголовком элемента и списком знаков зодиака
        response = f"<h2>{element.title()} signs:</h2><ul>{li_elements}</ul>"
        return HttpResponse(response)
    else:
        # Если указанный элемент неизвестен, возвращаем HttpResponseNotFound с сообщением об ошибке
        return HttpResponseNotFound(f"Неизвестный элемент - {element}")

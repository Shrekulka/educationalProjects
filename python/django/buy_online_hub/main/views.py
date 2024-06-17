from urllib.request import Request

from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request: Request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели Home',
    }
    return render(request, 'main/index.html', context)


def about(request: Request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том, почему магазин такой классный, и какой хороший товар',
    }
    return render(request, 'main/about.html', context)


def delivery_and_payment(request: Request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том, почему магазин такой классный, и какой хороший товар',
    }
    return render(request, 'main/delivery_and_payment.html', context)


def contacts(request: Request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том, почему магазин такой классный, и какой хороший товар',
    }
    return render(request, 'main/contacts.html', context)

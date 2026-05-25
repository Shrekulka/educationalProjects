# sitewomen/modules/women/views.py
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return HttpResponse(f"Содержание {request}")

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        print(f"GET = {request.GET}")
    elif request.POST:
        print(f"POST = {request.POST}")
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

def archive(request, year):
    if year == 2024:
        return redirect ('/')
    elif year == 2025:
        return redirect ('/', permanent=True)
    elif year == 2026:
        return redirect (index)
    elif year == 2027:
        return redirect ('home')
    elif year == 2028:
        return redirect ('cats_slug', 'dance')
    elif year == 2029:
        uri = reverse('cats_slug', args=('music',))
        return redirect (uri)
    elif year == 2030:
        uri = reverse('cats_slug', args=('sing',))
        return HttpResponseRedirect(uri)
    elif year == 2031:
        uri = reverse('cats_slug', args=('sport',))
        return HttpResponsePermanentRedirect(uri)
    elif year > 2024:
        raise Http404

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
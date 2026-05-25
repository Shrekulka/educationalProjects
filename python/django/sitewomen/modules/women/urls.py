# sitewomen/modules/women/urls.py

# sitewomen/modules/women/urls.py

from django.urls import path, include, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "yyyy")
urlpatterns = [
    path('', views.index, name='home'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats_slug'),
    path('archive/<yyyy:year>/', views.archive, name='archive'),
]
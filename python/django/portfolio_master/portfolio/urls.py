from django.urls import path

from portfolio.views import index, about, work_detail, contact

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('work/<slug:slug>/', work_detail, name='work_detail'),
    path('contact/', contact, name='contact'),
]

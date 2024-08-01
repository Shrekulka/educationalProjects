from django.contrib import admin

from shop.models import Book


@admin.register(Book)
class BookAdminPage(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')

    # Поля, по которым можно фильтровать комментарии в админ-панели.
    list_filter = ('id', 'name', 'price')

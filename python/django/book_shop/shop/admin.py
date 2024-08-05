from django.contrib import admin

from shop.models import Book


@admin.register(Book)
class BookAdminPage(admin.ModelAdmin):
    list_display = ('id', 'title', 'autor_name', 'price')

    # Указываем поля, которые будут кликабельными ссылками, ведущими к странице редактирования категории:
    list_display_links = ('id', 'title', 'autor_name', 'price')

    # Поля, по которым можно фильтровать комментарии в админ-панели.
    list_filter = ('id', 'title', 'autor_name', 'price')

    # Настраиваем автоматическое заполнение поля 'slug' на основе значения поля 'title'
    prepopulated_fields = {'slug': ('title',)}

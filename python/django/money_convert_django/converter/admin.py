# money_convert_django/converter/admin.py

from django.contrib import admin

from converter.models import ConversionHistory


# Регистрация модели ConversionHistory в админке
@admin.register(ConversionHistory)
class ConversionHistoryAdmin(admin.ModelAdmin):
    """
        Настройки отображения модели ConversionHistory в административной панели Django.

        Атрибуты:
        ----------
        list_display : tuple
            Список полей модели, которые будут отображаться в виде колонок в списке записей модели.
        list_filter : tuple
            Список полей модели, по которым можно будет фильтровать записи в административной панели.
        search_fields : tuple
            Список полей модели, по которым можно будет осуществлять поиск записей в административной панели.
        date_hierarchy : str
            Поле модели, по которому будет создана иерархия дат для фильтрации записей в административной панели.
    """

    # Поля, которые будут отображаться в списке записей в админке
    list_display = ('from_currency', 'to_currency', 'amount', 'converted_amount', 'conversion_date')

    # Фильтры, которые будут доступны в правой части экрана в админке
    list_filter = ('from_currency', 'to_currency', 'conversion_date')

    # Поля, по которым можно будет осуществлять поиск в админке
    search_fields = ('from_currency', 'to_currency')

    # Иерархия дат, позволяющая легко фильтровать записи по дате
    date_hierarchy = 'conversion_date'

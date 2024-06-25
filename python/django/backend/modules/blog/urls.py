# backend/modules/blog/urls.py

from django.urls import path
from django.urls import reverse
from .views import ArticleListView, ArticleDetailView, ArticleByCategoryListView, articles_list, ArticleCreateView, \
    ArticleUpdateView, ArticleDeleteView, CommentCreateView, ArticleByTagListView, ArticleSearchResultView

# Указываем список URL-шаблонов, которые могут обрабатываться веб-приложением.
urlpatterns = [
    # Определяем маршрут URL по умолчанию ('')
    # Когда пользователь заходит на корневой URL сайта (например, http://example.com/),
    # вызывается ArticleListView для отображения списка статей.
    # as_view() преобразует класс ArticleListView в представление на основе функций.
    # Имя маршрута 'home' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('', ArticleListView.as_view(), name='home'),

    # Определяем маршрут URL 'articles/', который вызывает функцию articles_list для отображения списка статей с
    # пагинацией.
    # Имя маршрута 'articles_by_page' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('articles/', articles_list, name='articles_by_page'),

    # Определяем маршрут URL 'articles/create/', который вызывает ArticleCreateView для отображения формы
    # создания новой статьи.
    # Имя маршрута 'articles_create' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('articles/create/', ArticleCreateView.as_view(), name='articles_create'),

    # Создаем URL-шаблон для обновления существующей статьи.
    # Когда пользователь переходит по этому URL, вызывается ArticleUpdateView для отображения формы обновления статьи.
    # Мы используем <str:slug> в URL для передачи уникального идентификатора статьи (slug).
    # Используемый slug будет передан представлению для получения конкретной статьи для обновления.
    # Имя маршрута 'articles_update' используется для ссылки на этот URL в шаблонах и других частях кода.
    path('articles/<str:slug>/update/', ArticleUpdateView.as_view(), name='articles_update'),

    # Создаем URL-шаблон для удаления существующей статьи.
    # Когда пользователь переходит по этому URL, вызывается ArticleDeleteView для отображения формы удаления статьи.
    # Мы используем <str:slug> в URL для передачи уникального идентификатора статьи (slug).
    # Используемый slug будет передан представлению для получения конкретной статьи для удаления.
    # Имя маршрута 'articles_delete' используется для ссылки на этот URL в шаблонах и других частях кода.
    path('articles/<str:slug>/delete/', ArticleDeleteView.as_view(), name='articles_delete'),

    # Определяем маршрут URL 'articles/<str:slug>/', где <str:slug> - это динамическая часть URL,
    # которая будет передана представлению для получения конкретной статьи.
    # Когда пользователь переходит по этому URL (например, http://example.com/articles/some-slug/),
    # вызывается ArticleDetailView для отображения деталей статьи с указанным slug.
    # Имя маршрута 'articles_detail' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),

    # Определяем маршрут URL 'articles/<int:pk>/comments/create/', который вызывает CommentCreateView для отображения
    # формы создания комментария к статье с определенным идентификатором.
    # Имя маршрута 'comment_create_view' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('articles/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),

    # Определяем маршрут URL 'articles/tags/<str:tag>/', где <str:tag> - это динамическая часть URL,
    # которая будет передана представлению ArticleByTagListView для получения списка статей по указанному тегу.
    # Имя маршрута 'articles_by_tags' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('articles/tags/<str:tag>/', ArticleByTagListView.as_view(), name='articles_by_tags'),

    # Определяем маршрут URL 'category/<str:slug>/', где <str:slug> - это динамическая часть URL,
    # которая будет передана представлению для получения списка статей определенной категории.
    # Когда пользователь переходит по этому URL (например, http://example.com/category/some-category-slug/),
    # вызывается ArticleByCategoryListView для отображения списка статей из указанной категории.
    # Имя маршрута 'articles_by_category' позволяет ссылаться на этот URL в шаблонах и других частях кода.
    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),

    # Определяем маршрут URL 'search/', который вызывает ArticleSearchResultView
    # для отображения результатов поиска статей по заданному запросу.
    # Имя маршрута 'search' используется для ссылки на этот URL в шаблонах и других частях кода.
    path('search/', ArticleSearchResultView.as_view(), name='search'),

]

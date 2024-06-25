# backend/modules/blog/views.py
import random
from typing import Dict, Any, Union, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.db.models import QuerySet, Count
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from taggit.models import Tag

from .forms import ArticleCreateForm, ArticleUpdateForm, CommentCreateForm
from .models import Article, Category, Comment
from ..services.mixins import AuthorRequiredMixin


########################################################################################################################
# Используется для отображения списков объектов (например, статей, комментариев, товаров и т. д.).
class ArticleListView(ListView):
    """
        Представление для отображения списка статей.

        Наследуется от `ListView` и использует шаблон `blog/articles_list.html` для отображения списка статей.
        В качестве контекстной переменной для списка статей используется `'articles'`.

        Attributes:
            model (Article): Модель, с которой работает представление.
            template_name (str): Путь к шаблону для отображения списка статей.
            context_object_name (str): Имя контекстной переменной, в которой будет храниться список статей.
            paginate_by (int): Количество статей на одной странице.
            queryset (QuerySet): Набор объектов, которые будут отображаться в списке.


       Methods:
           get_context_data(**kwargs) -> Dict[str, Any]:
               Добавляет в контекст заголовок страницы и возвращает обновленный контекст.
    """
    model = Article  # Название нашей модели, Article.
    template_name = 'blog/articles/articles_list.html'  # Название нашего шаблона
    context_object_name = 'articles'  # Переменная, в которой будем хранить список для вывода в шаблоне.
    paginate_by = 2  # Указываем количество статей на одной странице для пагинации.
    queryset = Article.objects.all()  # Явно указываем набор объектов для отображения.

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
            Добавляет в контекст заголовок страницы и возвращает обновленный контекст.

            Args:
                **kwargs: Дополнительные аргументы, передаваемые в базовый метод `get_context_data`.

            Returns:
                Dict[str, Any]: Контекстные данные для отображения в шаблоне.
        """
        # Получаем контекст данных, который будет передан в шаблон.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст данные о заголовке страницы.
        context['title'] = 'Главная страница'
        # Возвращаем обновленный контекст.
        return context


########################################################################################################################
# Используется для отображения деталей конкретного объекта (например, отдельной статьи, комментария, товара и т. д.).
class ArticleDetailView(DetailView):
    """
       Представление для отображения деталей конкретной статьи.

       Наследуется от `DetailView` и использует шаблон `blog/articles_detail.html` для отображения деталей статьи.
       В качестве контекстной переменной для объекта статьи используется `'article'`.

       Attributes:
           model (Article): Модель, с которой работает представление.
           template_name (str): Путь к шаблону для отображения деталей статьи.
           context_object_name (str): Имя контекстной переменной, в которой будет храниться объект статьи.
           queryset (QuerySet): Queryset для получения объектов статьи с необходимыми связями.


       Methods:
            get_similar_articles(self, obj: Article) -> List[Article]:
                Возвращает список похожих статей на основе тегов.

           get_context_data(**kwargs) -> Dict[str, Any]:
               Добавляет в контекст заголовок статьи и возвращает обновленный контекст.
    """
    # Указываем модель, с которой будет работать представление - это модель Article.
    model = Article
    # Указываем имя шаблона, который будет использоваться для отображения деталей статьи.
    template_name = 'blog/articles/articles_detail.html'
    # Указываем имя переменной контекста, через которую мы будем обращаться к объекту статьи в шаблоне.
    context_object_name = 'article'
    # Получаем queryset для статей с предварительно загруженными связями
    queryset = model.objects.detail()

    def get_similar_articles(self, obj: Article) -> List[Article]:
        """
            Возвращает список похожих статей на основе тегов.

            Использует теги статьи для поиска похожих статей и возвращает до 6 случайных статей,
            отсортированных по количеству общих тегов.

            Args:
                obj (Article): Текущая статья.

            Returns:
                List[Article]: Список похожих статей.
        """
        # Получаем ID тегов текущей статьи
        article_tags_ids = obj.tags.values_list('id', flat=True)
        # Ищем статьи, которые содержат эти теги, исключая текущую статью
        similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=obj.id)
        # Аннотируем статьи по количеству совпадающих тегов и сортируем по этому количеству
        similar_articles = similar_articles.annotate(related_tags=Count('tags')).order_by('-related_tags')
        # Преобразуем QuerySet в список и перемешиваем его
        similar_articles_list = list(similar_articles.all())
        random.shuffle(similar_articles_list)
        # Возвращаем до 6 случайных статей
        return similar_articles_list[:6]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
            Добавляет в контекст заголовок статьи и форму для создания комментария,
            затем возвращает обновленный контекст.

            Args:
                **kwargs: Дополнительные аргументы, передаваемые в базовый метод `get_context_data`.

            Returns:
                Dict[str, Any]: Контекстные данные для отображения в шаблоне.
        """
        # Получаем контекст данных, который будет передан в шаблон.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст данные о заголовке статьи, используя self.object.title.
        # self.object - это объект статьи, который был получен из базы данных.
        context['title'] = self.object.title

        # Добавляем в контекст форму создания комментариев.
        context['form'] = CommentCreateForm

        # Добавляем в контекст список похожих статей, полученный с помощью метода get_similar_articles.
        context['similar_articles'] = self.get_similar_articles(self.object)

        # Возвращаем обновленный контекст.
        return context


########################################################################################################################
# Представление для сортировки статей по категориям
class ArticleByCategoryListView(ListView):
    """
        Представление для отображения списка статей, относящихся к определенной категории.

        Представление наследуется от `ListView` и использует шаблон `blog/articles_list.html` для
        отображения списка статей. Категория, для которой отображаются статьи, определяется
        по `slug` в URL-адресе.

        Атрибуты:
            model (Article): Модель, с которой работает представление.
            template_name (str): Путь к шаблону для отображения списка статей.
            context_object_name (str): Имя контекстной переменной, в которой будет храниться список статей.
            category (Category | None): Объект текущей категории.

        Методы:
            get_queryset() -> QuerySet[Article]:
                Возвращает queryset со всеми статьями, относящимися к текущей категории.

            get_context_data(**kwargs) -> Dict[str, Any]:
                Возвращает контекстные данные для отображения в шаблоне, включая список статей
                и заголовок страницы с названием текущей категории.
    """

    # Указываем модель, с которой будем работать
    model = Article

    # Указываем шаблон для отображения списка статей
    template_name = 'blog/articles/articles_list.html'

    # Указываем имя контекстной переменной, в которой будет храниться список статей
    context_object_name = 'articles'

    # Создаем переменную для хранения текущей категории
    category: Category | None = None

    def get_queryset(self) -> QuerySet[Article]:
        """
            Возвращает queryset со всеми статьями, относящимися к текущей категории.

            Returns:
                QuerySet[Article]: Queryset со всеми статьями, относящимися к текущей категории.
        """
        # Получаем объект категории по slug из URL-адреса
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        ################################################################################################################
        # Отладочная информация
        print(f"URL: {self.request.path}")  # Выводим URL-адрес запроса
        print(f"Категория: {self.category.title}")  # Выводим название категории
        ################################################################################################################

        # Создаем queryset, содержащий все статьи, относящиеся к текущей категории
        queryset = Article.objects.all().filter(category__slug=self.category.slug)

        ################################################################################################################
        # Отладочная информация
        print(f"Количество статей: {queryset.count()}")  # Выводим количество статей в queryset
        ################################################################################################################

        # Возвращаем queryset
        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
            Возвращает контекстные данные для отображения в шаблоне, включая список статей
            и заголовок страницы с названием текущей категории.

            Args:
                **kwargs: Дополнительные аргументы, передаваемые в базовый метод `get_context_data`.

            Returns:
                Dict[str, Any]: Контекстные данные для отображения в шаблоне.
        """
        # Получаем контекстные данные из базового класса
        context = super().get_context_data(**kwargs)

        # Добавляем в контекст заголовок страницы, содержащий название категории
        context['title'] = f'Статьи из категории: {self.category.title}'

        # Возвращаем обновленный контекст
        return context


########################################################################################################################
class ArticleByTagListView(ListView):
    """
        Класс представления для отображения списка статей по тегу.

        Attributes:
            model (Article): Модель, которая используется для получения данных о статьях.
            template_name (str): Имя шаблона, используемого для рендеринга страницы.
            context_object_name (str): Имя переменной контекста для передачи списка статей в шаблон.
            paginate_by (int): Количество статей на одной странице пагинации.
            tag (Tag or None): Объект тега, используемый для фильтрации статей.

        Methods:
            get_queryset(): Возвращает queryset статей, отфильтрованных по заданному тегу.
            get_context_data(**kwargs): Добавляет дополнительные данные в контекст шаблона,
                                        включая название тега для отображения в заголовке страницы.
    """
    model: Article = Article  # Указываем модель, которая будет использоваться для получения данных (Article)

    template_name: str = 'blog/articles/articles_list.html'  # Задаем имя шаблона для отображения списка статей

    context_object_name: str = 'articles'  # Задаем имя переменной контекста для передачи списка статей в шаблон

    paginate_by: int = 10  # Задаем количество статей на одной странице пагинации

    tag: Tag or None = None  # Инициализируем переменную для хранения объекта тега или None, если тег не задан

    def get_queryset(self) -> QuerySet[Article]:
        """
            Возвращает queryset статей, отфильтрованных по тегу, полученному из URL-параметра.

            Returns:
                QuerySet[Article]: Queryset статей, отфильтрованных по заданному тегу.
        """
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])  # Получаем объект тега по его slug из URL-параметра

        queryset = Article.objects.all().filter(tags__slug=self.tag.slug)  # Фильтруем статьи по тегу

        return queryset  # Возвращаем queryset, содержащий статьи, отфильтрованные по заданному тегу

    def get_context_data(self, **kwargs) -> dict:
        """
            Добавляет дополнительные данные в контекст шаблона.

            Args:
                **kwargs: Дополнительные аргументы для передачи в родительский метод.

            Returns:
                dict: Контекст шаблона с дополнительными данными.
        """
        context = super().get_context_data(**kwargs)  # Получаем базовый контекст от родительского метода

        # Добавляем название тега в контекст для отображения в шаблоне
        context['title'] = f'Статьи по тегу: {self.tag.name}'

        return context  # Возвращаем обновленный контекст шаблона


########################################################################################################################
class ArticleCreateView(CreateView):
    """
    Представление для создания материалов на сайте.

    Атрибуты:
        model (Article): Модель статьи.
        template_name (str): Имя шаблона для отображения формы создания статьи.
        form_class (ArticleCreateForm): Форма для создания статьи.
    """

    model = Article  # Указываем модель, с которой работает представление
    template_name = 'blog/articles/articles_create.html'  # Имя шаблона для отображения формы создания статьи
    form_class = ArticleCreateForm  # Форма для создания статьи

    def get_context_data(self, **kwargs) -> dict:
        """
            Добавляет заголовок страницы в контекст.

            Args:
                **kwargs: Дополнительные аргументы.

            Returns:
                dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)  # Получаем существующий контекст данных
        context['title'] = 'Добавление статьи на сайт'  # Добавляем заголовок страницы в контекст
        return context  # Возвращаем обновленный контекст

    def form_valid(self, form) -> HttpResponse:
        """
            Обрабатывает валидную форму.

            Args:
                form (ArticleCreateForm): Форма для создания статьи.

            Returns:
                HttpResponse: Ответ сервера после успешного создания статьи.
        """
        form.instance.author = self.request.user  # Устанавливаем текущего пользователя как автора статьи
        form.save()  # Сохраняем форму и создаем объект статьи
        return super().form_valid(form)  # Вызываем метод form_valid родительского класса и возвращаем его результат

    def get_success_url(self) -> str:
        """
            Возвращает URL для перенаправления после успешного создания статьи.

            Returns:
                str: URL для перенаправления.
        """
        return reverse_lazy('articles_detail', kwargs={'slug': self.object.slug})  # Возвращаем URL для перенаправления


########################################################################################################################
class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
        Представление для обновления статьи.

        Расширяет базовый класс UpdateView, а также миксины AuthorRequiredMixin и SuccessMessageMixin.
        Обеспечивает функциональность для обновления существующих статей.

        Атрибуты:
            model (Article): Модель статьи, с которой работает представление.
            template_name (str): Имя шаблона для отображения формы обновления статьи.
            context_object_name (str): Имя переменной контекста для передачи объекта статьи в шаблон.
            form_class (ArticleUpdateForm): Форма для обновления статьи.
            login_url (str): URL для перенаправления неавторизованных пользователей.
            success_message (str): Сообщение об успешном обновлении статьи.

        Методы:
            get_context_data(self, object_list=None, **kwargs) -> dict:
                Добавляет заголовок страницы в контекст.
            form_valid(self, form) -> HttpResponse:
                Обрабатывает валидную форму, устанавливает текущего пользователя как обновившего статью и сохраняет форму.
            get_success_url(self) -> str:
                Получает URL-адрес после успешного обновления статьи.
    """
    model = Article  # Указываем модель, с которой работает представление
    template_name = 'blog/articles/articles_update.html'  # Имя шаблона для отображения формы обновления статьи
    context_object_name = 'article'  # Имя переменной контекста для передачи объекта статьи в шаблон
    form_class = ArticleUpdateForm  # Форма для обновления статьи
    login_url = 'home'  # URL для перенаправления неавторизованных пользователей
    success_message = 'Материал был успешно обновлен'  # Сообщение об успешном обновлении статьи

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Добавляет заголовок страницы в контекст.

        Args:
            object_list: Список объектов.
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)  # Получаем существующий контекст данных
        context['title'] = f'Обновление статьи: {self.object.title}'  # Добавляем заголовок страницы в контекст
        return context  # Возвращаем обновленный контекст

    def form_valid(self, form) -> HttpResponse:
        """
        Обрабатывает валидную форму.

        Args:
            form (ArticleUpdateForm): Форма для обновления статьи.

        Returns:
            HttpResponse: Ответ сервера после успешного обновления статьи.
        """
        form.instance.updater = self.request.user  # Устанавливаем текущего пользователя как апдейтера статьи
        form.save()  # Сохраняем форму и обновляем объект статьи
        return super().form_valid(form)  # Вызываем метод form_valid родительского класса и возвращаем


########################################################################################################################
class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
        Представление для удаления статьи.

        Расширяет базовый класс DeleteView, а также миксин AuthorRequiredMixin.
        Обеспечивает функциональность для удаления существующих статей.

        Атрибуты:
            model (Article): Модель статьи, с которой работает представление.
            success_url (str): URL для перенаправления после успешного удаления статьи.
            context_object_name (str): Имя переменной контекста для передачи объекта статьи в шаблон.
            template_name (str): Имя шаблона для отображения формы удаления статьи.

        Методы:
            get_context_data(self, object_list=None, **kwargs) -> dict:
                Добавляет заголовок страницы в контекст.
    """
    model = Article  # Модель статьи
    success_url = reverse_lazy('home')  # URL для перенаправления после успешного удаления статьи
    context_object_name = 'article'  # Имя переменной контекста для передачи объекта статьи в шаблон
    template_name = 'blog/articles/articles_delete.html'  # Имя шаблона для отображения формы удаления статьи

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
            Добавляет заголовок страницы в контекст.

            Args:
                object_list: Список объектов.
                **kwargs: Дополнительные аргументы.

            Returns:
                dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)  # Получаем существующий контекст данных
        context['title'] = f'Удаление статьи: {self.object.title}'  # Добавляем заголовок страницы в контекст
        return context  # Возвращаем обновленный контекст


########################################################################################################################
class ArticleSearchResultView(ListView):
    """
        Представление для отображения результатов поиска статей.

        Расширяет базовый класс ListView и добавляет функциональность поиска по статьям.

        Атрибуты:
            model (Article): Модель статьи, с которой работает представление.
            context_object_name (str): Имя переменной контекста для передачи списка статей в шаблон.
            paginate_by (int): Количество статей на одной странице.
            allow_empty (bool): Разрешить пустые результаты поиска.
            template_name (str): Имя шаблона для отображения результатов поиска.

        Методы:
            get_queryset(self) -> QuerySet:
                Возвращает набор данных (QuerySet) для отображения в представлении.
            get_context_data(self, **kwargs) -> dict:
                Добавляет заголовок страницы в контекст.
    """
    model = Article  # Указываем модель, с которой работает представление
    context_object_name = 'articles'  # Имя переменной контекста для передачи списка статей в шаблон
    paginate_by = 10  # Количество статей на одной странице
    allow_empty = True  # Разрешаем пустые результаты поиска
    template_name = 'blog/articles/articles_list.html'  # Имя шаблона для отображения результатов поиска

    def get_queryset(self) -> QuerySet:
        """
            Возвращает набор данных (QuerySet) для отображения в представлении.

            Использует полнотекстовый поиск по полям 'full_description' и 'title'.

            Returns:
                QuerySet: Набор данных, отфильтрованный по критериям поиска.
        """
        query = self.request.GET.get('do')  # Получаем поисковый запрос из GET-параметров
        # Определяем поисковые векторы для полнотекстового поиска
        search_vector = SearchVector('full_description', weight='B') + SearchVector('title', weight='A')
        search_query = SearchQuery(query)  # Создаем объект поискового запроса
        # Возвращаем набор данных, аннотированный ранком поиска, фильтруем по ранку и сортируем по убыванию ранка
        return (
            self.model.objects.annotate(rank=SearchRank(search_vector, search_query))
            .filter(rank__gte=0.3)
            .order_by('-rank')
        )

    def get_context_data(self, **kwargs: Any) -> dict:
        """
            Добавляет заголовок страницы в контекст.

            Args:
                **kwargs: Дополнительные аргументы.

            Returns:
                dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)  # Получаем существующий контекст данных
        context['title'] = f'Результаты поиска: {self.request.GET.get("do")}'  # Добавляем заголовок страницы в контекст
        return context  # Возвращаем обновленный контекст


########################################################################################################################
def articles_list(request: HttpRequest) -> HttpResponse:
    """
        Представление для отображения списка статей с возможностью пагинации.

        Эта функция-представление получает запрос от пользователя и обрабатывает его,
        извлекая все статьи из базы данных. Затем статьи разбиваются на страницы с помощью
        класса Paginator. Полученный объект страницы (page_object) передается в контекст для
        отображения в шаблоне.

        Args:
            request (HttpRequest): Объект HTTP-запроса от пользователя.

        Returns:
            HttpResponse: Отображаемая HTML-страница со списком статей для указанной страницы.
    """
    # Получаем все статьи из базы данных
    articles = Article.objects.all()

    # Создаем объект Paginator с количеством статей на странице, равным 2
    paginator = Paginator(articles, per_page=2)

    # Получаем номер страницы из GET-параметра 'page' или используем значение по умолчанию
    page_number = request.GET.get('page')

    # Получаем объект страницы для указанного номера страницы
    page_object = paginator.get_page(page_number)

    # Создаем контекст, который будет передан в шаблон
    context = {'page_obj': page_object}

    # Рендерим шаблон с контекстом и возвращаем HTTP-ответ
    return render(request, 'blog/articles/articles_func_list.html', context)


########################################################################################################################
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
        Представление для создания комментариев.

        Атрибуты:
            model (Comment): Модель комментария.
            form_class (CommentCreateForm): Форма для создания комментария.

        Методы:
            is_ajax(): Проверяет, является ли запрос AJAX-запросом.
            form_invalid(form: CommentCreateForm): Обрабатывает невалидную форму.
            form_valid(form: CommentCreateForm): Обрабатывает валидную форму.
            handle_no_permission(): Обрабатывает случай, когда у пользователя отсутствуют необходимые разрешения.
            get_context_data(**kwargs): Добавляет форму в контекст данных.
    """
    model = Comment  # Модель комментария
    form_class = CommentCreateForm  # Форма для создания комментария

    def is_ajax(self) -> bool:
        """
            Проверяет, является ли запрос AJAX-запросом.

            Возвращает:
                bool: True, если запрос является AJAX-запросом, иначе False.
        """
        # Проверяем наличие заголовка 'X-Requested-With' в запросе.
        # Если этот заголовок присутствует и его значение равно 'XMLHttpRequest', то запрос считается AJAX-запросом.
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form: CommentCreateForm) -> Union[JsonResponse, HttpResponse]:
        """
            Обрабатывает невалидную форму.

            Args:
                form (CommentCreateForm): Невалидная форма.

            Returns:
                Union[JsonResponse, HttpResponse]: JSON-ответ с ошибками валидации, если запрос AJAX,
                иначе редирект на страницу с формой.
        """
        # Проверяем, является ли запрос AJAX-запросом.
        if self.is_ajax():
            # Возвращаем JSON-ответ с ошибками валидации формы.
            return JsonResponse({'error': form.errors}, status=400)
        # Если запрос не AJAX, вызываем обработчик невалидной формы из родительского класса.
        return super().form_invalid(form)

    def form_valid(self, form: CommentCreateForm) -> Union[JsonResponse, HttpResponseRedirect]:
        """
            Обрабатывает валидную форму.

            Аргументы:
                form (CommentCreateForm): Валидная форма.

            Возвращает:
                Union[JsonResponse, HttpResponseRedirect]: JSON-ответ с информацией о созданном комментарии,
                если запрос AJAX, иначе редирект на страницу со статьей.
        """
        comment = form.save(commit=False)  # Сохраняем комментарий без записи в БД
        comment.article_id = self.kwargs.get('pk')  # Устанавливаем ID статьи
        comment.author = self.request.user  # Устанавливаем автора комментария
        comment.parent_id = form.cleaned_data.get('parent')  # Устанавливаем родительский комментарий, если указан
        comment.save()  # Сохраняем комментарий

        if self.is_ajax():  # Если запрос AJAX
            return JsonResponse({
                'is_child': comment.is_child_node(),  # Проверяем, является ли комментарий дочерним
                'id': comment.id,  # ID комментария
                'author': comment.author.username,  # Имя автора комментария
                'parent_id': comment.parent_id,  # ID родительского комментария
                'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),  # Время создания комментария
                'avatar': comment.author.profile.avatar.url,  # URL аватара автора комментария
                'content': comment.content,  # Содержание комментария
                'get_absolute_url': comment.author.profile.get_absolute_url()  # Абсолютный URL профиля автора
            }, status=200)

        return redirect(comment.article.get_absolute_url())  # Перенаправление на страницу, содержащую данную статью

    def handle_no_permission(self) -> JsonResponse:
        """
            Обрабатывает случай, когда у пользователя отсутствуют необходимые разрешения.

            Возвращает:
                JsonResponse: JSON-ответ с сообщением об ошибке.
        """
        # Возвращает JSON-ответ с сообщением об ошибке, указывая, что для добавления комментариев необходимо
        # авторизоваться.
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)

    def get_context_data(self, **kwargs) -> dict:
        """
            Добавляет форму в контекст данных.

            Аргументы:
                **kwargs: Дополнительные аргументы контекста.

            Возвращает:
                dict: Контекст данных с добавленной формой.
        """
        context = super().get_context_data(**kwargs)  # Получаем базовый контекст данных из родительского класса
        context['form'] = CommentCreateForm  # Добавляем форму в контекст данных
        return context  # Возвращаем обновленный контекст данных
########################################################################################################################

# find_all_links_on_web_pages/solution_using_dictionary.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, unquote
from collections import defaultdict

url = 'https://ru.wikipedia.org/wiki/Python'
response = requests.get(url)  # Отправляем GET-запрос на указанный URL

if response.status_code == 200:  # Если запрос успешен (статус код 200)
    soup = BeautifulSoup(response.content, 'html.parser')  # Создаем объект BeautifulSoup для анализа HTML-кода

    links_dict = defaultdict(set)  # Создаем словарь с значениями в виде множества для хранения ссылок
    # defaultdict(set) - Здесь мы создаем словарь, где значениями для каждого ключа будет множество. Когда мы обращаемся
    # к несуществующему ключу в этом словаре, он автоматически создаст новую запись с пустым множеством (set) в качестве
    # значения по умолчанию.

    # Это очень удобно, когда нам нужно создать словарь, где значения будут коллекциями, такими как список, множество
    # или другой словарь, и при этом автоматически обрабатывать несуществующие ключи. В данном случае, используя
    # defaultdict(set), мы создаем словарь links_dict, где каждое значение для ключа будет множество для хранения
    # уникальных ссылок. Таким образом, мы можем легко добавлять ссылки в словарь, и дубликаты автоматически будут
    # исключены.

    for link in soup.find_all('a'):  # Проходимся по всем тегам <a> (ссылкам) на странице
        href = link.get('href')  # Получаем значение атрибута 'href' из каждого тега <a>
        if href:
            if href.startswith('#'):  # Если ссылка начинается с якорного символа "#"
                continue  # Пропускаем эту ссылку, так как это якорные ссылки на текущую страницу

            parsed_url = urlparse(href)  # Анализируем атрибут 'href' с помощью метода urlparse
            # строка parsed_url = urlparse(href) используется для разбора (парсинга) значения атрибута href из тега <a>
            # в HTML-коде. Это позволяет получить структурированную информацию об URL (Uniform Resource Locator) и
            # использовать эту информацию для анализа ссылок.

            # urlparse() - это функция из модуля urllib.parse в Python, которая разбирает (парсит) переданный ей URL и
            # возвращает объект типа ParseResult, содержащий различные компоненты URL, такие как протокол, домен, путь,
            # параметры, запросы и т.д.

            # Например, если href содержит значение "https://ru.wikipedia.org/wiki/Python", то после применения
            # urlparse(href), parsed_url будет содержать следующую информацию:

            # parsed_url.scheme    # Возвращает протокол (например, "https")
            # parsed_url.netloc    # Возвращает домен и порт (например, "ru.wikipedia.org")
            # parsed_url.path      # Возвращает путь на сервере (например, "/wiki/Python")
            # parsed_url.params    # Возвращает параметры (если есть)
            # parsed_url.query     # Возвращает строку запроса (если есть)
            # parsed_url.fragment  # Возвращает фрагмент (якорь) после "#", если есть

            # Если netloc присутствует, это означает, что ссылка имеет домен (например, "ru.wikipedia.org"), и такая
            # ссылка считается внешней.
            if parsed_url.netloc:
                links_dict['external'].add(href)
            # Иначе считаем ее внутренней ссылкой
            else:
                # Внутренние ссылки сохраняем в множество с ключом 'internal'
                links_dict['internal'].add(urljoin(url, href))

    print("Внутренние ссылки:")  # Выводим все внутренние ссылки
    for idx, internal_link in enumerate(links_dict['internal'], start=1):
        print(f"{idx}. {unquote(internal_link)}")  # Декодируем ссылку перед выводом
        # Функция unquote принимает закодированную строку и декодирует ее обратно в исходный вид, восстанавливая
        # специальные символы и приводя ее в более читаемый и понятный формат.

    print("\nВнешние ссылки:")  # Выводим все внешние ссылки
    for idx, external_link in enumerate(links_dict['external'], start=1):
        print(f"{idx}. {unquote(external_link)}")  # Декодируем ссылку перед выводом

else:  # Если запрос не успешен (статус код не равен 200)
    print("Ошибка при получении страницы. Статус код:", response.status_code)  # Выводим сообщение об ошибке

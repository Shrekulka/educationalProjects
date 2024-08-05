# find_all_links_on_web_pages/solution_using_set.py

from urllib.parse import urlparse, urljoin, unquote

import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/Python'
response = requests.get(url)  # Отправляем GET-запрос на указанный URL

if response.status_code == 200:  # Если запрос успешен (статус код 200)
    soup = BeautifulSoup(response.content, 'html.parser')  # Создаем объект BeautifulSoup для анализа HTML-кода

    internal_links = set()  # Создаем пустое множество для хранения уникальных внутренних ссылок
    external_links = set()  # Создаем пустое множество для хранения уникальных внешних ссылок

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
                external_links.add(href)  # Добавляем ее во множество внешних ссылок
            # Иначе считаем ее внутренней ссылкой
            else:
                # Добавляем ее во множество внутренних ссылок, объединяя с базовым URL
                internal_links.add(urljoin(url, href))
    print("Внутренние ссылки:")

    for internal_link in internal_links:  # Выводим все внутренние ссылки
        print(unquote(internal_link))
        # Функция unquote принимает закодированную строку и декодирует ее обратно в исходный вид, восстанавливая
        # специальные символы и приводя ее в более читаемый и понятный формат.

    print("\n\nВнешние ссылки:")
    for external_link in external_links:  # Выводим все внешние ссылки
        print(unquote(external_link))

else:  # Если запрос не успешен (статус код не равен 200)
    print("Ошибка при получении страницы. Статус код:", response.status_code)  # Выводим сообщение об ошибке

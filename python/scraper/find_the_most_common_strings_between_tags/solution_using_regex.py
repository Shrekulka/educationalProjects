import requests
import re
from collections import Counter

# URL веб-страницы, содержащей блоки кода
url = "https://stepik.org/media/attachments/lesson/209719/2.html"

# Получаем текст HTML-контента с помощью requests.get() с использованием контекстного менеджера "with"
with requests.get(url) as response:
    html = response.text

# Используем регулярное выражение для поиска всех фрагментов кода между тегами <code> и </code>
code_blocks = re.findall(r'<code>(.*?)</code>', html)

# Используем Counter для подсчета вхождений каждого кода
code_counter = Counter(code_blocks)

# Находим максимальное количество вхождений кода
max_occurrences = max(code_counter.values())

# Используем генератор списка для выбора кодов, у которых количество вхождений равно максимальному
most_common_codes = [code for code, count in code_counter.items() if count == max_occurrences]

# Выводим коды в алфавитном порядке через пробел
print(" ".join(sorted(most_common_codes)))

# Будет такой ответ - else except finally
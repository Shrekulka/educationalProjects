import requests
from bs4 import BeautifulSoup

url = 'https://stepik.org/media/attachments/lesson/209723/3.html'
response = requests.get(url)  # Отправляем GET-запрос на указанный URL

if response.status_code == 200:  # Если запрос успешен (статус код 200)
    soup = BeautifulSoup(response.content, 'html.parser')  # Создаем объект BeautifulSoup для анализа HTML-кода

    numbers_in_table = []  # список для цифр

    # Находим все ячейки таблицы (теги <td>) в HTML и извлекаем текст из каждой ячейки
    for td in soup.find_all('td'):
        # Преобразуем текст в ячейке в число и добавляем его в список numbers_in_table
        try:
            number = int(td.text.strip())
            numbers_in_table.append(number)
        except ValueError:
            pass

    # Вычисляем сумму всех чисел в таблице
    total_sum = sum(numbers_in_table)
    print(total_sum)

else:  # Если запрос не успешен (статус код не равен 200)
    print("Ошибка при получении страницы. Статус код:", response.status_code)

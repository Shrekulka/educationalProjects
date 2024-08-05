import requests
from bs4 import BeautifulSoup

url = 'https://stepik.org/media/attachments/lesson/209723/3.html'

try:
    # Отправляем GET-запрос на указанный URL и получаем ответ
    with requests.get(url) as response:
        response.raise_for_status()  # Проверяем, успешно ли выполнился запрос (статус код 200)
        soup = BeautifulSoup(response.content, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML-кода

        total_sum = 0  # Переменная для хранения общей суммы чисел

        # Проходим по всем ячейкам <td> в таблице
        for td in soup.find_all('td'):
            # Проверяем, является ли текст в ячейке числом, и если да, то добавляем его к общей сумме
            if td.text.strip().isdigit():
                total_sum += int(td.text.strip())

        # Выводим общую сумму чисел на экран
        print(total_sum)

except requests.exceptions.RequestException as e:
    # Выводим сообщение об ошибке, если произошла ошибка при выполнении запроса
    print("Ошибка при получении страницы:", e)
except ValueError as e:
    # Выводим сообщение об ошибке, если произошла ошибка при обработке чисел
    print("Ошибка при обработке чисел:", e)
except AttributeError as e:
    # Выводим сообщение об ошибке, если таблица не была найдена на странице
    print("Таблица не найдена на странице:", e)

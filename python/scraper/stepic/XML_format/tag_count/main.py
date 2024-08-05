import xmltodict
import requests

# Загрузка XML-файла
url = "https://stepik.org/media/attachments/lesson/245678/map1.osm"
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    xml = response.text
    dct = xmltodict.parse(xml)

    # Инициализация счетчиков для узлов с вложенными тегами и для узлов без тегов
    nested_tag_count = 0
    tag_not_nested_count = 0

    # Перебор каждого элемента 'node' в структуре данных dct
    for node in dct['osm']['node']:
        # Проверка наличия ключа 'tag' в текущем элементе 'node'
        if 'tag' in node:
            nested_tag_count += 1
        else:
            tag_not_nested_count += 1

    # Вывод результата подсчета вложенных и не вложенных тегов для узлов
    print(f"Number of nodes with tag tag: {nested_tag_count}, number of nodes without tag tag: {tag_not_nested_count}")
else:
    print("Failed to retrieve XML data.")  # В случае неудачного запроса выводим сообщение об ошибке

import xmltodict
import requests
from collections import defaultdict

# Загрузка XML-файла
url = "https://stepik.org/media/attachments/lesson/245678/map1.osm"
response = requests.get(url)  # Выполнение GET-запроса к указанному URL

# Проверка успешности запроса
if response.status_code == 200:  # Если код состояния ответа равен 200 (успешный запрос)
    xml = response.text  # Получение текстового содержимого ответа
    dct = xmltodict.parse(xml)  # Преобразование XML в структуру данных Python

    # Инициализация словаря для подсчета магазинов по типам
    shop_info_types = defaultdict(int)
    # Инициализация словаря для хранения информации о магазинах (тип, имя)
    shop_info_names = defaultdict(list)

    # Инициализация счетчика общего количества магазинов
    total_shop_count = 0

    # Перебор каждого элемента 'node' в структуре данных
    for node in dct['osm']['node']:
        if 'tag' in node:  # Проверка наличия вложенных тегов 'tag'
            tags = node['tag']

            # Проверка, является ли 'tags' строкой, иначе делаем его списком
            if not isinstance(tags, list):
                tags = [tags]

            # Поиск тега '@k' равного 'shop'
            shop_tag = next((tag for tag in tags if isinstance(tag, dict) and tag.get('@k') == 'shop'), None)

            # Если найден тег 'shop', извлекаем информацию о магазине
            if shop_tag:
                shop_type = shop_tag.get('@v')

                # Извлечение имени магазина из других тегов, если доступно
                name_tag = next((tag for tag in tags if isinstance(tag, dict) and tag.get('@k') == 'name'), None)
                name = name_tag.get('@v') if name_tag else 'N/A'

                # Добавление информации о магазине
                shop_info_types[shop_type] += 1
                shop_info_names[shop_type].append(name)

                # Увеличим счетчик общего количества магазинов
                total_shop_count += 1

    # Вывод общего количества магазинов
    print(f"Total number of shops: {total_shop_count}\n")

    # Вывод информации о магазинах по типам и их количеству
    print("Shop Types and Counts:")
    for shop_type, count in shop_info_types.items():
        names = ', '.join(shop_info_names[shop_type])
        print(f"Shop Type: {shop_type}\tCount: {count}\tNames: {names}")

else:
    print("Failed to retrieve XML data.")  # Вывод сообщения об ошибке, если запрос не удался

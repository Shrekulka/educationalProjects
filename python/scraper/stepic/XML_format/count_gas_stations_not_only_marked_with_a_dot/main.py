# Импорт необходимых библиотек
import requests
import xmltodict

# Определение URL-адреса фрагмента карты OSM
url = 'https://stepik.org/media/attachments/lesson/245681/map2.osm'

# Выполнение HTTP-запроса GET для получения XML-данных OSM
response = requests.get(url)

# Проверка успешности запроса (статус код 200)
if response.status_code == 200:
    # Извлечение XML-данных из ответа
    xml = response.text

    # Разбор XML-данных в словарь с использованием xmltodict
    dct = xmltodict.parse(xml)

    # Инициализация счетчика для подсчета АЗС
    petrol_count = 0

    # Перебор всех узлов (nodes) и линий (ways) в словаре OSM
    for node_or_way in (dct['osm']['node'] + dct['osm']['way']):
        # Проверка наличия ключа 'tag' у узла или линии (теги, связанные с объектом)
        if 'tag' in node_or_way:
            tags = node_or_way['tag']

            # Обработка случаев, когда 'tags' является списком (несколько тегов)
            if isinstance(tags, list):
                # Перебор каждого тега в списке
                for tag in tags:
                    # Проверка, представляет ли тег АЗС
                    if '@k' in tag and tag['@k'] == 'amenity' and tag['@v'] == 'fuel':
                        # Увеличение счетчика АЗС
                        petrol_count += 1
            # Обработка случаев, когда 'tags' является словарем (один тег)
            elif isinstance(tags, dict):
                # Проверка, представляет ли тег АЗС
                if '@k' in tags and tags['@k'] == 'amenity' and '@v' in tags and tags['@v'] == 'fuel':
                    # Увеличение счетчика АЗС
                    petrol_count += 1

    # Вывод количества найденных АЗС
    print("Number of gas stations:", petrol_count)
else:
    # Вывод сообщения, если получение XML-данных не удалось
    print("Failed to retrieve XML data.")

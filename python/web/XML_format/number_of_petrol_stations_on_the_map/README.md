**Task:**
Vasya decided to open a gas station (fuel station). In order to assess the level of competition, he wants to study the 
number of gas stations in the area of his interest. Vasya downloaded the map fragment he's interested in from OSM 
(OpenStreetMap) at this link: https://stepik.org/media/attachments/lesson/245681/map2.osm. He wants to count how many 
point objects (nodes) on the map are marked as gas stations. Your task is to output a single number - the count of gas 
stations.
"How is a gas station marked in OpenStreetMap" - an example of a good query to find out how gas stations are marked in 
OpenStreetMap.

**Solution:**
To solve the task of counting the number of gas stations on the desired segment of the OSM (OpenStreetMap) map, the 
`xmltodict` library is used to parse XML data, and the `requests` library is used to perform an HTTP request and 
retrieve XML data. The URL of the OSM map is specified first, followed by a GET request to that URL. If the request is 
successful (status code 200), XML data is extracted from the response. The XML data is then parsed into a dictionary 
using `xmltodict.parse`.

Then, a loop iterates through all nodes in the dictionary obtained from the XML. For each node, it checks if tags exist.
If tags exist, it checks whether the node represents a gas station. If the node has an attribute `@k` with the value 
`'amenity'` and an attribute `@v` with the value `'fuel'`, it is considered a gas station, and the counter is 
incremented.
Note that the code also handles different tag data structures (array or dictionary) since depending on the number of 
tags, they can be represented as an array or individual dictionaries.

As a result, the code outputs the count of gas stations found on the desired segment of the OSM map.




**Задача:**
Вася решил открыть АЗС (заправку). Чтобы оценить уровень конкуренции, он хочет изучить количество заправок в интересующем
его районе. Вася скачал интересующий его кусок карты OSM https://stepik.org/media/attachments/lesson/245681/map2.osm и 
хочет посчитать, сколько на нём отмечено точечных объектов (node), являющихся заправкой. В качестве ответа вам необходимо
вывести одно число - количество АЗС.

"Как обозначается заправка в OpenStreetMap" - пример хорошего запроса, чтобы узнать, как обозначается заправка в 
OpenStreetMap.

**Решение:**
Для решения задачи по подсчету количества АЗС на интересующем участке карты OSM (OpenStreetMap) используется библиотека 
`xmltodict` для разбора XML-данных и библиотека `requests` для выполнения HTTP-запроса и получения XML-данных.
Сначала указывается URL-адрес карты OSM, затем выполняется GET-запрос к этому URL. Если запрос успешен (статус код 200),
XML-данные извлекаются из ответа. XML-данные затем разбираются в словарь с помощью `xmltodict.parse`.
Затем идет цикл по всем узлам (nodes) в словаре, полученном из XML. Для каждого узла проверяется наличие тегов (`tag`). 
Если теги существуют, то идет проверка на то, является ли узел заправкой. Если узел имеет атрибут `@k` со значением 
`'amenity'` и атрибут `@v` со значением `'fuel'`, то он считается заправкой, и счетчик увеличивается.
Обратите внимание, что код также учитывает различные структуры данных для тегов (массив или словарь), так как в 
зависимости от количества тегов они могут представляться как массив или как отдельные словари.

В результате выводится количество найденных АЗС на интересующем участке карты OSM.
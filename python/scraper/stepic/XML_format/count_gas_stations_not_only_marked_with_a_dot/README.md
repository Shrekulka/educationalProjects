**Task:**
Vasya, who opened a gas station in the previous lesson, went bankrupt. The competition turned out to be too fierce. 
Vasya suspects that this happened because gas station tags might not only be associated with points, but also with 
certain contours. Determine how many gas stations actually exist (not just those marked as points) on the map fragment 
at https://stepik.org/media/attachments/lesson/245681/map2.osm.

**Solution:**
1. Import the necessary libraries: `xmltodict` for parsing XML data and `requests` for making HTTP requests.
2. Define the URL address of the OSM map fragment.
3. Perform a GET request to the URL and retrieve XML data.
4. If the request is successful, parse the XML data into a dictionary using `xmltodict.parse`.
5. Initialize the `petrol_count` counter to keep track of gas stations.
6. Iterate through all nodes and ways in the OSM dictionary (specified as nodes and ways).
7. Check for the existence of the 'tag' key in the node or way (tags associated with the object).
8. If tags exist, check each tag for the presence of attributes @k and @v that correspond to a gas station.
9. If a tag represents a gas station, increment the `petrol_count` counter.
10. Output the number of gas stations found.
    This solution allows you to account for not only gas stations marked as points, but also those represented by contours 
on the OSM map fragment.




**Задача:**
Вася, открывший заправку в прошлом уроке, разорился. Конкуренция оказалась слишком большой. Вася предполагает, что это 
произошло от того, что теги заправки могут быть не только на точке, но и на каком-то контуре. Определите, сколько 
заправок на самом деле (не только обозначенных точкой) есть на фрагменте карты 
https://stepik.org/media/attachments/lesson/245681/map2.osm

**Решение:**
1. Импортируем необходимые библиотеки: xmltodict для разбора XML-данных и requests для выполнения HTTP-запроса.
2. Определяем URL-адрес фрагмента карты OSM.
3. Выполняем GET-запрос к URL-адресу и получаем XML-данные.
4. Если запрос успешен, разбираем XML-данные в словарь с помощью xmltodict.parse.
5. Инициализируем счетчик petrol_count для подсчета заправок.
6. Перебираем все узлы и линии в словаре OSM (указанные как nodes и ways).
7. Проверяем наличие ключа 'tag' у узла или линии (теги, связанные с объектом).
8. Если теги существуют, проверяем каждый тег на наличие атрибутов @k и @v, которые соответствуют заправке.
9. Если тег представляет заправку, увеличиваем счетчик petrol_count.
10. Выводит количество найденных заправок.
Это решение позволяет учесть не только точечные заправки, но и контуры, обозначающие заправки на фрагменте карты OSM.
###Task:
In OpenStreetMap XML, there are node tags that correspond to certain points on the map. Nodes can represent not only 
individual point objects but can also be part of a way (a line, possibly closed) and may not have their own tags. For 
the available fragment of the map at the link https://stepik.org/media/attachments/lesson/245678/map1.osm, calculate how
many nodes have at least one nested 'tag' tag, and how many do not. Provide the answer as two numbers separated by a 
space.

####Solution:
To solve this task:

1. Load the content of the file map1.osm from the provided link. We will use the 'requests' library to retrieve XML data
   from the specified URL.
2. Parse the XML data using the xmltodict library. After obtaining the data, we convert the XML into a Python data 
   structure using the 'xmltodict' library for easier manipulation.
3. Iterate through each 'node' element in the obtained data. We loop through the 'node' elements within the data 
   structure.
4. For each 'node' element, check for the presence of nested 'tag' tags. We check whether the current 'node' element 
   contains a nested 'tag' tag.
5. Based on the check, increment counters for nodes with nested 'tag' tags and nodes without tags. Depending on the 
   presence or absence of nested 'tag' tags, we update the corresponding counters.
6. Output the result: the number of nodes with nested 'tag' tags and the number of nodes without tags. After processing 
   all 'node' elements, we display the counts of nodes with nested 'tag' tags and nodes without such tags on the screen.




###Задача:
В OpenStreetMap XML встречаются теги node, которые соответствуют некоторым точкам на карте. Ноды могут не только 
обозначать какой-то точечный объект, но и входить в состав way (некоторой линии, возможно замкнутой) и не иметь 
собственных тегов. Для доступного по ссылке https://stepik.org/media/attachments/lesson/245678/map1.osm фрагмента карты 
посчитайте, сколько node имеет хотя бы один вложенный тэг tag, а сколько - не имеют. В качестве ответа введите два 
числа, разделённых пробелом.

####Решение:
Для решения этой задачи:

1. Загрузим содержимое файла map1.osm по указанной ссылке. Мы используем библиотеку requests, чтобы получить XML-данные 
   из указанного URL.
2. Используя библиотеку xmltodict, разберем XML-данные. После получения данных, мы преобразуем XML в структуру данных 
   Python с помощью библиотеки xmltodict, чтобы легче работать с содержимым.
3. Переберем каждый элемент node в полученных данных. Мы итерируем через элементы node внутри структуры данных.
4. Для каждого элемента node проверим наличие вложенных тегов tag. Мы проверяем, есть ли в текущем элементе node 
   вложенный тег tag.
5. На основе проверки, увеличим счетчик для узлов с вложенными тегами и для узлов без тегов. В зависимости от наличия 
   или отсутствия вложенных тегов tag, мы обновляем соответствующие счетчики.
6. Выведем результат: количество узлов с вложенными тегами и количество узлов без тегов. По окончании обработки всех 
   элементов node, мы выводим на экран количество узлов с вложенными тегами и количество узлов без таких тегов.
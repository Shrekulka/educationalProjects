This code solves the problem of obtaining location information associated with a given IP address. It sends 
GET request to "ip-api.com" web service using given IP address and gets JSON response. It then extracts 
the necessary data from the response and displays it, including the IP address, Internet service provider, organization,
country, name of region, city, postal code, and latitude and longitude (if available).

Additionally, if the IP address has latitude and longitude coordinates, the code creates a location map using the 
folium library and saves it as an HTML file. If no coordinates are available, a message is displayed saying that no 
coordinates are available.

The user enters the target IP address and the location information is then displayed.




Данный код решает задачу получения информации о местоположении, связанной с заданным IP-адресом. Он отправляет 
GET-запрос к веб-сервису "ip-api.com", используя заданный IP-адрес, и получает ответ в формате JSON. Затем он извлекает 
необходимые данные из ответа и выводит их на экран, включая IP-адрес, интернет-провайдера, организацию, страну, название
региона, город, почтовый индекс, а также широту и долготу (если доступны).

Дополнительно, если у IP-адреса есть координаты широты и долготы, код создает карту местоположения с помощью библиотеки 
folium и сохраняет ее в виде HTML-файла. Если координаты не доступны, выводится сообщение о их отсутствии.

Пользователь вводит целевой IP-адрес, после чего информация о его местоположении отображается на экране.
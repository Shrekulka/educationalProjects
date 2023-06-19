import requests
from pyfiglet import Figlet
import folium


def get_info_by_ip(ip='127.0.0.1'):
    """
        Возвращает информацию о местоположении на основе IP-адреса.

        Аргументы:
        ip (строка): IP-адрес для получения информации о местоположении. По умолчанию '127.0.0.1'.

        Возвращает:
        None

        Исключения:
        requests.exceptions.ConnectionError: Возникает, если есть проблема с подключением.

        """
    try:
        # Отправляет get-запрос на следующий url
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()

        # Создадим словарь и соберем данные для вывода
        data = {
            '[IP]': response.get('query'),
            '[Int prov]': response.get('isp'),
            '[Org]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region Name]': response.get('regionName'),
            '[City]': response.get('city'),
            '[ZIP]': response.get('zip'),
            '[Lat]': response.get('lat'),
            '[Lon]': response.get('lon '),
        }
        for key, value in data.items():
            print(f'{key} : {value}')

        # Получаем отдельную карту
        lat = response.get('lat')
        lon = response.get('lon')
        if lat is not None and lon is not None:
            area = folium.Map(location=[lat, lon])
            area.save(f'{response.get("query")}_{response.get("city")}.html')
        else:
            print('Latitude or longitude not available for the given IP.')

    except requests.exceptions.ConnectionError:
        print("!!! Please check your connection!!!!")


def main():
    """
       Основная функция для запуска программы.

       """
    # Красивый вывод в консоль
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('IP INFO'))
    ip = input("Please enter a target IP: ")
    get_info_by_ip(ip)


if __name__ == '__main__':
    main()

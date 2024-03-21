# lesson_first_file_server_with_fastapi/second_startup_option.py

"""
Этот модуль представляет собой простой файловый сервер, использующий FastAPI.

Он определяет функцию create_app(), которая создает экземпляр FastAPI и обработчики маршрутов для различных URL-адресов.
Обработчики маршрутов возвращают содержимое файла "index.html" по запросу.

Функционал:
- Корневой URL-адрес ("/") возвращает содержимое файла "index.html" для отображения в браузере.
- URL-адрес "/download" возвращает содержимое файла "index.html" для скачивания.
- URL-адрес "/custom_filename" возвращает содержимое файла "index.html" для скачивания с пользовательским именем файла.

Для запуска приложения используйте скрипт напрямую в IDE или выполните команду в терминале.

Здесь мы создаем функцию create_app(), которая создает экземпляр FastAPI. Затем мы используем строку
"second_startup_option:create_app" в uvicorn.run() для указания пути к функции, которая создает экземпляр FastAPI.
В "second_startup_option:create_app" мы указываем путь к нашему модулю, который содержит функцию create_app.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from logger_config import logger


def create_app() -> FastAPI:
    """
        Создает экземпляр FastAPI с заголовком "my_second_startup_option" и определяет обработчик маршрута для HTTP GET
        запросов на корневой URL "/".

        Возвращает созданный экземпляр FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "my_second_startup_option"
    app: FastAPI = FastAPI(title="my_second_startup_option")

    # Объявляем обработчик маршрута для HTTP GET запросов на корневой URL "/"
    @app.get("/")
    async def root() -> FileResponse:
        """
            Обработчик маршрута для HTTP GET запросов на корневой URL "/".

            Возвращает файл "index.html" в ответ на запрос.
        """
        # Возвращаем файл "index.html" в ответ на запрос
        return FileResponse("index.html")

    # Если добавить заголовок "Content-Disposition" со значением "attachment", то файл будет предложен для
    # скачивания, а не открытия в браузере
    @app.get("/download")
    async def download_file() -> FileResponse:
        """
            Обработчик маршрута для HTTP GET запросов на URL "/download".
            Возвращает файл "index.html" для скачивания.
        """
        headers = {"Content-Disposition": "attachment; filename=index.html"}
        return FileResponse("index.html", headers=headers)

    # Обработчик маршрута для скачивания файла "index.html" с пользовательским именем файла
    @app.get("/custom_filename")
    async def download_with_custom_filename() -> FileResponse:
        """
        Обработчик маршрута для HTTP GET запросов на URL "/custom_filename".
        Возвращает файл "index.html" для скачивания с пользовательским именем файла "my_custom_file.html".
        """
        # Определяем пользовательское имя файла
        custom_filename = "my_custom_file.html"

        # Создаем заголовок "Content-Disposition" с указанием пользовательского имени файла
        headers = {"Content-Disposition": f"attachment; filename={custom_filename}"}

        # Возвращаем FileResponse с файлом "index.html" и заголовками для скачивания
        return FileResponse("index.html", headers=headers)

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("second_startup_option:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

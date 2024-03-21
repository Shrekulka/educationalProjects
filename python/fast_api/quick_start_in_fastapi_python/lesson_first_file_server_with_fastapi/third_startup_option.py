# lesson_first_file_server_with_fastapi/third_startup_option.py

"""
Этот модуль представляет собой простой файловый сервер, использующий FastAPI.

Он определяет функцию create_app(), которая создает экземпляр FastAPI и обработчики маршрутов для различных URL-адресов.
Обработчики маршрутов возвращают содержимое файла "index.html" по запросу.

Функционал:
- Корневой URL-адрес ("/") возвращает содержимое файла "index.html" для отображения в браузере.
- URL-адрес "/download" возвращает содержимое файла "index.html" для скачивания.
- URL-адрес "/custom_filename" возвращает содержимое файла "index.html" для скачивания с пользовательским именем файла.

Также включен третий вариант решения, который использует HTMLResponse для чтения и возврата содержимого файла
"index.html".

Для запуска приложения используйте скрипт напрямую в IDE или выполните команду в терминале.

Здесь мы создаем функцию create_app(), которая создает экземпляр FastAPI. Затем мы используем строку
"third_startup_option:create_app" в uvicorn.run() для указания пути к функции, которая создает экземпляр FastAPI.
В "third_startup_option:create_app" мы указываем путь к нашему модулю, который содержит функцию create_app.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from logger_config import logger


def create_app() -> FastAPI:
    """
    Создает экземпляр FastAPI с заголовком "my_third_startup_option" и определяет обработчики маршрутов для различных
    URL-адресов.

    Возвращает созданный экземпляр FastAPI.
    """
    app: FastAPI = FastAPI(title="my_third_startup_option")

    # Объявляем обработчик маршрута для HTTP GET запросов на корневой URL "/"
    @app.get("/", response_class=HTMLResponse)
    async def root() -> HTMLResponse:
        """
        Обработчик маршрута для HTTP GET запросов на корневой URL "/".

        Читает содержимое файла "index.html" и возвращает его в виде HTML-ответа для отображения в браузере.
        """
        # Открываем файл "index.html" для чтения
        with open("index.html", encoding="UTF-8") as f:
            # Читаем содержимое файла
            html_content = f.read()

        # Возвращаем содержимое файла в виде HTML-ответа
        return HTMLResponse(content=html_content, status_code=200)

    # Обработчик маршрута для скачивания файла "index.html"
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
        custom_filename = "my_custom_file.html"
        headers = {"Content-Disposition": f"attachment; filename={custom_filename}"}
        return FileResponse("index.html", headers=headers)

    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("third_startup_option:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

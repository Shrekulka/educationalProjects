# lesson_first_file_server_with_fastapi/first_startup_option.py

"""
Этот модуль демонстрирует простой файловый сервер, использующий FastAPI.

Он создает экземпляр FastAPI с заголовком "my_first_startup_option" и определяет обработчик маршрута для HTTP GET
запросов на корневой URL "/". При получении таких запросов возвращает файл "index.html".

Для запуска приложения используйте скрипт напрямую. Например:
    uvicorn first_startup_option:app --reload

Посетите 'http://127.0.0.1:8000' в вашем веб-браузере, чтобы получить доступ к серверу.
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse

# Создаем экземпляр FastAPI с заголовком "my_first_startup_option"
app: FastAPI = FastAPI(title="my_first_startup_option")


# Объявляем обработчик маршрута для HTTP GET запросов на корневой URL "/"
@app.get("/")
async def root() -> FileResponse:
    """
        Обработчик маршрута для HTTP GET запросов на корневой URL "/".

        Возвращает файл "index.html" в ответ на запрос.
    """
    return FileResponse("index.html")

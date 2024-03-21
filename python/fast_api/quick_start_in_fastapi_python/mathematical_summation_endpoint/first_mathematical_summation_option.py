# mathematical_summation_endpoint/first_mathematical_summation_option.py

"""
Особенности данного решения:
- Для валидации данных используется Pydantic, что обеспечивает простоту и надежность работы с данными.
- Для обработки статических файлов, таких как HTML, используется Starlette, мощная библиотека для веб-приложений.
- Веб-приложение предоставляет форму для ввода двух чисел и вычисления их суммы.
- Обработчик POST-запроса на /calculate принимает данные в формате JSON, валидирует их с помощью модели Numbers,
  вычисляет сумму и возвращает результат в виде JSON.
- Запуск сервера осуществляется с использованием uvicorn, а настройки логирования предварительно настроены и
  импортированы из logger_config.
"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from logger_config import logger


class Numbers(BaseModel):
    """
      Модель данных Pydantic для валидации входных данных, представляющих два числа.

      Attributes:
          num1 (float): Поле, представляющее первое число (тип float).
          num2 (float): Поле, представляющее второе число (тип float).
    """
    num1: float  # Поле num1 типа float
    num2: float  # Поле num2 типа float


def create_app() -> FastAPI:
    """
        Создает и настраивает экземпляр приложения FastAPI.

        Returns:
            FastAPI: Настроенный экземпляр приложения FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "FastAPI Mathematical Summation Endpoint"
    app: FastAPI = FastAPI(title="FastAPI Mathematical Summation Endpoint")

    # Монтируем статические файлы из папки "templates" на корневой URL "/templates"
    app.mount("/templates", StaticFiles(directory="templates"), name="templates")

    # Обработчик для отображения страницы с формой вычисления
    @app.get("/calculate")
    def calculate_form() -> FileResponse:
        """
            Отображает HTML-форму для ввода чисел.

            Returns:
                FileResponse: Файловый объект, представляющий HTML-форму для ввода чисел.
        """
        # Возвращаем файл calculate.html
        return FileResponse("templates/calculate_first_option.html")

    # Добавляем обработчик для POST-запроса на /calculate
    @app.post("/calculate")
    async def calculate_sum(nums: Numbers) -> dict:
        """
            Вычисляет сумму двух чисел.

            Args:
                nums (Numbers): Объект модели данных Numbers, содержащий два числа для сложения.

            Returns:
                dict: Словарь с результатом вычисления суммы.
        """
        # Получаем числа из объекта модели данных
        num1 = nums.num1
        num2 = nums.num2
        # Вычисляем сумму чисел
        total = num1 + num2
        # Возвращаем результат в виде JSON
        return {"result": total}

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("first_mathematical_summation_option:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

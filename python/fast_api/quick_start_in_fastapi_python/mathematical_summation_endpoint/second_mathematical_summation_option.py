# mathematical_summation_endpoint/second_mathematical_summation_option.py

"""
В этом решении мы создаем простое веб-приложение с помощью FastAPI. Оно принимает два числа в качестве параметров в
строке запроса GET-запроса и возвращает их сумму в виде JSON-ответа.

Ключевые особенности:
- Использование FastAPI для создания веб-приложения.
- Параметры num1 и num2 передаются в строке запроса (query parameters) GET-запроса.
- Веб-приложение принимает два числа (num1 и num2) в виде параметров в строке запроса.
- Результат - сумма переданных чисел - возвращается в виде JSON-ответа.
- Не требуется дополнительных библиотек или валидации данных, работа с параметрами в строке запроса реализована напрямую
  в FastAPI.
- Простая и компактная реализация, подходящая для быстрого создания небольших веб-приложений.
- Запуск сервера осуществляется с использованием uvicorn, а настройки логирования импортируются из logger_config.

Пример строки запроса для GET-запроса:
http://127.0.0.1:5080/calculate?num1=5&num2=10

Этот URL указывает на /calculate с параметрами num1=5 и num2=10. В коде параметры num1 и num2 ожидаются как часть query
parameters, поэтому они должны быть переданы в виде части URL.
"""

import uvicorn
from fastapi import FastAPI, Form
from starlette.responses import FileResponse

from logger_config import logger


def create_app() -> FastAPI:
    """
        Создает и настраивает экземпляр приложения FastAPI.

        Returns:
            FastAPI: Настроенный экземпляр приложения FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "FastAPI Mathematical Summation Endpoint"
    app: FastAPI = FastAPI(title="FastAPI Mathematical Summation Endpoint")

    @app.get("/calculate", response_class=FileResponse)
    def calculate_form() -> FileResponse:
        """
            Обрабатывает GET-запросы на /calculate, возвращая файл calculate.html.

            Returns:
                FileResponse: Файл calculate.html.
        """
        # Возвращаем файл calculate.html
        return FileResponse("templates/calculate_second_option.html")

    @app.post("/calculate")
    def calculate_sum(
            num1: float = Form(..., ge=0.0, lt=999999.0,  # Должно быть больше или равно 0 и меньше 999999
                               alias="number1",  # Задаем альтернативное имя для параметра
                               title="Первое число",  # Задаем заголовок для параметра в документации
                               description="Это первое число для вычисления суммы",  # Добавляем описание в документацию
                               example=10.0,  # Задаем пример значения для документации
                               ),
            # Задаем значение по умолчанию 10.0 и значение должно быть больше или равно 0 и меньше 999999
            num2: float = Form(10.0, ge=0.0, lt=999999.0),
            precision: int = Form(2),  # Количество знаков после запятой в результате (по умолчанию 2)

    ) -> dict:
        """
           Функция для вычисления суммы двух чисел.

           Args:
               num1 (float): Первое число.
               num2 (float): Второе число.
               precision (int): Количество знаков после запятой в результате.

           Returns:
               dict: Словарь с ключом 'result', содержащий сумму чисел с заданной точностью.
        """
        total = num1 + num2
        total = round(total, precision)
        return {"result": total}

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("second_mathematical_summation_option:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

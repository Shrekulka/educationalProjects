# mathematical_summation_endpoint/third_mathematical_summation_option.py

"""
В FastAPI параметры, передаваемые в запросе GET, обычно ожидаются в строке запроса (query parameters). Поэтому, мы
должны передать параметры num1 и num2 в строке запроса.
Пример строки запроса для GET-запроса:
http://127.0.0.1:5080/calculate?num1=5&num2=10
Этот URL указывает на /calculate с параметрами num1=5 и num2=10. В нашем коде параметры num1 и num2 ожидаются как часть
query parameters, поэтому они должны быть переданы в виде части URL.
"""

import uvicorn
from fastapi import FastAPI

from logger_config import logger


def create_app() -> FastAPI:
    """
        Создает и настраивает экземпляр приложения FastAPI.

        Returns:
            FastAPI: Настроенный экземпляр приложения FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "FastAPI Mathematical Summation Endpoint"
    app: FastAPI = FastAPI(title="FastAPI Mathematical Summation Endpoint")

    @app.get("/calculate")
    async def calculate(num1: int, num2: int) -> dict:
        """
        Вычисляет сумму двух чисел.

        Parameters:
            num1 (int): Первое число для сложения.
            num2 (int): Второе число для сложения.

        Returns:
            dict: Словарь, содержащий сообщение о сумме переданных чисел.
        """
        total = f"Сумма чисел {num1} and {num2} равна: {num1 + num2}"
        # Вычисляем сумму двух чисел и возвращаем результат в виде словаря
        return {"result": total}

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("third_mathematical_summation_option:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

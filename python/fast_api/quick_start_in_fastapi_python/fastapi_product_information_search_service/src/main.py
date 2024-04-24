# fastapi_product_information_search_service/src/main.py
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from src.database import sample_products
from src.logger_config import logger
from src.models import Product


def create_app() -> FastAPI:
    """
        Создает экземпляр FastAPI приложения для обработки запросов, связанных с продуктами.

        Returns:
            FastAPI: Экземпляр FastAPI приложения.
    """
    # Создаем экземпляр FastAPI с заголовком "Fastapi Product Information Search Service"
    app: FastAPI = FastAPI(title="Fastapi Product Information Search Service")

    @app.get("/product/{product_id}", response_model=Product)
    async def get_product(product_id: int) -> Product:
        """
            Получает информацию о продукте по его идентификатору.

            Args:
                product_id (int): Идентификатор продукта.

            Returns:
                Product: Информация о продукте.

            Raises:
                HTTPException: Если продукт не найден, возвращает ошибку 404.
        """
        # Ищем продукт в списке sample_products с помощью генератора списков и функции next.
        # Функция next возвращает первый элемент, удовлетворяющий условию, или None, если такой элемент не найден.
        # Если продукт найден, он будет присвоен переменной product, в противном случае product будет равен None.
        product = next((i for i in sample_products if i["product_id"] == product_id), None)

        # Если продукт найден, создаем экземпляр класса Product, передавая ему данные из словаря product.
        if product:
            return Product(**product)
        # Если продукт не найден, возбуждаем исключение HTTPException с кодом состояния 404 (Not Found)
        # и сообщением "Product not found".
        else:
            raise HTTPException(status_code=404, detail="Product not found")

    @app.get("/products/search", response_model=List[Product])
    async def search_product(keyword: str, category: Optional[str] = None, limit: int = 10) -> List[Product]:
        """
           Ищет продукты по ключевому слову и (или) категории.

           Args:
               keyword (str): Ключевое слово для поиска товаров.
               category (str, optional): Категория для фильтрации товаров.
               limit (int, optional): Максимальное количество товаров для возврата. По умолчанию 10.

           Returns:
               List[Product]: Список найденных продуктов.
        """
        # Создаем список результатов, включающих продукты, у которых в имени содержится ключевое слово (keyword),
        # приведенное к нижнему регистру.
        results = [i for i in sample_products if keyword.lower() in i['name'].lower()]

        if category:
            # Если указана категория, фильтруем результаты, оставляя только продукты с указанной категорией.
            results = [i for i in results if i["category"] == category]

        # Создаем экземпляры класса Product для каждого продукта в отфильтрованном списке результатов,
        # а затем возвращаем только первые 'limit' элементов.
        return [Product(**i) for i in results[:limit]]

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("main:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

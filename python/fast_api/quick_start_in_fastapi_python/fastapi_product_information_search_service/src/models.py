# fastapi_product_information_search_service/src/models.py

from pydantic import BaseModel, Field


class Product(BaseModel):
    """
        Модель данных для представления информации о продукте.

        Attributes:
            product_id (int): Идентификатор продукта (целое число).
            name (str): Ключевое слово для поиска товара (строка, обязательно). Длина от 2 до 50 символов.
            category (str, optional): Категория для товара (строка, необязательно).
            price (float): Цена товара (число с плавающей запятой, обязательно).
    """

    product_id: int = Field(..., description="Идентификатор продукта (целое число)")

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Ключевое слово для поиска товара (строка, обязательна)"
    )

    category: str = Field(None, description="Категория для товара (строка, необязательно)")

    price: float = Field(..., description="Цена товара (float, обязательно)")

from typing import Optional, Literal

from django.db import models


# Определение модели Categories (категории товаров)
class Categories(models.Model):
    """
       A model representing categories of products.

       Attributes:
           name (str): The name of the category, limited to 150 characters.
           slug (str): The URL slug for the category, limited to 200 characters.
    """
    # Поле для названия категории, ограниченное до 150 символов, уникальное
    name: str = models.CharField(max_length=150, unique=True, verbose_name='Название')
    # Поле для URL-адреса категории, ограниченное до 200 символов, уникальное, может быть пустым
    slug: Optional[str] = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        """
            Meta options for Categories model.

            Attributes:
                db_table (str): The name of the database table.
                verbose_name (str): The human-readable name of the model in singular form.
                verbose_name_plural (str): The human-readable name of the model in plural form.
        """
        # Настройки метаданных модели
        db_table: str = 'category'  # Имя таблицы в базе данных
        verbose_name: str = 'категорию'  # Отображаемое название модели в единственном числе
        verbose_name_plural: str = 'категории'  # Отображаемое название модели во множественном числе

    # Метод для представления объекта в виде строки
    def __str__(self) -> str:
        """
           String representation of the category.

           Returns:
               str: The name of the category.
        """
        return self.name  # Возвращает название категории


# Определение модели Products (товара)
class Products(models.Model):
    """
       A model representing products.

       Attributes:
           name (str): The name of the product, limited to 150 characters.
           slug (str): The URL slug for the product, limited to 200 characters.
           description (str): The description of the product.
           image (str): The image of the product.
           price (float): The price of the product.
           discount (float): The discount percentage applied to the product.
           quantity (int): The quantity of the product.
           category (Categories): The category to which the product belongs.
    """
    # Поле для названия товара, ограниченное до 150 символов, уникальное
    name: str = models.CharField(max_length=150, unique=True, verbose_name='Название')
    # Поле для URL-адреса товара, ограниченное до 200 символов, уникальное, может быть пустым
    slug: Optional[str] = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    # Поле для описания товара, текстовое поле, может быть пустым
    description: Optional[str] = models.TextField(blank=True, null=True, verbose_name='Описание')
    # Поле для изображения товара
    image: Optional[str] = models.ImageField(upload_to='goods_images', blank=True, null=True,
                                             verbose_name='Изображение')
    # Поле для цены товара
    price: float = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    # Поле для скидки на товар, ограниченное до 4 символов, по умолчанию 0.00
    discount: float = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    # Поле для количества товара
    quantity: int = models.PositiveIntegerField(default=0, verbose_name='Количество')
    # Поле для связи с категорией товара, на удаление категории - удаление товара
    category: Categories = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')


    class Meta:
        """
           Meta options for Products model.

           Attributes:
               db_table (str): The name of the database table.
               verbose_name (str): The human-readable name of the model in singular form.
               verbose_name_plural (str): The human-readable name of the model in plural form.
        """
        # Настройки метаданных модели
        db_table: str = 'product'  # Имя таблицы в базе данных
        verbose_name: str = 'продукт'  # Отображаемое название модели в единственном числе
        verbose_name_plural: str = 'продукты'  # Отображаемое название модели во множественном числе
        ordering: tuple[Literal['id']] = ('id',)

    # Метод для представления объекта в виде строки
    def __str__(self) -> str:
        """
            String representation of the product.

            Returns:
                str: The name of the product along with its quantity.
        """
        return f"{self.name} количество - {self.quantity}"  # Возвращает строку с названием и количеством товара

    def display_id(self) -> str:
        return f"{self.id:05}"

    def sell_price(self) -> float:
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

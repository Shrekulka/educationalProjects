# book_shop/shop/models.py

from django.db import models


class Book(models.Model):

    title = models.CharField(max_length=255)

    # Ссылка на материал (латиница), или в простонародии ЧПУ-человеко-понятный урл, с максимальным количеством символов
    # 255, blank (необязательно к заполнению)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)

    autor_name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Book(title={self.title}, autor_name={self.autor_name}, price={self.price})>"

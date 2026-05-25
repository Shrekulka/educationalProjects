# book_shop/shop/models.py

from autoslug import AutoSlugField
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)

    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)

    author_name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Book(title={self.title}, author_name={self.author_name}, price={self.price})>"

from django.db import models


class Cinema(models.Model):
    title = models.CharField(max_length=40, verbose_name="Название")
    rating = models.IntegerField(default=0, null=True, verbose_name="Рейтинг")
    year = models.IntegerField(verbose_name="Год")
    budget = models.DecimalField(verbose_name="Бюджет")

    def __str__(self):
        return f"{self.title} - {self.rating}%"

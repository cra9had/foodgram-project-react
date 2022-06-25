from django.db import models

class Ingredient(models.Model):

    name = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента.'
    )

    amount = models.IntegerField(
        verbose_name='Количество ингредиента',
        help_text='Введите количество ингредиента.'
    )

    unit = models.CharField(
        max_length=250,
        verbose_name='Единицы измерения',
        help_text='Введите tдиницы измерения.'
    )
    
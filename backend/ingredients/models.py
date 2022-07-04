from django.db import models


class Ingredient(models.Model):

    name = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента.'
    )

    CHOICES = (
        ('кг', 'Килограмм'),
        ('г', 'грамм'),
        ('л', 'литров'),
        ('мл', 'милилитров'),
        )

    unit = models.CharField(
        max_length=2,
        verbose_name='Единицы измерения',
        help_text='Введите единицы измерения().',
        choices=CHOICES
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name

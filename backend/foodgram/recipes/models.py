from django.db import models
from django.contrib.auth import get_user_model
from ingredients.models import Ingredient
User=get_user_model()

class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта.'
    )

    name = models.CharField(
        max_length=250,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта.'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        verbose_name='Картинка',
        help_text='Можете добавить фото.'
    )

    description = models.TextField(
        default='',
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта.'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты для рецепта.'
    )

    tags = models.ManyToManyField(
        tag,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Тэги',
        help_text='Выберите теги для рецепта.'
    )

    time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах.'
    )

    def __str__(self):
        return self.name
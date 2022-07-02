from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from ingredients.models import Ingredient

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(
        max_length=250,
        verbose_name='Название тэга',
        help_text='Введите название тэга.'
    )

    hexcolour = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name='Цветовой HEX-код',
        help_text='Выберете цвет тэга.'
        )

    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        help_text='Введите slug тэга.'
        )

    def __str__(self):
        return self.slug


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
        Tag,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Тэги',
        help_text='Выберите теги для рецепта.'
    )

    time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах.',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.name

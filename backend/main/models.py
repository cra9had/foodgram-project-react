from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Follow(models.Model):
    """Модель подписки на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique follow')
        ]


class Favorite(models.Model):
    """Модель подписки на рецепт."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fan')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favouriting')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique favorite')
        ]


class Basket(models.Model):
    """Модель добавления рецепта в корзину."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='buying')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique basket')
        ]

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
        ordering = ['user', 'author']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique follow')
        ]

    def __str__(self):
        return '{} - {}'.format(self.user, self.author)


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
        ordering = ['user', 'recipe']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique favorite')
        ]

    def __str__(self):
        return '{} - {}'.format(self.user, self.recipe)


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
        ordering = ['user', 'recipe']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique basket')
        ]

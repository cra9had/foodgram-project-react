from django.forms import ModelForm
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'author', 'name', 'image', 'description',
            'ingredients', 'tags', 'time']
        labels = {
            'text': 'Текст рецепта',
            'group': 'Группа',
            'image': 'Картинка',
            'description': 'Описание',
            'ingredients': 'Ингредиенты',
            'tags': 'Тэги',
            'time': 'Время преготовлени в минутах'
        }

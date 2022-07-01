import tempfile
from django.contrib.auth import get_user_model

from foodgram.ingredients.models import Ingredient
from foodgram.recipes.models import Tag, Recipe

User = get_user_model()


class CreateTempData():
    def create_user():
        username = "testuser"
        email = "testuser@testbase.com"
        first_name = "Test"
        last_name = "User"
        password = "12345678"

        test_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        return test_user

    def create_ingredients():
        name = 'Мука'
        name2 = 'Соль'
        name3 = 'Молоко'

        unit = 'г'
        unit2 = 'мл'

        amount = 25
        amount2 = 200
        amount3 = 150

        test_ingredient = Ingredient.objects.create(
            name=name,
            amount=amount,
            unit=unit,
        )
        test_ingredient2 = Ingredient.objects.create(
            name=name2,
            amount=amount2,
            unit=unit,
        )
        test_ingredient3 = Ingredient.objects.create(
            name=name3,
            amount=amount3,
            unit=unit2,
        )
        return (test_ingredient, test_ingredient2, test_ingredient3)

    def create_tags():
        name = 'Завтрак'
        name2 = 'Обед'
        name3 = 'Ужин'

        hexcolour = '#e8eb34'
        hexcolour2 = '#5334eb'
        hexcolour3 = '#d934eb'

        slug = 'zavtrak'
        slug2 = 'obed'
        slug3 = 'ugin'

        test_tag = Tag.objects.create(
            name=name,
            hexcolour=hexcolour,
            slug=slug,
        )
        test_tag2 = Tag.objects.create(
            name=name2,
            hexcolour=hexcolour2,
            slug=slug2,
        )
        test_tag3 = Tag.objects.create(
            name=name3,
            hexcolour=hexcolour3,
            slug=slug3,
        )

        return (test_tag, test_tag2, test_tag3)

    def create_recipes(self):
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        author_exmpl = self.create_user()
        ingredients_exmpl = self.create_ingredients()
        tags_exmpl = self.create_tags()

        recipe_data = {
            'author': author_exmpl,
            'name': 'Блины',
            'name2': 'Хлеб',
            'name3': 'Лепёшки',
            'image': image,
            'description': 'Как приготовить Блины',
            'description2': 'Как приготовить Хлеб',
            'description3': 'Как приготовить Лепёшки',
            'ingredients': ingredients_exmpl,
            'tags': tags_exmpl,
            'time': 30,
            'time2': 90,
            'time3': 60,
        }

        test_recipe = Recipe.objects.create(
            author=recipe_data['author'],
            name=recipe_data['name'],
            image=recipe_data['image'],
            description=recipe_data['description'],
            ingredients=recipe_data['ingredients'],
            tags=recipe_data['tags'],
            time=recipe_data['time']
        )
        test_recipe2 = Recipe.objects.create(
            author=recipe_data['author'],
            name=recipe_data['name2'],
            image=recipe_data['image'],
            description=recipe_data['description2'],
            ingredients=recipe_data['ingredients'],
            tags=recipe_data['tags'],
            time=recipe_data['time2']
        )
        test_recipe3 = Recipe.objects.create(
            author=recipe_data['author'],
            name=recipe_data['name3'],
            image=recipe_data['image'],
            description=recipe_data['description3'],
            ingredients=recipe_data['ingredients'],
            tags=recipe_data['tags'],
            time=recipe_data['time3']
        )
        return (test_recipe, test_recipe2, test_recipe3)
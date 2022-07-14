from django.db.models import Sum
from recipes.models import RecipeIngredient


def ing_count(user):
    # ingredients = {}
    # ingredients_list = ''
    # for basket in baskets:
    #     print(basket.recipe.ingredients.all())
    #     for ingredient in basket.recipe.ingredients.all():
    #         amount = RecipeIngredient.objects.filter(
    #             recipe__).values(
    #             'ingredient__name',
    #             'ingredient__measurement_unit').annotate(total=Sum('amount'))
    #         desc = ingredients.setdefault(ingredient.name, [0, ingredient.unit])
    #         ingredients[ingredient.name] = (desc[0] + amount, desc[1])
    #
    # for name, desc in ingredients.items():
    #     amount, unit = desc
    #     ingredients_list += f'{name} - {amount}{unit}'
    # return ingredients_list
    ingredients = RecipeIngredient.objects.filter(
        recipe__buying__user=user).values(
        'ingredient__name',
        'ingredient__unit').annotate(total=Sum('amount'))

    shopping_list = 'список:\n'
    for number, ingredient in enumerate(ingredients, start=1):
        shopping_list += (
            f'{number} '
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["total"]} '
            f'{ingredient["ingredient__unit"]}\n')
    return shopping_list

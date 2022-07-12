
def ing_count(baskets):

    ingredients_for_buy = [[0 for x in range(1000)] for y in range(3)]
    for basket in baskets:
        for ingredient in basket.recipe.ingredients.all():
            cur_elmn_idx = ingredients_for_buy[0].index(ingredient.name)
            amount_add = ingredient.amount
            if ingredient.unit == 'л':
                amount_add = amount_add * 1000
                ingredients_for_buy[2][cur_elmn_idx] = 'мл'
            if ingredient.unit == 'кг':
                amount_add = amount_add * 1000
                ingredients_for_buy[2][cur_elmn_idx] = 'г'
            if ingredient.name in ingredients_for_buy[0]:
                ingredients_for_buy[1][cur_elmn_idx] = (
                    ingredients_for_buy[1][cur_elmn_idx] + amount_add)
            else:
                for idx, slot in enumerate(ingredients_for_buy[0]):
                    if slot != 0:
                        ingredients_for_buy[0][idx] = ingredient.name
                        ingredients_for_buy[1][idx] = amount_add
                        ingredients_for_buy[2][idx] = ingredient.unit

    for idx, ingredient in enumerate(ingredients_for_buy[0]):
        name = ingredients_for_buy[0][idx]
        amount = ingredients_for_buy[1][idx]
        unit = ingredients_for_buy[2][idx]
        if amount >= 1000 and unit == 'г':
            unit = 'кг'
            amount = round(amount/1000, 2)
        if amount >= 1000 and unit == 'мл':
            unit = 'л'
            amount = round(amount/1000, 2)

        if idx == 0:
            ingredients_list = ''
        else:
            ingredients_list = (ingredients_list + name + ' '
                                + (str(amount) + ' ' + unit + '/n'))
    print(ingredients_list)
    return ingredients_list

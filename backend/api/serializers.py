import base64
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from main.models import Basket, Favorite, Follow
from recipes.models import Recipe, RecipeIngredient, Tag
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return not user.is_anonymous and Follow.objects.filter(
            user=user,
            author=author.id
        ).exists()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name', 'last_name')


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Favorite.objects.filter(user=user, recipe__id=recipe).exists():
            raise serializers.ValidationError(
                {
                    "errors": "Рецепт уже в избранном"
                }
            )

        return {
            "user": User.objects.get(pk=data['user']['id']),
            "recipe": Recipe.objects.get(pk=data['recipe']['id'])
        }

    def create(self, validated_data):
        user = validated_data["user"]
        recipe = validated_data["recipe"]
        print(user, recipe)
        Favorite.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class CreateFollowSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Follow
        fields = ['user', 'author']

    def validate(self, data):
        user = data['user']['id']
        author = data['author']['id']
        follow_exist = Follow.objects.filter(
            user__id=user, author__id=author
        ).exists()
        if user == author:
            raise serializers.ValidationError(
                {"errors": 'Вы не можете подписаться на самого себя'}
            )
        elif follow_exist:
            raise serializers.ValidationError({"errors": 'Вы уже подписаны'})
        return data

    def create(self, validated_data):
        author = validated_data.get('author')
        author = get_object_or_404(User, pk=author.get('id'))
        user = User.objects.get(id=validated_data["user"]["id"])
        Follow.objects.create(user=user, author=author)
        return validated_data


class RecipeFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]


class ShowFollowsSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, author):
        return author.recipes.count()

    def get_recipes(self, author):
        recipes = author.recipes.all()
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit'
        )
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeMinifiedSerializer(recipes, many=True).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Basket
        fields = '__all__'

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Basket.objects.filter(user=user, recipe__id=recipe).exists():
            raise serializers.ValidationError(
                {
                    'errors': 'рецепт уже в корзине'
                }
            )
        return {"user": User.objects.get(pk=user),
                "recipe": Recipe.objects.get(pk=recipe)}

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        Basket.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']

    @staticmethod
    def get_measurement_unit(obj):
        return obj.unit


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name', read_only=True)
    unit = serializers.ReadOnlyField(
        source='ingredient.unit', read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'unit')


class IngredientAmountCreate(IngredientAmountSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    def validate_amount(self, amount):
        if amount < 1:
            raise serializers.ValidationError(
                'Значение не может быть меньше 0.'
            )
        return amount

    def to_representation(self, instance):
        ingredient_in_recipe = [
            item for item in
            Ingredient.objects.filter(id=instance.id)
        ]
        return IngredientAmountSerializer(ingredient_in_recipe).data


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.unit")

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(source="recipe_ingredients",
                                               many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Basket.objects.filter(user=request.user, recipe=obj).exists()

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'В рецепте не заполнены ингредиенты!')
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError('В рецепте не заполнены теги!')
        return tags

    def validate_image(self, image):
        if not image:
            raise serializers.ValidationError('Добавьте картинку рецепта!')
        return image

    def validate_name(self, name):
        if not name:
            raise serializers.ValidationError('Не заполнено название рецепта!')
        if self.context.get('request').method == 'POST':
            current_user = self.context.get('request').user
            if Recipe.objects.filter(author=current_user, name=name).exists():
                raise serializers.ValidationError(
                    'Рецепт с таким названием у вас уже есть!'
                )
        return name

    def validate_text(self, text):
        if not text:
            raise serializers.ValidationError('Не заполнено описание рецепта!')
        return text

    def validate_cooking_time(self, cooking_time):
        if not cooking_time:
            raise serializers.ValidationError(
                'Не заполнено время приготовления рецепта!')
        return cooking_time

    def create_recipe_ingredients(self, ingredients, recipe):
        for i in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=i.get('id'),
                amount=i.get('amount'),
            )

    @staticmethod
    def base64_file(data, name=None):
        _format, _img_str = data.split(';base64,')
        _name, ext = _format.split('/')
        if not name:
            name = _name.split(":")[-1]
        return ContentFile(base64.b64decode(_img_str),
                           name='{}.{}'.format(name, ext))

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.ingredients.clear()
        self.create_recipe_ingredients(
            self.validate_ingredients(self.initial_data.get('ingredients', instance.ingredients)), instance)
        instance.name = validated_data.get('name', instance.name)
        img = validated_data.get('image')
        if not img:
            img = instance.image
        else:
            img = self.base64_file(img)
        instance.image = img
        instance.text = validated_data.get('text', instance.text)
        instance.tags.set(self.validate_tags(self.initial_data.get('tags', instance.tags)))
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        current_user = self.context.get('request').user
        ingredients = self.validate_ingredients(
            self.initial_data.get('ingredients')
        )
        name = self.validate_name(
            self.initial_data.get('name')
        )
        image = self.base64_file(self.validate_image(
            self.initial_data.get('image')
        ))
        text = self.validate_text(
            self.initial_data.get('text')
        )
        tags = self.validate_tags(
            self.initial_data.get('tags')
        )
        cooking_time = self.validate_cooking_time(
            self.initial_data.get('cooking_time')
        )
        recipe = Recipe.objects.create(
            author=current_user,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time
        )
        self.create_recipe_ingredients(
            ingredients,
            recipe
        )
        recipe.tags.set(tags)
        return recipe


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', 'author')


class FollowerSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    @staticmethod
    def get_is_subscribed(obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()

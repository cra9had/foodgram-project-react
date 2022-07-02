from django.urls import include, path
from main.views import (BasketView, IngredientViewSet, RecipeViewSet,
                        TagsViewSet, download_basket)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/<int:recipe_id>/basket/', BasketView.as_view(),
         name='shopping_cart'),
    path('recipes/download_basket/', download_basket,
         name='download_shopping_cart'),
    path('', include(router.urls)),
]

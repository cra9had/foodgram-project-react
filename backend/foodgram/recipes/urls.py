from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main.views import (IngredientViewSet, RecipeViewSet, BasketView,
                    TagsViewSet, download_basket)

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
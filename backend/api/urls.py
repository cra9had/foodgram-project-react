from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from main.views import IngredientViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]

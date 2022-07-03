from django.urls import include, re_path
from main.views import IngredientViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]

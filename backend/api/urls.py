from django.urls import include, path
from main.views import IngredientViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]

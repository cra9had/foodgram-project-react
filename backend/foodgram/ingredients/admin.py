import imp

from django.contrib import admin

from .models import Ingredient


# todo
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ('author', 'name', 'tags')

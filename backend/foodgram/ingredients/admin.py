from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('id', 'name', 'unit',)
    search_fields = ('name',)

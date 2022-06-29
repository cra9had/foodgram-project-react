from django.contrib import admin
from main.models import Favorite

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('fan_count',)

    def fan_count(self, obj):
        count = Favorite.objects.filter(recipe = obj).count()
        return count
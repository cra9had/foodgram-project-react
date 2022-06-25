from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from recipes.forms import RecipeForm
from .models import Follow

User=get_user_model()


def paginator_my(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    recipe_list = Recipe.objects.all()
    page_obj = paginator_my(request, recipe_list)
    if len(request.GET) != 0:
        cache.clear()
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'recipes/index.html', context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = recipe.author
    full_name = author.get_full_name()
    recipe_count = author.recipe.all().count()
    context = {
        'recipe': recipe,
        'author': author,
        'full_name': full_name,
        'recipe_count': recipe_count,
    }
    return render(request, 'recipe/recipe_detail.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    full_name = author.get_full_name()

    recipe_list = author.posts.all()
    recipe_count = recipe_list.count()
    page_obj = paginator_my(request, recipe_list)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author
        )
    else:
        following = False

    context = {
        'page_obj': page_obj,
        'recipe_count': recipe_count,
        'full_name': full_name,
        'author': author,
        'following': following,
    }
    return render(request, 'recipes/profile.html', context)


@login_required
def recipe_create(request):

    form = RecipeForm(request.POST or None, files=request.FILES or None)
    context = {
        'form': form,
    }
    if form.is_valid() and request.method == 'POST':
        form_obj = form.save(commit=False)
        form_obj.author = request.user
        form_obj.save()
        return redirect('recipes:profile', username=request.user)
    else:
        return render(request, 'recipes/create_post.html', context)


def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user:
        return redirect('recipes:recipe_detail', recipe_id=recipe_id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        return redirect('recipes:recipe_detail', recipe_id=recipe_id)
    context = {
        'recipe': recipe,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'recipes/create_recipe.html', context)


@login_required
def follow_index(request):
    recipe_list = Recipe.objects.filter(author__following__user=request.user)
    page_obj = paginator_my(request, recipe_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'recipes/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('recipes:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('recipes:profile', username)


# todo избранные рецепты


# todo Список покупок


# todo Фильтрация по тегам
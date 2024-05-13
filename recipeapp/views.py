from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import RecipeForm
from .models import Recipe, Category, Relation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


def index(request):
    categories = Category.objects.all()
    relation = Relation.objects.all().order_by('-id')[:5]
    return render(request, 'index.html', {'categories': categories, 'relation': relation})


def recipe_desc(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_desc.html', {'recipe': recipe})


@login_required(login_url='/accounts/login/')
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.image = request.FILES['image']

            current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
            file_extension = recipe.image.name.split('.')[-1]
            file_name = f"{current_time}.{file_extension}"
            recipe.image.name = file_name
            recipe.save()

            # Получение категории из формы и сохранение связи
            category_id = request.POST.get('category')
            category = Category.objects.get(pk=category_id)
            Relation.objects.create(recipe=recipe, category=category)

            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'recipe_add.html', {'form': form})

def recipe_edit(request, recipe_id):
    # Получение рецепта
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            # Сохранение рецепта
            form.save()
            return redirect('index')
    else:
        # Получение связей категорий для этого рецепта
        relation = Relation.objects.filter(recipe=recipe)
        # Получение первой связи категории, если она существует
        if relation.exists():
            category = relation.first().category
        else:
            category = None
        # Передача категории в форму при создании экземпляра формы
        form = RecipeForm(instance=recipe, initial={'category': category})

    return render(request, 'recipe_form.html', {'form': form, 'recipe': recipe})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Некорректное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
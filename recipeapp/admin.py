from django.contrib import admin
from .models import Recipe, Category, Relation

admin.site.register(Recipe)

admin.site.register(Category)

admin.site.register(Relation)
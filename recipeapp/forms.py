from django import forms
from .models import Recipe, Category, Relation


class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'instructions', 'time_prepare', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'time_prepare': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'ingredients': 'Ингредиенты',
            'instructions': 'Инструкции',
            'time_prepare': 'Время приготовления (в минутах)',
            'image': 'Фото',
            'category': 'Категория',
        }
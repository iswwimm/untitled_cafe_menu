from django import forms
from menu.models import Coffee, Toast, Sweet

class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'group', 'price', 'price_2', 'temperature', 'description', 'is_active']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional description for coffee information modal'}),
        }
        labels = {
            'price': 'Основна ціна',
            'price_2': 'Друга ціна',
            'description': 'Опис кави (для інформаційного вікна)',
        }

class ToastForm(forms.ModelForm):
    class Meta:
        model = Toast
        fields = ['name', 'image', 'ingredients', 'description', 'allergens', 'price', 'is_active']

class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = ['name', 'image', 'ingredients', 'description', 'allergens', 'price', 'is_active']

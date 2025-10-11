from django import forms
from menu.models import Coffee, Toast, Sweet

class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'price', 'price_2', 'temperature', 'is_active']
        widgets = {
            'temperature': forms.Select(),
        }
        labels = {
            'price': 'Основна ціна',
            'price_2': 'Друга ціна',
        }

class ToastForm(forms.ModelForm):
    class Meta:
        model = Toast
        fields = ['name', 'image', 'ingredients', 'description', 'allergens', 'price', 'is_active']

class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = ['name', 'image', 'ingredients', 'description', 'allergens', 'price', 'is_active']

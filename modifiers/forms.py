from django import forms
from menu.models import Coffee, Toast, Sweet, CoffeeVolume

class CoffeeForm(forms.ModelForm):
    volume = forms.ModelMultipleChoiceField(
        queryset=CoffeeVolume.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Volumes"
    )

    class Meta:
        model = Coffee
        fields = ['name', 'price', 'volume', 'temperature', 'is_active']
        widgets = {
            'temperature': forms.Select(),
        }

class ToastForm(forms.ModelForm):
    class Meta:
        model = Toast
        fields = ['name', 'image', 'ingredients', 'description', 'allergens', 'price', 'is_active']

class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = ['name', 'image', 'ingredients', 'description', 'allergens', 'price', 'is_active']

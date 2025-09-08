# modifiers/forms.py
from django import forms
from menu.models import Coffee, Toast, Sweet

class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = '__all__'

class ToastForm(forms.ModelForm):
    class Meta:
        model = Toast
        fields = '__all__'

class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = '__all__'

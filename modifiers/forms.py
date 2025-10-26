from django import forms
from menu.models import Coffee, Toast, Sweet

class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'group', 'price', 'price_2', 'temperature', 'image', 'description', 'is_active']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional description for coffee information modal'}),
        }
        labels = {
            'price': 'Main Price',
            'price_2': 'Second Price',
            'description': 'Coffee Description (for information modal)',
            'image': 'Coffee Image',
        }

class ToastForm(forms.ModelForm):
    allergens = forms.MultipleChoiceField(
        choices=[
            ('1', '1 - Gluten'),
            ('2', '2 - Dairy'),
            ('3', '3 - Nuts'),
            ('4', '4 - Eggs'),
            ('5', '5 - Soy'),
            ('6', '6 - Sesame'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'allergens-checkboxes'}),
        required=False,
        label='Allergens'
    )
    
    class Meta:
        model = Toast
        fields = ['name', 'image', 'description', 'allergens', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional description for toast information modal'}),
        }
        labels = {
            'description': 'Toast Description (for information modal)',
            'image': 'Toast Image',
        }

class SweetForm(forms.ModelForm):
    allergens = forms.MultipleChoiceField(
        choices=[
            ('1', '1 - Gluten'),
            ('2', '2 - Dairy'),
            ('3', '3 - Nuts'),
            ('4', '4 - Eggs'),
            ('5', '5 - Soy'),
            ('6', '6 - Sesame'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'allergens-checkboxes'}),
        required=False,
        label='Allergens'
    )
    
    class Meta:
        model = Sweet
        fields = ['name', 'image', 'description', 'allergens', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional description for sweet information modal'}),
        }
        labels = {
            'description': 'Sweet Description (for information modal)',
            'image': 'Sweet Image',
        }

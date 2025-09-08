from django.contrib import admin
from .models import Coffee, Toast, Sweet

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'milk_alternatives', 'preparation_method')

@admin.register(Toast)
class ToastAdmin(admin.ModelAdmin):
    list_display = ('name', 'preparation_method')

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'preparation_method')

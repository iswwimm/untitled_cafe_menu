from django.contrib import admin
from menu.models import Coffee, CoffeeVolume, Toast, Sweet

@admin.register(CoffeeVolume)
class CoffeeVolumeAdmin(admin.ModelAdmin):
    list_display = ('volume',)

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'display_volumes', 'temperature')
    list_filter = ('temperature',)
    search_fields = ('name',)

    def display_volumes(self, obj):
        return ", ".join([v.volume for v in obj.volume.all()])
    display_volumes.short_description = 'Volumes'

@admin.register(Toast)
class ToastAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'allergens', 'price')
    search_fields = ('name', 'ingredients', 'allergens', 'price')

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'allergens', 'price')
    search_fields = ('name', 'ingredients', 'allergens', 'price')

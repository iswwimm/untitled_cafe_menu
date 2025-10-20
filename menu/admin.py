from django.contrib import admin
from django.utils.html import format_html
from .models import Coffee, Toast, Sweet


@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'price', 'is_active', 'display_volumes', 'temperature')
    list_filter = ('is_active', 'temperature', 'group')
    search_fields = ('name',)
    actions = ('make_active', 'make_inactive')
    fields = ('name', 'group', 'price', 'temperature', 'image', 'is_active')

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected as inactive"


@admin.register(Toast)
class ToastAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'ingredients', 'allergens')
    actions = ('make_active', 'make_inactive')

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'ingredients', 'allergens')
    actions = ('make_active', 'make_inactive')

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

from django.shortcuts import render
from .models import Coffee, Toast, Sweet

def home(request):
    return render(request, 'menu/home.html')

def coffee_list(request):
    coffees = Coffee.objects.filter(is_active=True)
    return render(request, 'menu/coffee.html', {'coffees': coffees})

def toasts_list(request):
    toasts = Toast.objects.filter(is_active=True)
    return render(request, 'menu/toasts.html', {'toasts': toasts})

def sweets_list(request):
    sweets = Sweet.objects.filter(is_active=True)
    return render(request, 'menu/sweets.html', {'sweets': sweets})

from django.shortcuts import render
from .models import Coffee, Toast, Sweet

def home(request):
    return render(request, 'menu/home.html')

def coffee_menu(request):
    coffees = Coffee.objects.all()
    return render(request, 'menu/coffee.html', {'coffees': coffees})

def toast_menu(request):
    toasts = Toast.objects.all()
    return render(request, 'menu/toasts.html', {'toasts': toasts})

def sweet_menu(request):
    sweets = Sweet.objects.all()
    return render(request, 'menu/sweets.html', {'sweets': sweets})

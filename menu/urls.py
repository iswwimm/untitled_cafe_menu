from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('coffee/', views.coffee_menu, name='coffee'),
    path('toasts/', views.toast_menu, name='toasts'),
    path('sweets/', views.sweet_menu, name='sweets'),
]

from django.urls import path
from . import views

app_name = 'modifiers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Coffee
    path('coffee/add/', views.add_coffee, name='add_coffee'),
    path('coffee/edit/<int:pk>/', views.edit_coffee, name='edit_coffee'),
    path('coffee/delete/<int:pk>/', views.delete_coffee, name='delete_coffee'),

    # Toast
    path('toast/add/', views.add_toast, name='add_toast'),
    path('toast/edit/<int:pk>/', views.edit_toast, name='edit_toast'),
    path('toast/delete/<int:pk>/', views.delete_toast, name='delete_toast'),

    # Sweet
    path('sweet/add/', views.add_sweet, name='add_sweet'),
    path('sweet/edit/<int:pk>/', views.edit_sweet, name='edit_sweet'),
    path('sweet/delete/<int:pk>/', views.delete_sweet, name='delete_sweet'),
]

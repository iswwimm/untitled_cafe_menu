# modifiers/urls.py
from django.urls import path
from . import views

app_name = 'modifiers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/<str:category>/', views.add_item, name='add_item'),
    path('edit/<str:category>/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete/<str:category>/<int:pk>/', views.delete_item, name='delete_item'),
]

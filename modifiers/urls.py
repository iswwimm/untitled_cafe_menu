from django.urls import path
from . import views

app_name = 'modifiers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('archive/', views.archive, name='archive'),

    path('<str:category>/add/', views.add_item, name='add_item'),
    path('<str:category>/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('<str:category>/delete/<int:pk>/', views.delete_item, name='delete_item'),

    path('<str:category>/archive/<int:pk>/', views.archive_item, name='archive_item'),
    path('<str:category>/restore/<int:pk>/', views.restore_item, name='restore_item'),
]

from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('coffee/', views.coffee_list, name='coffee'),
    path('toasts/', views.toasts_list, name='toasts'),
    path('sweets/', views.sweets_list, name='sweets'),
    path('update-order/<str:model_type>/', views.update_order, name='update_order'),
]

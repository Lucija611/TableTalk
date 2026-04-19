from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/<int:restaurant_id>/comment/', views.add_comment, name='add_comment'),
    path('statistics/', views.owner_statistics, name='owner_statistics'),
]
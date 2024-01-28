from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dice/', views.dice, name='dice'),
    path('coin/', views.coin, name='coin'),
    path('random_hundred/', views.random_hundred, name='random_hundred'),
]

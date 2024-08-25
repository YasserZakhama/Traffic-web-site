# network/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.packet_list, name='packet_list'),
    path('clear-and-capture/', views.clear_and_capture, name='clear_and_capture'),
]

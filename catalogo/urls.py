# catalogo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Módulo Público
    path('', views.catalogo, name='catalogo'),
    path('celular/<int:pk>/', views.detalle_celular, name='detalle_celular'),
    path('gestion/dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('gestion/tutoriales/', views.tutoriales, name='tutoriales'),
    path('gestion/dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('gestion/tutoriales/', views.tutoriales, name='tutoriales'), 
    path('gestion/reserva/confirmar/<int:pk>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('gestion/reserva/cancelar/<int:pk>/', views.cancelar_reserva, name='cancelar_reserva'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('solicitar-prestamo/', views.solicitar_prestamo_view, name='solicitar_prestamo'),
    
]
from django.urls import path
from . import views

urlpatterns = [
    path('medicoes/', views.listar_medicoes, name='listar_medicoes'),
    path('', views.home, name='home'),  # Página inicial
]

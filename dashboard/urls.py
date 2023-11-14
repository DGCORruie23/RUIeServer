from django.urls import path
from . import views

urlpatterns = [
     path('', views.dashboard, name="dashboard"),
     path('datos/', views.mostrarData, name="mostrar"),
     path('editar/<int:pk>', views.editarData, name="editar"),
]


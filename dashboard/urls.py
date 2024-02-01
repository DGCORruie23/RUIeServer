from django.urls import path
from . import views

urlpatterns = [
     path('', views.dashboard, name="dashboard"),
     path('datos/', views.mostrarData, name="mostrar"),
     path('editar/<int:pk>', views.editarData, name="editar"),
     path('datos/fecha', views.datos_fecha, name="datos_por_fecha"),
     path('datos/eliminarM', views.eliminar_registros, name="eliminar_varios_registros"),
     path('datos/<int:year>/<int:month>/<int:day>/', views.tabla_registros, name='tabla_registros_fecha'),
]


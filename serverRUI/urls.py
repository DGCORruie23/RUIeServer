"""
URL configuration for serverRUI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuario import views
from usuarioL.views import index
from django.contrib.auth import views as viewsL

urlpatterns = [
    path('', index, name="index"),

    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('log-in/', viewsL.LoginView.as_view(template_name= 'base/log_in.html'), name='log-in'),
    path('log-out', viewsL.LogoutView.as_view(), name="logout" ),

    path('login/', include('usuario.urls')),
    path('info/cargarPais', views.cargarPais),
    path('info/cargarFuerza', views.cargarEdoFuerza),
    path('info/cargarMunicipios', views.cargarMunicipios),
    path('info/cargarPuntosI', views.cargarPuntoI),
    path('info/Paises', views.infoPaises),
    path('info/Fuerza', views.infoEstadoFuerza),
    path('info/Municipios', views.infoMunicipios),
    path('info/PuntosI', views.infoPuntosInterna),
    path('info/frases', views.infoFrases),
    path('info/descargaN', views.generarExcelNombres),
    path('info/descargaC', views.generarExcelConteo),
    path('info/descargaD', views.pagDuplicados),
    path('info/descargaD_a', views.downloadDuplicados, name="descarga_duplicados"),
    path('info/descargaTab22', views.generarExcelTab),
    path('info/descargaExcel', views.generarExcelORs, name="descarga_excel"),

    path('registro/insertR', views.insert_rescates),
    path('registro/insertC', views.insert_conteo),
    path('descargas/', views.servirApps, name="descargas"),
    path('descargas/apk', views.downloadAPK, name="descarga_android"),
]

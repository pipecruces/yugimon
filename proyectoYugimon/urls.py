"""
URL configuration for proyectoYugimon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from plataformaYugimon.views import *
from django.views.generic.base import TemplateView
from plataformaYugimon.views import mostrarBanlist

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ingresarCarta/', ingresarCarta, name='ingresarCarta'),
    path('tablaCartas/', tablaCartas, name='tablaCartas'),
    path('editarCarta/<int:id>', editarCarta, name='editarCarta'),
    path('eliminarCarta/<int:id>', eliminarCarta, name='eliminarCarta'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('usuarios/', include('plataformaYugimon.urls')),
    path('mostrarBanlist/', mostrarBanlist, name='mostrarBanlist'),
    path('crearMazo/<int:mazo_id>', crear_mazo, name='crear_mazo'),
    path('agregar_carta/<int:mazo_id>,<int:carta_id>', agregar_carta_a_mazo, name='agregar_carta'),
    path('quitar_carta/<int:mazo_id>,<int:carta_id>', quitar_carta_de_mazo, name='quitar_carta'),

]

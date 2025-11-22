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
from django.contrib.auth.decorators import login_required

urlpatterns = [

    #Direcciones para las funcionalidades del panel admin
    path('admin/', admin.site.urls),

    #CRUD Cartas
    path('ingresarCarta/', ingresarCarta, name='ingresarCarta'),
    path('tablaCartas/', tablaCartas, name='tablaCartas'),
    path('editarCarta/<int:id>', editarCarta, name='editarCarta'),
    path('eliminarCarta/<int:id>', eliminarCarta, name='eliminarCarta'),

    #Crud Banlist ****
    path('mostrarBanlist/', mostrarBanlist, name='mostrarBanlist'),

    #Autenticación y home
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('usuarios/', include('plataformaYugimon.urls')),

    #URLS de publicaciones de intercambio
    path('publicacionCartas/', login_required(PublicacionCartaView.as_view()), name="publicacionCarta"),
    path('articuloCartas/<int:pk>', login_required(PublicacionCartaDetail.as_view()), name="detallePublicacion"),
    path('escribirPostCarta/', login_required(EscribirPostCarta.as_view()), name="postCarta"),
    path('editarPostCarta/<int:pk>', login_required(EditarPostCarta.as_view()), name="editarPostCarta"),
    path('eliminarPostCarta/<int:pk>', login_required(EliminarPostCarta.as_view()), name="eliminarPostCarta"),
    #Filtros de categoria
    path('publicacionCartas/<str:categorias>', CategoriaView, name='categoria')

]

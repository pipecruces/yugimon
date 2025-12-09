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
from django.contrib.auth.decorators import login_required
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [

    #Direcciones para las funcionalidades del panel admin
    path('admin/', admin.site.urls),

    #CRUD Cartas
    path('ingresarCarta/', ingresarCarta, name='ingresarCarta'),
    path('tablaCartas/', tablaCartas, name='tablaCartas'),
    path('editarCarta/<int:id>', editarCarta, name='editarCarta'),
    path('eliminarCarta/<int:id>', eliminarCarta, name='eliminarCarta'),

    #Crud Banlist ****
    path('mostrarBanlist/', MostrarCartasBanlistView.as_view(), name='mostrarBanlist'),
    path('agregarBanlist/', login_required(CrearBanlist.as_view()), name='agregarCartasBanlist'),
    path('editarBanlist/<int:pk>', login_required(editarBanlist.as_view()), name='editarBanlist'),

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

    #Publicaciones de venta de mazos
    
    path('escribirPostVentaMazos/', login_required(EscribirPostVentaMazo.as_view()), name="escribirPostVentaMazos"),
    path('publicacionesMazos/', login_required(PublicacionesMazosListView.as_view()), name='listarPublicacionesMazos'),
    path('publicacionVentaMazos/<int:pk>/', login_required(PublicacionVentaMazoView.as_view()), name='detallesPublicacionVentaMazos'),
    path('eliminarPostVentaMazos/<int:pk>', login_required(EliminarVentaMazos.as_view()), name="eliminarPostVentaMazos"),
    path('editarPostVentaMazos/<int:pk>', login_required(EditarPostVentaMazos.as_view()), name="editarPostVentaMazos"),


    #CRUD MAZOS
    path('crearMazo/', crear_mazo, name='crearMazo'),
    path("mazo/<int:mazo_id>/editar/", editar_mazo, name="editar_mazo"),
    path("mazo/update/", update_mazo, name="update_mazo"),
    path("mazo/update/ajax/", update_mazo_ajax, name="update_mazo_ajax"),
    path('verCartas/', CartaView.as_view(), name="verCartas"),
    path("mazos/", listarMazos, name="listarMazos"),
    path("misMazos/", misMazos, name="misMazos"),
    path("mazo/<int:mazo_id>/ver/", verMazo, name="verMazo"),
    path("mazo/<int:mazo_id>/eliminar/", eliminarMazo, name="eliminarMazo"),
    path('comparador/datos_mazo/<int:mazo_id>/', obtener_datos_mazo, name='obtener_datos_mazo'),
    path('comparador/', login_required(ComparadorMazo.as_view()),name='comparador'),

    #Comentarios
    path('mazo/<int:pk>/ver/crearComentario', login_required(CrearComentario.as_view()), name="comentario"),
    path('editarComentario/<int:pk>/', login_required(EditarComentario.as_view()), name="editarComentario"),
    path('eliminarComentario/<int:pk>/', login_required(EliminarComentario.as_view()), name="eliminarComentario"),

    path('comentario/<int:pk>/responder/', login_required(CrearRespuestaComentario.as_view()), name="responderComentario"),
    path('editarRespuesta/<int:pk>/', login_required(EditarRespuestaComentario.as_view()), name="editarRespuesta"),
    path('eliminarRespuesta/<int:pk>/', login_required(EliminarRespuestaComentario.as_view()), name="eliminarRespuesta"),


    #Notificaciones
    path("me-interesa/<int:pk>/", me_interesa, name="me_interesa"),
    path("notificaciones/", listar_todas_notificaciones, name="todas_notificaciones"),
    path("me-interesa-intercambio/<int:pk>/", me_interesa_intercambio, name="me_interesa_intercambio"),
    path("notificaciones/<int:pk>/leer/", leer_notificacion, name="leer_notificacion"),

] + debug_toolbar_urls()

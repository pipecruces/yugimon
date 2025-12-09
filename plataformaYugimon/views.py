from django.shortcuts import render, redirect, get_object_or_404
from plataformaYugimon.models import *
from plataformaYugimon.forms import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.views.decorators.http import  require_POST
from django.http import JsonResponse
import json
from django.db.models import Sum, F, Avg, Count, Q
from .models import Edicion, Tipo, Raza
from django.core.paginator import Paginator

# Create your views here.

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangedForm
    success_url = reverse_lazy('home')

def SignUpView(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistroUsuario()
        
    data = {'form': form}
    return render(request, 'registration/signup.html', data)

#Editar Cuenta
class EditarCuentaView(generic.UpdateView):
    form_class = EditarUsuario
    template_name = 'registration/editarPerfil.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


@user_passes_test(lambda u: u.is_superuser)
def ingresarCarta(request):
    form = RegistroCarta()

    if request.method == 'POST':
        form = RegistroCarta(request.POST)
        if form.is_valid():
            carta = form.save(commit=False)
            carta.id_usuario = request.user  
            carta.save()
            return HttpResponseRedirect(reverse('tablaCartas'))

    return render(request, 'plataformaYugimon/formularioCartas.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def editarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    form = RegistroCarta(instance = cartas)
    if request.method == 'POST':
        form = RegistroCarta(request.POST, instance =  cartas)
        if form.is_valid():
            form.save()
            form = RegistroCarta()
            return HttpResponseRedirect(reverse('tablaCartas'))
    data = {'form': form}
    return render(request, 'plataformaYugimon/formularioCartas.html', data)

@user_passes_test(lambda u: u.is_superuser)
def eliminarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    cartas.delete()
    return HttpResponseRedirect(reverse('tablaCartas'))

@user_passes_test(lambda u: u.is_superuser)
def tablaCartas(request):
    cartas = Carta.objects.all()
    data = {'cartas': cartas}
    return render(request, 'plataformaYugimon/tablaCartas.html', data)

@user_passes_test(lambda u: u.is_superuser)
def crearBanlist(request):
    form = BanlistForm()
    if request.method == 'POST':
        form = BanlistForm(request.POST)
        if form.is_valid():
            form.save()
            form = BanlistForm()
            return HttpResponseRedirect(reverse('mostrarBanlist'))
    data = {'form': form}
    return render(request, 'plataformaYugimon/crearBanlist.html', data)

#Vistas de publicaciones
class PublicacionCartaView(ListView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/publicacionesCartas.html'
    ordering = ['-fecha']
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.all().prefetch_related('cartas_tengo', 'cartas_quiero').order_by(*self.ordering)

#Vistas de publicaciones
class PublicacionCartaDetail(DetailView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/detallesPublicacionCartas.html'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('cartas_tengo', 'cartas_quiero')

class EscribirPostCarta(CreateView):
    model = Publicacion_intercambio
    form_class = PostForm
    template_name = "plataformaYugimon/escribirPost.html"
    success_url = reverse_lazy('publicacionCarta')

    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EditarPostCarta(UpdateView):
    model = Publicacion_intercambio
    template_name = "plataformaYugimon/editarPost.html"
    
    form_class = PostEditForm
    success_url = reverse_lazy('publicacionCarta')

class EliminarPostCarta(DeleteView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/publicacionesCartas.html'
    success_url = reverse_lazy('publicacionCarta')
    
class ListaCartas(ListView):
    model = Carta
    template_name = 'plataformaYugimon/crearMazo.html'

@login_required
@require_POST
def update_mazo(request):
    carta_id = request.POST.get("carta_id")
    mazo_id = request.POST.get("mazo_id")
    action = request.POST.get("action")

    mazo = Mazo.objects.get(id=mazo_id)
    carta = Carta.objects.get(id=carta_id)

    if action == "agregar":
        Cartas_mazos.objects.get_or_create(id_mazo=mazo, id_carta=carta)

    elif action == "quitar":
        Cartas_mazos.objects.filter(id_mazo=mazo, id_carta=carta).delete()

    return redirect("editar_mazo", mazo_id=mazo_id)

@login_required
def crear_mazo(request):
    if request.method == "POST":
        form = MazoForm(request.POST)
        if form.is_valid():
            mazo = form.save(commit=False)
            mazo.id_usuario = request.user 
            mazo.save()
            return redirect('editar_mazo', mazo_id=mazo.id)
    else:
        form = MazoForm()

    return render(request, "plataformaYugimon/crearMazo.html", {'form':form})

@login_required
def editar_mazo(request, mazo_id):
    mazo = Mazo.objects.get(id=mazo_id)
    cartas = Carta.objects.all()
    cartas_mazo = Cartas_mazos.objects.filter(id_mazo=mazo)

    if request.method == "POST":
        form = MazoForm(request.POST, instance=mazo)
        if form.is_valid():
            form.save()
            return redirect("listarMazos")
    else:
        form = MazoForm(instance=mazo)

    context = {"mazo": mazo, 'form': form, "object_list": cartas, "cartas_mazo": cartas_mazo}

    return render(request, 'plataformaYugimon/editarMazo.html', context)

@login_required
@require_POST
def update_mazo_ajax(request):
    data = json.loads(request.body)

    carta_id = data.get("carta_id")
    mazo_id = data.get("mazo_id")
    action = data.get("action")

    # Obtener mazo
    try:
        mazo = Mazo.objects.get(id=mazo_id)
    except Mazo.DoesNotExist:
        return JsonResponse({"success": False, "error": "Mazo no encontrado."})

    
    if action == "check":
        cartas_qs = Cartas_mazos.objects.filter(id_mazo=mazo)

        conteo = {}
        for entry in cartas_qs:
            cid = entry.id_carta.id
            conteo[cid] = conteo.get(cid, 0) + 1

        total_cartas = cartas_qs.count()

        return JsonResponse({
            "success": True,
            "total": total_cartas,
            "conteo": conteo
        })

    
    if not carta_id:
        return JsonResponse({"success": False, "error": "Falta carta_id."})

    try:
        carta = Carta.objects.get(id=carta_id)
    except Carta.DoesNotExist:
        return JsonResponse({"success": False, "error": "Carta no encontrada."})

    total_cartas = Cartas_mazos.objects.filter(id_mazo=mazo).count()
    copias_carta = Cartas_mazos.objects.filter(id_mazo=mazo, id_carta=carta).count()

    if action == "agregar":

        if total_cartas >= 50:
            return JsonResponse({"success": False, "error": "El mazo ya tiene 50 cartas."})

        if copias_carta >= 3:
            return JsonResponse({"success": False, "error": "Máximo 3 copias por carta."})

        Cartas_mazos.objects.create(id_mazo=mazo, id_carta=carta)

    elif action == "quitar":
        Cartas_mazos.objects.filter(id_mazo=mazo, id_carta=carta).first().delete()

    else:
        return JsonResponse({"success": False, "error": "Acción inválida."})

    cartas_mazo = list(
        Cartas_mazos.objects.filter(id_mazo=mazo)
        .select_related("id_carta")
        .values(
            "id_carta__id",
            "id_carta__nombre",
            "id_carta__ilustracion"
        )
    )

    return JsonResponse({
        "success": True,
        "cartas_mazo": cartas_mazo,
        "total": len(cartas_mazo),
        "copias": copias_carta
    })

class CartaView(ListView):
    model = Carta
    template_name = 'plataformaYugimon/ListaCartas.html'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(nombre__icontains=query)

        edicion_id = self.request.GET.get('edicion')
        if edicion_id:
            queryset = queryset.filter(id_edicion=edicion_id)

        tipo_id = self.request.GET.get('tipo')
        if tipo_id:
            queryset = queryset.filter(id_tipo=tipo_id)

        raza_id = self.request.GET.get('raza')
        if raza_id:
            queryset = queryset.filter(id_raza=raza_id)

        coste = self.request.GET.get('coste')
        if coste:
            queryset = queryset.filter(coste=int(coste))
        
        return queryset.order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ediciones'] = Edicion.objects.all().order_by('nombre')
        context['tipos'] = Tipo.objects.all().order_by('nombre')
        context['razas'] = Raza.objects.all().order_by('nombre')

        
        context['selected_edition'] = self.request.GET.get('edicion', '')
        context['selected_tipo'] = self.request.GET.get('tipo', '')
        context['selected_raza'] = self.request.GET.get('raza', '')
        context['selected_coste'] = self.request.GET.get('coste', '')
        context['selected_query'] = self.request.GET.get('q', '')

        return context

@login_required
def listarMazos(request):
    mazos = Mazo.objects.all().annotate(
        promedio_estrellas=Avg('puntuacionmazo__estrellas') 
    ).order_by('-id')
    
    for mazo in mazos:
        if mazo.promedio_estrellas is not None:
            mazo.puntuacion_promedio = round(mazo.promedio_estrellas, 2)
        else:
            mazo.puntuacion_promedio = '-'
    return render(request, "plataformaYugimon/listarMazos.html", {
        "mazos": mazos
    })

@login_required
def verMazo(request, mazo_id):
    mazo = get_object_or_404(Mazo, id=mazo_id)

    #Genera un promedio de todas las puntuaciones de un mazo y lo retorna
    if request.method == 'POST':
        estrellas = request.POST.get('val')
        
        if estrellas:
            estrellas_num = int(estrellas)
            if 1 <= estrellas_num <= 5:
                PuntuacionMazo.objects.update_or_create(
                    mazo=mazo,
                    usuario=request.user, 
                    defaults={'estrellas': estrellas_num}
                )
                nuevo_promedio = PuntuacionMazo.objects.filter(mazo=mazo).aggregate(Avg('estrellas')).get('estrellas__avg')
                
                if nuevo_promedio is not None:
                    promedio_formateado = round(nuevo_promedio, 2)
                else:
                    promedio_formateado = None

                return JsonResponse({
                    'success': True, 
                    'message': 'Puntuación guardada con éxito.',
                    'promedio_estrellas': promedio_formateado
                })

    #Guarda la cantidad de estrellas seleccionada por el usuario
    puntuacion_usuario = 0
    try:
        voto_existente = PuntuacionMazo.objects.get(mazo=mazo, usuario=request.user)
        puntuacion_usuario = voto_existente.estrellas
    except PuntuacionMazo.DoesNotExist:
        puntuacion_usuario = 0

    cartas = (
        Cartas_mazos.objects
        .filter(id_mazo=mazo)
        .values('id_carta')                     
        .annotate(cantidad=Sum('cantidad'))    
        .annotate(
            nombre=F('id_carta__nombre'),
            ilustracion=F('id_carta__ilustracion')
        )
    )

    total = sum(c['cantidad'] for c in cartas)

    promedio_puntuacion = PuntuacionMazo.objects.filter(mazo=mazo).aggregate(Avg('estrellas'))
    promedio_estrellas = promedio_puntuacion.get('estrellas__avg')

    if promedio_estrellas is not None:
        promedio_formateado = round(promedio_estrellas, 2) 
    else:
        promedio_formateado = None

    sort_order = request.GET.get('sort', '-fecha')
    allowed_sorts = {
        '-fecha': '-fecha',  
        'fecha': 'fecha',
    }
    sort_field = allowed_sorts.get(sort_order, '-fecha')
    comentarios_ordenados = mazo.comentarios.all().order_by(sort_field)

    comentarios_por_pagina = 3
    paginator = Paginator(comentarios_ordenados, comentarios_por_pagina)
    page_number = request.GET.get('page')

    try:
        comentarios_paginados = paginator.get_page(page_number)
    except Exception:
        comentarios_paginados = paginator.get_page(1)

    return render(request, "plataformaYugimon/verMazo.html", {
        "mazo": mazo,
        "cartas": cartas,
        "total": total,
        "comentarios_ordenados": comentarios_ordenados,
        "comentarios_paginados": comentarios_paginados,
        "current_sort": sort_order,
        "promedio_estrellas": promedio_formateado,
        "puntuacion_usuario": puntuacion_usuario,
    })

@login_required
def eliminarMazo(request, mazo_id):
    mazo = get_object_or_404(Mazo, id=mazo_id)

    if request.method == "POST":
        mazo.delete()
        return redirect("listarMazos")

    return render(request, "plataformaYugimon/eliminarMazo.html", {
        "mazo": mazo
    })

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CrearBanlist(CreateView):
    model = Cartas_Banlist
    form_class = BanlistForm
    template_name = "plataformaYugimon/agregarCartasBanlist.html"
    success_url = reverse_lazy('mostrarBanlist')

    def form_valid(self, form):
        carta_seleccionada = form.cleaned_data['carta']
        form.instance.edicion = carta_seleccionada.id_edicion
        return super().form_valid(form)

class MostrarCartasBanlistView(TemplateView):
    template_name = 'plataformaYugimon/banlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        todas_las_entradas = Cartas_Banlist.objects.all().select_related('edicion', 'carta', 'restriccion')
        
        banlist_agrupada = {}
        
        for entrada in todas_las_entradas:
            nombre_edicion = entrada.edicion.nombre
            nombre_restriccion = entrada.restriccion.nombre
            
            if nombre_edicion not in banlist_agrupada:
                banlist_agrupada[nombre_edicion] = {}
            
            if nombre_restriccion not in banlist_agrupada[nombre_edicion]:
                banlist_agrupada[nombre_edicion][nombre_restriccion] = []
            
            banlist_agrupada[nombre_edicion][nombre_restriccion].append(entrada)
            
        context['banlist_por_edicion'] = banlist_agrupada

        return context

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class editarBanlist(DeleteView):
    model = Cartas_Banlist
    template_name = 'plataformaYugimon/banlist.html'
    success_url = reverse_lazy('mostrarBanlist')


class PublicacionesMazosListView(ListView):
    model = Publicacion_venta
    template_name = 'plataformaYugimon/publicacionesMazos.html' 
    context_object_name = 'publicaciones'  
    ordering = ['-fecha_publicacion']
    paginate_by = 5

    def get_queryset(self):
        return Publicacion_venta.objects.select_related('id_mazo').all().order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        publicaciones = context['publicaciones']

        for pub in publicaciones:
            pub.cartas = Cartas_mazos.objects.filter(id_mazo=pub.id_mazo).select_related('id_carta')

        return context

class PublicacionVentaMazoView(DetailView):
    model = Publicacion_venta
    template_name = 'plataformaYugimon/detallesPublicacionVentaMazos.html'

    context_object_name = 'publicacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        publicacion = self.object
        mazo = publicacion.id_mazo
        promedio_puntuacion = PuntuacionMazo.objects.filter(mazo=mazo).aggregate(Avg('estrellas'))
        promedio_estrellas = promedio_puntuacion.get('estrellas__avg')

        if promedio_estrellas is not None:
            puntuacion_promedio = round(promedio_estrellas, 2)
        else:
            puntuacion_promedio = '-'

        cartas_mazo = Cartas_mazos.objects.filter(id_mazo=mazo).select_related('id_carta')

        context['mazo'] = mazo
        context['cartas_mazo'] = cartas_mazo
        context['puntuacion_promedio'] = puntuacion_promedio

        return context

class EscribirPostVentaMazo(CreateView):
    model = Publicacion_venta
    form_class = PostVentaMazoForm
    template_name = "plataformaYugimon/escribirPostVentaMazos.html"
    success_url = reverse_lazy('listarPublicacionesMazos')

    def form_valid(self, form):
        form.instance.id_usuario = self.request.user
        return super().form_valid(form)

class EliminarVentaMazos(DeleteView):
    model = Publicacion_venta
    template_name = 'plataformaYugimon/publicacionesMazos.html'
    success_url = reverse_lazy('listarPublicacionesMazos')

class EditarPostVentaMazos(UpdateView):
    model = Publicacion_venta
    template_name = "plataformaYugimon/editarPostVentaMazos.html"
    
    form_class = PostVentaMazoForm
    success_url = reverse_lazy('listarPublicacionesMazos')

class CrearComentario(CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'plataformaYugimon/crearComentario.html'

    def form_valid(self, form):
        form.instance.mazo_id = self.kwargs['pk']
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('verMazo', kwargs={'mazo_id': self.kwargs['pk']})
    
class EditarComentario(UpdateView):
    model = Comentario
    template_name = "plataformaYugimon/editarComentario.html"
    form_class = ComentarioForm
    def get_success_url(self):
        mazo_id = self.object.mazo.id
        return reverse_lazy('verMazo', kwargs={'mazo_id': mazo_id})

class EliminarComentario(DeleteView):
    model = Comentario
    template_name = 'plataformaYugimon/verMazo.html'
    def get_success_url(self):
        mazo_id = self.object.mazo.id
        return reverse_lazy('verMazo', kwargs={'mazo_id': mazo_id})


class CrearRespuestaComentario(CreateView):
    model = RespuestaComentario
    form_class = RespuestaComentarioForm
    template_name = 'plataformaYugimon/crearComentario.html'

    def form_valid(self, form):
        comentario = get_object_or_404(Comentario, pk=self.kwargs['pk'])
        form.instance.comentario = comentario
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        comentario = get_object_or_404(Comentario, pk=self.kwargs['pk'])
        mazo_id = comentario.mazo.id
        return reverse_lazy('verMazo', kwargs={'mazo_id': mazo_id})
    
class EditarRespuestaComentario(UpdateView):
    model = RespuestaComentario
    template_name = "plataformaYugimon/editarComentario.html"
    form_class = RespuestaComentarioForm
    def get_success_url(self):
        mazo_id = self.object.comentario.mazo.id 
        return reverse_lazy('verMazo', kwargs={'mazo_id': mazo_id})

class EliminarRespuestaComentario(DeleteView):
    model = RespuestaComentario
    template_name = 'plataformaYugimon/verMazo.html'
    def get_success_url(self):
        mazo_id = self.object.comentario.mazo.id 
        return reverse_lazy('verMazo', kwargs={'mazo_id': mazo_id})
    

@login_required
def misMazos(request):
    usuario_logueado = request.user
    mazos = Mazo.objects.filter(id_usuario=usuario_logueado).annotate(
        promedio_estrellas=Avg('puntuacionmazo__estrellas') 
    ).order_by('-id')
    
    for mazo in mazos:
        if mazo.promedio_estrellas is not None:
            mazo.puntuacion_promedio = round(mazo.promedio_estrellas, 2)
        else:
            mazo.puntuacion_promedio = '-'
    return render(request, "plataformaYugimon/listarMazos.html", {
        "mazos": mazos
    })

class ComparadorMazo(ListView):
    model = Cartas_mazos
    template_name = 'plataformaYugimon/comparadorMazos.html' 
    context_object_name = 'comparaciones'

    def get_queryset(self):
        return Mazo.objects.select_related('id_usuario').all()

@login_required
def obtener_datos_mazo(request, mazo_id):
    try:
        mazo = Mazo.objects.get(id=mazo_id)
    except Mazo.DoesNotExist:
        return JsonResponse({"error": "Mazo no encontrado."}, status=404)

    # Obtener el listado de cartas con su cantidad y datos
    cartas_mazo_qs = (
        Cartas_mazos.objects
        .filter(id_mazo=mazo)
        .values('id_carta')
        .annotate(
            cantidad=Count('id_carta'),
            nombre=F('id_carta__nombre'),
            habilidad=F('id_carta__habilidad'),
            raza=F('id_carta__id_raza__nombre'),
            tipo=F('id_carta__id_tipo__nombre'),
            edicion=F('id_carta__id_edicion__nombre'),
            ilustracion=F('id_carta__ilustracion'),
            coste=F('id_carta__coste'), 
            fuerza=F('id_carta__fuerza'), 
        )
        .order_by('nombre')
    )

    # Calcular estadísticas del mazo
    stats_agregadas = (
        Cartas_mazos.objects
        .filter(id_mazo=mazo)
        .aggregate(
            coste_total=Sum('id_carta__coste'),
            fuerza_total=Sum('id_carta__fuerza'),
            coste_promedio=Avg('id_carta__coste'),
            fuerza_promedio=Avg('id_carta__fuerza'),
            total_cartas=Count('id_carta')
        )
    )

    # Calcular el promedio de estrellas del mazo
    promedio_puntuacion = PuntuacionMazo.objects.filter(mazo=mazo).aggregate(Avg('estrellas'))
    promedio_estrellas = promedio_puntuacion.get('estrellas__avg')
    
    # Formatear el promedio de estrellas
    puntuacion_formateada = round(promedio_estrellas, 2) if promedio_estrellas is not None else 0

    # Prepara los datos de las cartas para el JSON
    cartas_list = list(cartas_mazo_qs)

    # Prepara las estadísticas formateadas
    stats_formateadas = {
        "ID": mazo.id,
        "Nombre": mazo.nombre,
        "Total de Cartas": stats_agregadas.get('total_cartas', 0),
        "Coste Total": stats_agregadas.get('coste_total', 0) or 0,
        "Fuerza Total": stats_agregadas.get('fuerza_total', 0) or 0,
        "Coste Promedio": round(stats_agregadas.get('coste_promedio', 0) or 0, 2),
        "Fuerza Promedio": round(stats_agregadas.get('fuerza_promedio', 0) or 0, 2),
        "Puntuación Promedio": puntuacion_formateada,
    }

    return JsonResponse({
        "stats": stats_formateadas,
        "cartas": cartas_list
    })



def me_interesa(request, pk):
    publicacion = get_object_or_404(Publicacion_venta, pk=pk)

    Notificacion.objects.create(
        receptor = publicacion.id_usuario,
        emisor = request.user,
        mensaje = f"A {request.user.username} Le interesa tu publicación: {publicacion.titulo} \n Contáctate a su correo: {request.user.email}.",
        url = f"/publicacionVentaMazos/{pk}/"
    )
    return redirect("detallesPublicacionVentaMazos", pk=pk)



@login_required
def leer_notificacion(request, pk):
    notif = get_object_or_404(Notificacion, pk=pk, receptor=request.user)
    notif.leida = True
    notif.save()
    
    # si la notificación tiene URL, redirige a ella
    if notif.url:
        return redirect(notif.url)

    # si no, vuelve a donde estaba
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def listar_todas_notificaciones(request):
    notificaciones = Notificacion.objects.filter(
        receptor=request.user
    ).order_by("-fecha")

    return render(request, "plataformaYugimon/notificaciones/todas.html", {
        "notificaciones": notificaciones
    })

from django.shortcuts import get_object_or_404, redirect
from .models import Publicacion_intercambio, Notificacion

def me_interesa_intercambio(request, pk):
    publicacion = get_object_or_404(Publicacion_intercambio, pk=pk)

    if request.user == publicacion.autor:
        return redirect(publicacion.get_absolute_url())

    # Crear notificación
    Notificacion.objects.create(
        receptor=publicacion.autor,
        emisor=request.user,
        mensaje=f"{request.user.username} quiere intercambiar contigo., publicacion: {publicacion.titulo} \n Contáctate a su correo: {request.user.email}.",
        url=publicacion.get_absolute_url()
    )

    return redirect(publicacion.get_absolute_url())

def listar_todas_notificaciones(request):
    notificaciones = Notificacion.objects.filter(
        receptor=request.user
    ).order_by('-fecha')

    return render(request, "plataformaYugimon/notificaciones/todas.html", {
        "notificaciones": notificaciones
    })



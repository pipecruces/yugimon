from django.shortcuts import render, redirect, get_object_or_404
from plataformaYugimon.models import *
from plataformaYugimon.forms import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.views.decorators.http import  require_POST
from django.http import JsonResponse
import json
from django.db.models import Sum, F
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

    def get_context_data(self, *args, **kwargs):
        categoria_menu = CategoriaPost.objects.all()
        context = super(PublicacionCartaView, self).get_context_data(*args, **kwargs)
        context['categoria_menu'] = categoria_menu
        
        context['object_list'] = self.model.objects.all().prefetch_related('cartas_tengo', 'cartas_quiero').order_by(*self.ordering)
        return context

#Filtrar publicaciones por categoria
@login_required
def CategoriaView(request, categorias):
    categoria_posts = Publicacion_intercambio.objects.filter(categoria__nombre=categorias.replace('-', ' '))
    return render(request, 'plataformaYugimon/categorias.html', {'categorias':categorias.title().replace('-', ' '), 'categoria_posts':categoria_posts})

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

def crear_mazo(request):
    if request.method == "POST":
        form = MazoForm(request.POST)
        if form.is_valid():
            mazo = form.save(commit=False)
            mazo.id_usuario = request.user   # 👈 asignar usuario automáticamente
            mazo.save()
            return redirect('editar_mazo', mazo_id=mazo.id)
    else:
        form = MazoForm()

    return render(request, "plataformaYugimon/crearmazo.html", {'form':form})

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

def listarMazos(request):
    mazos = Mazo.objects.all().order_by('-id')
    return render(request, "plataformaYugimon/listarMazos.html", {
        "mazos": mazos
    })

def verMazo(request, mazo_id):
    mazo = Mazo.objects.get(id=mazo_id)

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

    return render(request, "plataformaYugimon/verMazo.html", {
        "mazo": mazo,
        "cartas": cartas,
        "total": total,
    })
def eliminarMazo(request, mazo_id):
    mazo = get_object_or_404(Mazo, id=mazo_id)

    if request.method == "POST":
        mazo.delete()
        return redirect("listarMazos")

    return render(request, "plataformaYugimon/eliminarMazo.html", {
        "mazo": mazo
    })

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

class PublicacionesMazosListView(ListView):
    model = Publicacion_venta
    template_name = 'plataformaYugimon/publicacionesMazos.html' 
    context_object_name = 'publicaciones'  
    ordering = ['-fecha_publicacion']

    def get_queryset(self):
        return Publicacion_venta.objects.select_related('id_mazo').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        publicaciones = context['publicaciones']

        for pub in publicaciones:
            pub.cartas = Cartas_mazos.objects.filter(id_mazo=pub.id_mazo).select_related('id_carta')

        return context

@login_required
def CategoriaView(request, categorias):
    categoria_posts = Publicacion_intercambio.objects.filter(categoria__nombre=categorias.replace('-', ' '))
    return render(request, 'plataformaYugimon/categorias.html', {'categorias':categorias.title().replace('-', ' '), 'categoria_posts':categoria_posts})

class PublicacionVentaMazoView(DetailView):
    model = Publicacion_venta
    template_name = 'plataformaYugimon/detallesPublicacionVentaMazos.html'

    context_object_name = 'publicacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        publicacion = self.object
        mazo = publicacion.id_mazo

        cartas_mazo = Cartas_mazos.objects.filter(id_mazo=mazo).select_related('id_carta')

        context['mazo'] = mazo
        context['cartas_mazo'] = cartas_mazo

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
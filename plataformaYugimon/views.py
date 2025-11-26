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
            form.save()
            form = RegistroCarta()
            return HttpResponseRedirect(reverse('tablaCartas')) #NO SÉ SI PONER RESPONSE
    data = {'form': form}
    return render(request, 'plataformaYugimon/formularioCartas.html', data)

@user_passes_test(lambda u: u.is_superuser)
def editarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    form = RegistroCarta(instance = cartas)
    if request.method == 'POST':
        form = RegistroCarta(request.POST, instance =  cartas)
        if form.is_valid():
            form.save()
            form = RegistroCarta()
            return HttpResponseRedirect(reverse('tablaCartas'))#ESTOS REVERSE HAY QUE CAMBIAR DESPUÉS
    data = {'form': form}
    return render(request, 'plataformaYugimon/formularioCartas.html', data)

@user_passes_test(lambda u: u.is_superuser)
def eliminarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    cartas.delete()
    return HttpResponseRedirect(reverse('tablaCartas')) #REVISAR REVERSE

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
        # Optimizacion: Cargar cartas relacionadas en la lista principal
        context['object_list'] = self.model.objects.all().prefetch_related('cartas_tengo', 'cartas_quiero').order_by(*self.ordering)
        return context


#Filtrar publicaciones por categoria
@login_required
def CategoriaView(request, categorias):
    nombre_categoria = categorias.replace('-', ' ')
    # CORRECCIÓN 2: Añadir prefetch_related para cargar cartas relacionadas
    categoria_posts = Publicacion_intercambio.objects.filter(
        categoria=nombre_categoria
    ).prefetch_related('cartas_tengo', 'cartas_quiero') # <-- CORRECCIÓN APLICADA

    return render(request, 'plataformaYugimon/categorias.html', {
        'categorias': nombre_categoria.title(), 
        'categoria_posts':categoria_posts
    })

#Vistas de publicaciones
class PublicacionCartaDetail(DetailView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/detallesPublicacionCartas.html'
    # Sugerencia: Asegurar la carga de cartas en el detalle
    def get_queryset(self):
        return super().get_queryset().prefetch_related('cartas_tengo', 'cartas_quiero')


class EscribirPostCarta(CreateView):
    model = Publicacion_intercambio
    form_class = PostForm
    template_name = "plataformaYugimon/escribirPost.html"
    success_url = reverse_lazy('publicacionCarta')

    #Deja al usuario autenticado como autor por defecto
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EditarPostCarta(UpdateView):
    model = Publicacion_intercambio
    template_name = "plataformaYugimon/editarPost.html"
    # fields = ['titulo', 'contenido']
    form_class = PostEditForm
    success_url = reverse_lazy('publicacionCarta')

class EliminarPostCarta(DeleteView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/publicacionesCartas.html'
    success_url = reverse_lazy('publicacionCarta')
    
class CreacionMazo(CreateView):
    model = Mazo
    form_class = MazoForm
    template_name = "plataformaYugimon/crearMazo.html"
    success_url = reverse_lazy('crearMazo')

    #Deja al usuario autenticado como autor por defecto
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

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
            mazo = form.save()
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

    # Si la acción es solo CHECK no necesitamos carta
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

    # Validamos que llegue una carta si NO es "check"
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
    cartas = Cartas_mazos.objects.filter(id_mazo=mazo)

    total = sum(c.cantidad for c in cartas)

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

class MostrarCartasBanlistView(TemplateView):
    template_name = 'plataformaYugimon/banlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Obtener TODAS las entradas, incluyendo las ediciones, cartas y restricciones.
        # Esto reduce el número de consultas a la base de datos (SELECTs).
        todas_las_entradas = Cartas_Banlist.objects.all().select_related('edicion', 'carta', 'restriccion')
        
        # 2. Inicializar la estructura anidada de agrupación
        banlist_agrupada = {}
        
        # 3. Agrupar primero por Edición y luego por Restricción
        for entrada in todas_las_entradas:
            nombre_edicion = entrada.edicion.nombre
            nombre_restriccion = entrada.restriccion.nombre
            
            # Agrupación por Edición
            if nombre_edicion not in banlist_agrupada:
                # Inicializa la edición como un diccionario vacío (para almacenar restricciones)
                banlist_agrupada[nombre_edicion] = {}
            
            # Agrupación por Restricción (dentro de la Edición)
            if nombre_restriccion not in banlist_agrupada[nombre_edicion]:
                # Inicializa la restricción como una lista (para almacenar las cartas)
                banlist_agrupada[nombre_edicion][nombre_restriccion] = []
            
            # Agrega la entrada de banlist (la carta) a la lista de la restricción correspondiente
            banlist_agrupada[nombre_edicion][nombre_restriccion].append(entrada)
            
        # 4. Añadir la estructura agrupada al contexto
        context['banlist_por_edicion'] = banlist_agrupada

        return context

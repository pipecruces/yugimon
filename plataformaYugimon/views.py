from django.shortcuts import render, redirect
from plataformaYugimon.models import *
from plataformaYugimon.forms import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
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
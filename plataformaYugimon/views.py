from django.shortcuts import render, redirect
from plataformaYugimon.models import *
from plataformaYugimon.forms import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
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

def mostrarBanlist(request):
    ediciones = [
        {
            'id': '1',
            'nombre': 'Edición 1: Nombre de la edicion',
            'prohibidas':[
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/2.-%20Dragon/Groostlang-small.webp',
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/1.-%20El%20Reto/Talismanes/Od%C3%ADn%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/5.-%20Esp%C3%ADritu%20de%20Drag%C3%B3n/Armas/Yoroi-small.webp'
                }
            ],
            'unicas': [
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/1.-%20El%20Reto/Talismanes/Od%C3%ADn%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/2.-%20Dragon/Quetzalc%C3%B3atl-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/1.-%20Caballero/Caballero%20Negro-small.webp'
                }
            ],
            'limitadas': [
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/1.-%20El%20Reto/Talismanes/Zeus%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/2.-%20Mundo%20G%C3%B3tico/Talismanes/Lucha%20de%20Golems-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/4.-%20Cazador/Niamh-small.webp'
                }
            ]
        },
        {
            'id': '2',
            'nombre': 'Edición 2: Nombre de la edicion',
            'prohibidas':[
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/4.-%20Cazador/Exorcista-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/2.-%20Mundo%20G%C3%B3tico/Talismanes/Stribog%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/7.-%20Bestia/Trauko%20(Arte%20Alternativo)-small.webp'
                }
            ],
            'unicas': [
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/2.-%20Mundo%20G%C3%B3tico/Oros/Manada%20Mort%C3%ADfera%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/3.-%20La%20Ira%20del%20Nahual/T%C3%B3tems/T%C3%B3tem%20de%20Jaguar%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/7.-%20Bestia/Sisiutl%20(Arte%20Alternativo)-small.webp'
                }
            ],
            'limitadas': [
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/5.-%20Lic%C3%A1ntropo/Lupo%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/3.-%20La%20Ira%20del%20Nahual/Oros/Bestias%20Furiosas%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/3.-%20La%20Ira%20del%20Nahual/T%C3%B3tems/T%C3%B3tem%20del%20%C3%81guila-small.webp'
                }
            ]
        },
        {
            'id': '3',
            'nombre': 'Edición 3: Nombre de la edicion',
            'prohibidas':[
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/7.-%20Bestia/Grifo-small.webp'  
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/9.-%20Guerrero/Shuar-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/11.-%20B%C3%A1rbaro/Bjorn%20Ragnarsson-small.webp'
                }
            ],
            'unicas': [
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/3.-%20La%20Ira%20del%20Nahual/T%C3%B3tems/T%C3%B3tem%20de%20Serpiente%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/4.-%20Ragnarok/Oros/Horda%20B%C3%A1rbara%20(Arte%20Alternativo)-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/10.-%20Abominaci%C3%B3n/Brokk-small.webp'
                }
            ],
            'limitadas': [
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/7.-%20Bestia/Pihuchen%20(Arte%20Alternativo)-small.webp',
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Soporte/5.-%20Esp%C3%ADritu%20de%20Drag%C3%B3n/Armas/Kabuto-small.webp'
                },
                {
                    'image': 'https://mazosyleyendas.b-cdn.net/PE%20COMP/Razas/14.-%20Campe%C3%B3n/Guan%20Yu%20(Arte%20Alternativo)-small.webp'
                }
            ]
        }
    ]
    return render(request, 'plataformaYugimon/banlist.html', {'ediciones': ediciones})

#Vistas de publicaciones
class PublicacionCartaView(ListView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/publicacionesCartas.html'
    ordering = ['-fecha']

    def get_context_data(self, *args, **kwargs):
        categoria_menu = CategoriaPost.objects.all()
        context = super(PublicacionCartaView, self).get_context_data(*args, **kwargs)
        context['categoria_menu'] = categoria_menu
        return context


#Filtrar publicaciones por categoria
@login_required
def CategoriaView(request, categorias):
    categoria_posts = Publicacion_intercambio.objects.filter(categoria=categorias.replace('-', ' '))
    return render(request, 'plataformaYugimon/categorias.html', {'categorias':categorias.title().replace('-', ' '), 'categoria_posts':categoria_posts})

#Vistas de publicaciones
class PublicacionCartaDetail(DetailView):
    model = Publicacion_intercambio
    template_name = 'plataformaYugimon/detallesPublicacionCartas.html'

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
    

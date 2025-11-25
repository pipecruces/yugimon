from django.shortcuts import render, redirect, get_object_or_404
from plataformaYugimon.models import *
from plataformaYugimon.forms import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
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
    categoria_posts = Publicacion_intercambio.objects.filter(categoria__nombre=categorias.replace('-', ' '))
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
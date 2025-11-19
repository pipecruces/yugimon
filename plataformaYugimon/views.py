
from django.shortcuts import render, redirect, get_list_or_404
from plataformaYugimon.models import Carta, Mazo, Cartas_mazos
from plataformaYugimon.forms import RegistroCarta, RegistroUsuario
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
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

@login_required
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

@login_required
def eliminarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    cartas.delete()
    return HttpResponseRedirect(reverse('tablaCartas')) #REVISAR REVERSE

@login_required
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

# Create your views here.
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

@login_required
def crear_mazo(request, id_mazo):
    mazo = get_list_or_404(Mazo, id=id_mazo, usuario=request.user)
    cartas_en_mazo_query = Cartas_mazos.objects.filter(mazo=mazo).values('id_carta', 'cantidad')
    cartas_en_mazo_dict = {}
    for item in cartas_en_mazo_query:
        id_carta = item['id_carta']
        cantidad = item['cantidad']
        
        cartas_en_mazo_dict[id_carta] = cantidad
    context = {
        'cartas_en_mazo_dict': cartas_en_mazo_dict,
    }
    return render(request, 'plataformaYugimon/creacionMazo.html', context)

@login_required
def agregar_carta_a_mazo(request, id_mazo, id_carta):
    if request.method == 'POST':
        mazo = get_list_or_404(Mazo, id=id_mazo, usuario=request.user)
        carta = get_list_or_404(Carta, id=id_carta)
        relacion, created = Cartas_mazos.objects.get_or_create(
            mazo=mazo,
            carta=carta,
            defaults={'cantidad': 1}
        )
        if not created:
            if relacion.cantidad < 3: 
                 relacion.cantidad += 1
                 relacion.save()
    return redirect('plataformaYugimon/creacionMazo.html', id_mazo=id_mazo)

@login_required
def quitar_carta_de_mazo(request, id_mazo, id_carta):
    if request.method == 'POST':
        mazo = get_list_or_404(Mazo, id=id_mazo, usuario=request.user)
        carta = get_list_or_404(Carta, id=id_carta)
        relacion = get_list_or_404(Cartas_mazos, mazo=mazo, carta=carta)
        if relacion.cantidad > 1:
            relacion.cantidad -= 1
            relacion.save()
        else:
            relacion.delete()
    return redirect('plataformaYugimon/creacionMazo.html', id_mazo=id_mazo)
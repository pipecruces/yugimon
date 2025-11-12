
from django.shortcuts import render
from plataformaYugimon.models import Carta
from plataformaYugimon.forms import RegistroCarta
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.


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

def eliminarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    cartas.delete()
    return HttpResponseRedirect(reverse('tablaCartas')) #REVISAR REVERSE

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

from django.shortcuts import render, redirect
from plataformaYugimon.forms import RegistroUsuario
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import request

# Create your views here.
def SignUpView(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroUsuario()
        
    data = {'form': form}
    return render(request, 'registration/signup.html', data)


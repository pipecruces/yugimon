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
            return HttpResponseRedirect(reverse('ingresarCarta')) #NO SÉ SI PONER RESPONSE
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
            return HttpResponseRedirect(reverse('editarCarta'))#ESTOS REVERSE HAY QUE CAMBIAR DESPUÉS
    data = {'form': form}
    return render(request, 'plataformaYugimon/formularioCartas.html', data)

def eliminarCarta(request, id):
    cartas = Carta.objects.get(id = id)
    cartas.delete()
    return HttpResponseRedirect(reverse('editarCarta')) #REVISAR REVERSE
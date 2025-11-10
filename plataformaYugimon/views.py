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
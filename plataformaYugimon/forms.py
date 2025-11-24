from django import forms
from plataformaYugimon.views import Carta
from django.core import validators

# class RegistroUsuario(forms.Form):
#     nombre = forms.CharField(max_length=50)
#     correo = forms.CharField(max_length=50)
#     contraseña = forms.CharField(max_length=200)

# class RegistroUsuario(forms.ModelForm):
#     class Meta:
#         model = Usuario
#         fields = '__all__'
#     nombre = forms.CharField(validators=[validators.MinLengthValidator(3), validators.MaxLengthValidator(30)])

class RegistroCarta(forms.Form):
    nombre = forms.CharField(max_length=50)
    habilidad = forms.CharField(max_length=50)
    fuerza = forms.IntegerField()
    coste = forms.IntegerField()
    id_raza = forms.IntegerField()
    ilustracion = forms.CharField(max_length=200)
    edicion = forms.IntegerField()
    id_tipo = forms.IntegerField()
    id_usuario = forms.IntegerField()

class RegistroCarta(forms.ModelForm):
    class Meta:
        model = Carta
        fields = '__all__'

class RegistroMazo(forms.Form):
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=200)
    nota_promedio = forms.FloatField()
    id_estado = forms.IntegerField()


class FormCartaBanlist(forms.Form):
    nombre = forms.CharField(max_length=50)
    habilidad = forms.CharField(max_length=50)
    fureza = forms.CharField(max_length=50)
    coste = forms.CharField(max_length=50)
    ilustracion = forms.CharField(max_length=50)
    edicion = forms.CharField(max_length=50)
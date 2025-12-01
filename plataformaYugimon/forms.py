from django import forms
from plataformaYugimon.views import Carta 
from .models import Publicacion_intercambio, CategoriaPost, Usuario, Cartas_Banlist, Mazo, Comentario, RespuestaComentario, Publicacion_venta
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from datetime import date

#Para que deje crear usuarios con correo
class RegistroUsuario(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)

class EditarUsuario(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100 ,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('email', 'username')

class PasswordChangedForm(PasswordChangeForm):
    old_password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('old_password', 'new_password1', 'new_password2')

class RegistroCarta(forms.ModelForm):
    class Meta:
        model = Carta
        exclude = ['id_usuario']  

class RegistroMazo(forms.Form):
    nombre = forms.CharField(max_length=50)
    descripcion = forms.CharField(max_length=200)
    nota_promedio = forms.FloatField()
    id_estado = forms.IntegerField()

class PostForm(forms.ModelForm):
    class Meta:
        model = Publicacion_intercambio
        fields = ('titulo', 'contenido', 'categoria', 'cartas_tengo', 'cartas_quiero')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'cartas_tengo': forms.SelectMultiple(attrs={'class':'form-control'}),
            'cartas_quiero': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

    def init(self, args, **kwargs):
        super(PostForm, self).init(args, **kwargs)
        self.fields['categoria'].widget.choices = CategoriaPost.objects.all().values_list('nombre', 'nombre')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Publicacion_intercambio
        fields = ('titulo', 'contenido', 'categoria', 'cartas_tengo', 'cartas_quiero')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'cartas_tengo': forms.SelectMultiple(attrs={'class':'form-control'}),
            'cartas_quiero': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

    def init(self, args, **kwargs):
        super(PostEditForm, self).init(args, **kwargs)
        self.fields['categoria'].widget.choices = CategoriaPost.objects.all().values_list('nombre', 'nombre')

class MazoForm(forms.ModelForm):
    class Meta:
        model = Mazo
        fields = ('nombre','descripcion','id_estado')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'id_estado': forms.Select(attrs={'class':'form-control'}),
        }

class BanlistForm(forms.ModelForm):
    class Meta:
        model = Cartas_Banlist
        fields = ('carta', 'restriccion')
        widgets = {
            'carta': forms.Select(attrs={'class':'form-control'}),
            'restriccion': forms.Select(attrs={'class':'form-control'}),
        }

class EditBanlistForm(forms.ModelForm):
    class Meta:
        model = Cartas_Banlist
        fields = ('carta', 'restriccion')
        widgets = {
            'carta': forms.Select(attrs={'class':'form-control'}),
            'restriccion': forms.Select(attrs={'class':'form-control'}),}
        
class PostVentaMazoForm(forms.ModelForm):
    class Meta:
        model = Publicacion_venta
        fields = ('titulo', 'descripcion', 'categoria', 'id_mazo',)
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'id_mazo': forms.Select(attrs={'class': 'form-control'}),
        }

    def init(self, args, **kwargs):
        super(PostVentaMazoForm, self).init(args, **kwargs)
        self.fields['categoria'].widget.choices = CategoriaPost.objects.all().values_list('nombre', 'nombre')

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('contenido',)
        widgets = {
            'contenido': forms.Textarea(attrs={'class':'form-control'})
            }
        
class RespuestaComentarioForm(forms.ModelForm):
    class Meta:
        model = RespuestaComentario
        fields = ('contenido',)
        widgets = {
            'contenido': forms.Textarea(attrs={'class':'form-control'})
            }

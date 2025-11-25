from django import forms
from plataformaYugimon.views import Carta
from .models import Publicacion_intercambio, CategoriaPost, Usuario, Mazo
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

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

#Para darle formato a las publicaciones
class PostForm(forms.ModelForm):
    class Meta:
        model = Publicacion_intercambio
        fields = ('titulo', 'contenido', 'categoria', 'resumen', 'cartas_tengo', 'cartas_quiero')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'cartas_tengo': forms.SelectMultiple(attrs={'class':'form-control'}),
            'cartas_quiero': forms.SelectMultiple(attrs={'class':'form-control'}),
        }
    def init(self, args, **kwargs):
        super(PostForm, self).init(args, **kwargs)
        self.fields['categoria'].widget.choices = CategoriaPost.objects.all().values_list('nombre', 'nombre')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Publicacion_intercambio
        fields = ('titulo', 'contenido', 'categoria', 'resumen',  'cartas_tengo', 'cartas_quiero')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'cartas_tengo': forms.SelectMultiple(attrs={'class':'form-control'}),
            'cartas_quiero': forms.SelectMultiple(attrs={'class':'form-control'}),
        }
    def init(self, args, **kwargs):
        super(PostEditForm, self).init(args, **kwargs)
        self.fields['categoria'].widget.choices = CategoriaPost.objects.all().values_list('nombre', 'nombre')

class MazoForm(forms.ModelForm):
    class Meta:
        model = Mazo
        fields = ['nombre','descripcion','nota_promedio','id_estado']

    
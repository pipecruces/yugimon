from django.db import models

#Usar email para iniciar sesion
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Edicion(models.Model):
    nombre = models.CharField(max_length=50)

class Tipo(models.Model):
    nombre = models.CharField(max_length=50)

class Estado(models.Model):
    nombre = models.CharField(max_length=50)

class Raza(models.Model):
    nombre = models.CharField(max_length=50)

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

class Mazo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    nota_promedio = models.FloatField()
    id_estado = models.ForeignKey(Estado, on_delete = models.CASCADE)

#Usar email para iniciar sesion
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    id_rol = models.ForeignKey(Rol, on_delete = models.CASCADE, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email

# class Usuario(models.Model):
#     nombre = models.CharField(max_length=50)
#     correo = models.CharField(max_length=50)
#     contraseña = models.CharField(max_length=200)
#     id_rol = models.ForeignKey(Rol, on_delete = models.CASCADE)

class Publicacion_venta(models.Model):
    descripcion = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

class Comentario(models.Model):
    descripcion = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

class Usuario_notas(models.Model):
    nota_promedio = models.FloatField()
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

class Publicacion_intercambio(models.Model):
    descripcion = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

class Carta(models.Model):
    nombre = models.CharField(max_length=50)
    habilidad = models.CharField(max_length=50)
    fuerza = models.IntegerField()
    coste = models.IntegerField()
    id_raza = models.ForeignKey(Raza, on_delete = models.CASCADE)
    ilustracion = models.CharField(max_length=200)
    id_edicion = models.ForeignKey(Edicion, on_delete = models.CASCADE)
    id_tipo = models.ForeignKey(Tipo, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

class Cartas_publicacion_intercambio(models.Model):
    id_publicacion_intercambio = models.ForeignKey(Publicacion_intercambio, on_delete = models.CASCADE)
    id_carta = models.ForeignKey(Carta, on_delete = models.CASCADE)

class Cartas_mazos(models.Model):
    id_carta = models.ForeignKey(Carta, on_delete = models.CASCADE)
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE)

class Banlist(models.Model):
    fecha_edicion = models.DateField()
    descripcion = models.CharField(max_length=200)

class Cartas_banlist(models.Model):
    id_carta = models.ForeignKey(Carta, on_delete = models.CASCADE)
    id_banlist = models.ForeignKey(Banlist, on_delete = models.CASCADE)

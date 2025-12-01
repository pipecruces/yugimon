from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator

#Usar email para iniciar sesion
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Edicion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre #para que en los formularios aparezca el nombre y no 'Object_Class_#'
    
class Restriccion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Tipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Tipo_Restriccion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Raza(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class CategoriaPost(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('publicacionCartas')


#Usar email para iniciar sesion
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    id_rol = models.ForeignKey(Rol, on_delete = models.CASCADE, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.username

class Mazo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    id_estado = models.ForeignKey(Estado, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

    def __str__(self):
        return self.nombre
    
class PuntuacionMazo(models.Model):
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)
    estrellas = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]                                
    )
    class Meta:
        unique_together = ('mazo', 'usuario')

    def __str__(self):
        return f"Mazo: {self.mazo.nombre} - Puntuado por: {self.usuario.username} con {self.estrellas} estrellas"
    

class Publicacion_venta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(CategoriaPost, on_delete=models.CASCADE)
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

    def __str__(self):
        return self.descripcion + ' | ' + str(self.id_mazo)

class Comentario(models.Model):
    mazo = models.ForeignKey(Mazo, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = RichTextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.mazo.nombre, self.autor)

class Usuario_notas(models.Model):
    nota_promedio = models.FloatField()
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

class Publicacion_intercambio(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    contenido = RichTextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(CategoriaPost, on_delete=models.CASCADE)
    cartas_tengo = models.ManyToManyField('Carta', related_name='cartas_tengo', blank=True)
    cartas_quiero = models.ManyToManyField('Carta', related_name='cartas_quiero', blank=True)

    def __str__(self):
        return self.titulo + ' | ' + str(self.autor)
    
    def get_absolute_url(self):
        return reverse('detallePublicacion', args=(str(self.id)))

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

    def __str__(self):
        return 'Nombre: ' + self.nombre + '- Coste: ' + str(self.coste) + '- Tipo: ' + str(self.id_tipo) + '- raza: ' + str(self.id_raza)


class Cartas_publicacion_intercambio(models.Model):
    id_publicacion_intercambio = models.ForeignKey(Publicacion_intercambio, on_delete = models.CASCADE)
    id_carta = models.ForeignKey(Carta, on_delete = models.CASCADE)

class Cartas_mazos(models.Model):
    id_carta = models.ForeignKey(Carta, on_delete = models.CASCADE, related_name='rel_cartas')
    id_mazo = models.ForeignKey(Mazo, on_delete = models.CASCADE, related_name= 'rel_mazos')
    cantidad = models.IntegerField(default=1)

class Cartas_Banlist(models.Model):
    carta = models.ForeignKey(Carta, on_delete = models.CASCADE)
    edicion = models.ForeignKey(Edicion, on_delete= models.CASCADE)
    restriccion = models.ForeignKey(Restriccion, on_delete=models.CASCADE)


class RespuestaComentario(models.Model):
    comentario = models.ForeignKey(Comentario, related_name="respuestas", on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = RichTextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return '%s - %s' % (self.comentario.autor, self.autor)

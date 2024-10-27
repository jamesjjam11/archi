from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

User = get_user_model()

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    ci = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Persona'

class Secretaria(models.Model):
    nombre_secretaria = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre_secretaria

class Unidad(models.Model):
    nombre_secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, null=True, blank=True)
    nombre_unidad = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_unidad

class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre_cargo

class UsuarioCargoUnidad(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, null=True, blank=True)
    nombre_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.nombre_cargo.nombre_cargo} en {self.nombre_unidad.nombre_unidad}'
class Bitacora(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
        
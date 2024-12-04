from django.db import models
from django.contrib.auth.models import User
from userArchivoapp.models import Documento, Prestamo

class SolicitudPrestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    motivo_solicitud = models.TextField()
    fecha_solicitud = models.DateField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)  # Este campo es clave para filtrar las solicitudes pendientes
    generado_word = models.BooleanField(default=False)
    prestamo = models.OneToOneField(Prestamo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Solicitud de {self.usuario} para {self.documento}'

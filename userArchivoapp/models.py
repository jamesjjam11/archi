from django.db import models
from django.contrib.auth import get_user_model
from webapp.models import Secretaria, Unidad, UsuarioCargoUnidad
import mimetypes

User = get_user_model()

class Documento(models.Model):
    ESTADO_CHOICES = [
        ('optimo', 'Óptimo'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('algo_dañado', 'Algo Dañado'),
        ('malo', 'Malo'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    fecha_documento = models.DateField(null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    numero_hojas = models.IntegerField(max_length=4)
    tipo_documentacion = models.CharField(max_length=100)
    ambiente = models.CharField(max_length=100)
    estante = models.CharField(max_length=100)
    columna = models.CharField(max_length=100)
    balda = models.CharField(max_length=100)
    detalles = models.TextField(blank=True, null=True)
    responsable = models.CharField(blank=True, null=True)
    tipo = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    gestion = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.nombre_archivo} - {self.usuario.username}"

    def save(self, *args, **kwargs):
        if self.usuario:
            usuario_cargo_unidad = UsuarioCargoUnidad.objects.filter(user=self.usuario).first()
            if usuario_cargo_unidad:
                self.secretaria = usuario_cargo_unidad.nombre_unidad.nombre_secretaria
                self.unidad = usuario_cargo_unidad.nombre_unidad
        super(Documento, self).save(*args, **kwargs)
    def es_imagen(self):
        tipo_mime, _ = mimetypes.guess_type(self.archivo.url)
        return tipo_mime and tipo_mime.startswith('image')

    def es_pdf(self):
        tipo_mime, _ = mimetypes.guess_type(self.archivo.url)
        return tipo_mime == 'application/pdf'

    def es_word(self):
        tipo_mime, _ = mimettypes.guess_type(self.archivo.url)
        return tipo_mime in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']

    def es_excel(self):
        tipo_mime, _ = mimetypes.guess_type(self.archivo.url)
        return tipo_mime in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

class Prestamo(models.Model):
    DOCUMENTO_TIPO = [
        ('fisico', 'Físico'),
        ('digital', 'Digital'),
    ]
    
    ESTADO_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    usuario_prestamo = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=10, choices=DOCUMENTO_TIPO, default='fisico')
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    estado_prestamo = models.BooleanField(default=False)  # False = No devuelto, True = Devuelto
    estado_solicitud = models.CharField(max_length=10, choices=ESTADO_SOLICITUD, default='pendiente')
    archivo_solicitud = models.FileField(upload_to='solicitudes/', null=True, blank=True)

    def __str__(self):
        return f'{self.documento} prestado a {self.usuario_prestamo}'    

class Gestion(models.Model):
    año = models.CharField(max_length=4, unique=True)
    abierta = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.año} - {'Abierta' if self.abierta else 'Cerrada'}"

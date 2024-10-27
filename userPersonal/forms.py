from django import forms
from .models import SolicitudPrestamo
from webapp.models import Persona
from django.utils.timezone import now
from webapp.models import UsuarioCargoUnidad
from userArchivoapp.models import Prestamo

class SolicitudPrestamoForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    apellido = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cargo = forms.CharField(label='Cargo', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    secretaria = forms.CharField(label='Secretaría', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    unidad = forms.CharField(label='Unidad', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_solicitud = forms.DateField(label='Fecha de Solicitud', initial=now, widget=forms.DateInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SolicitudPrestamo
        fields = ['documento', 'motivo_solicitud']

    def __init__(self, *args, **kwargs):
        # Captura el usuario que realiza la solicitud
        user = kwargs.pop('user')
        super(SolicitudPrestamoForm, self).__init__(*args, **kwargs)
        
        # Obtén los datos del solicitante desde el modelo Persona
        persona = Persona.objects.get(user=user)
        usuario_cargo_unidad = UsuarioCargoUnidad.objects.get(user=user)
        
        self.fields['nombre'].initial = persona.nombre
        self.fields['apellido'].initial = persona.apellido_paterno
        self.fields['cargo'].initial = usuario_cargo_unidad.nombre_cargo.nombre_cargo
        self.fields['secretaria'].initial = usuario_cargo_unidad.nombre_unidad.nombre_secretaria.nombre_secretaria
        self.fields['unidad'].initial = usuario_cargo_unidad.nombre_unidad.nombre_unidad

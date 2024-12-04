from django import forms
from .models import Documento, Prestamo, Gestion
from webapp.models import Secretaria, Unidad
from userPersonal.models import SolicitudPrestamo

class DocumentoForm(forms.ModelForm):
    
    class Meta:
        model = Documento
        fields = [
            'nombre_archivo', 'archivo', 'estado', 'numero_hojas',
            'tipo_documentacion', 'ambiente', 'estante', 'columna', 
            'balda', 'detalles', 'responsable', 'secretaria', 'unidad',
            'tipo', 'numero', 'gestion', 'fecha_documento',
        ]
        def clean_gestion(self):
            gestion = self.cleaned_data['gestion']
            try:
                gestion_activa = Gestion.objects.get(año=gestion, abierta=True)
            except Gestion.DoesNotExist:
                raise forms.ValidationError("No es posible registrar documentos para la gestión seleccionada.")
            return gestion
        widgets = {
            'estado': forms.Select(choices=[
                ('optimo', 'OPTIMO'),
                ('bueno', 'BUENO'),
                ('regular', 'REGULAR'),
                ('algo_desgastado', 'ALGO DESGASTADO'),
                ('malo', 'MALO'),
            ]),
            'fecha_documento': forms.DateInput(attrs={'type': 'date'}),
        }
        secretaria = forms.ModelChoiceField(queryset=Secretaria.objects.all(), empty_label="Seleccione una secretaria", required=True)
        unidad = forms.ModelChoiceField(queryset=Unidad.objects.all(), empty_label="Seleccione una unidad", required=True)

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['documento', 'tipo_documento', 'archivo_solicitud']

class GestionSolicitudForm(forms.ModelForm):
    # Nuevo campo para rechazar la solicitud, de tipo booleano.
    rechazado = forms.BooleanField(required=False, label="Rechazar solicitud")

    class Meta:
        model = SolicitudPrestamo
        fields = ['aprobado', 'rechazado']

    def clean(self):
        cleaned_data = super().clean()
        aprobado = cleaned_data.get("aprobado")
        rechazado = cleaned_data.get("rechazado")

        # Verificar que solo se seleccione una opción entre aprobar y rechazar
        if aprobado and rechazado:
            raise forms.ValidationError("Solo puedes aprobar o rechazar la solicitud, no ambas opciones.")
        
        return cleaned_data

    def save(self, commit=True):
        solicitud = super().save(commit=False)
        
        # Si la solicitud está aprobada, creamos un Prestamo asociado
        if solicitud.aprobado and not solicitud.prestamo:
            prestamo = Prestamo.objects.create(
                documento=solicitud.documento,
                usuario_prestamo=solicitud.usuario,
                tipo_documento='fisico',  # Puedes tomar el tipo de documento si es necesario
                estado_solicitud='aprobado'
            )
            solicitud.prestamo = prestamo
        
        # Si la solicitud está rechazada, actualizamos su estado a 'rechazado'
        if self.cleaned_data.get('rechazado'):
            if solicitud.prestamo:  # Si ya existe un préstamo asociado
                solicitud.prestamo.estado_solicitud = 'rechazado'
                solicitud.prestamo.save()
            solicitud.aprobado = False  # Cambiar el estado de la solicitud a no aprobada
            solicitud.prestamo = None  # Eliminar el préstamo asociado

        if commit:
            solicitud.save()
        return solicitud

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['fecha_devolucion', 'estado_prestamo']
        labels = {
            'fecha_devolucion': 'Fecha de Devolución',
            'estado_prestamo': 'Documento Devuelto',
        }
        widgets = {
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'estado_prestamo': forms.CheckboxInput(),
        }

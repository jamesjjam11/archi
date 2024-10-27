from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from .forms import SolicitudPrestamoForm
from .models import SolicitudPrestamo
from io import BytesIO
from docx import Document
@never_cache
@login_required
def solicitar_prestamo_view(request):
    if request.method == 'POST':  
        form = SolicitudPrestamoForm(request.POST, user=request.user)
        if form.is_valid():
            # Guarda la solicitud en la base de datos
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()
            
            # Genera el documento Word
            buffer = BytesIO()
            doc = Document()

            # Añadir título
            doc.add_heading('Solicitud de Préstamo de Documentos', 0)

            # Añadir campos del formulario al documento
            doc.add_paragraph(f"Nombre: {request.user.first_name}")
            doc.add_paragraph(f"Apellido: {request.user.last_name}")
            doc.add_paragraph(f"Cargo: {form.cleaned_data['cargo']}")
            doc.add_paragraph(f"Secretaría: {form.cleaned_data['secretaria']}")
            doc.add_paragraph(f"Unidad: {form.cleaned_data['unidad']}")
            doc.add_paragraph(f"Fecha de Solicitud: {solicitud.fecha_solicitud}")
            doc.add_paragraph(f"Motivo del Préstamo: {form.cleaned_data['motivo_solicitud']}")
            doc.add_paragraph(f"Documento Solicitado: {solicitud.documento}")

            # Guardar el documento en el buffer
            doc.save(buffer)
            buffer.seek(0)

            # Enviar el archivo como respuesta HTTP
            response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="Solicitud_Prestamo.docx"'
            return response
    else:
        form = SolicitudPrestamoForm(user=request.user)
    
    return render(request, 'solicitud_prestamo.html', {'form': form})

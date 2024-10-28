from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from .forms import DocumentoForm, GestionSolicitudForm, DevolucionForm
from django.contrib import messages
from webapp.models import Secretaria, Unidad, UsuarioCargoUnidad
from userPersonal.models import SolicitudPrestamo
from PIL import Image
from django.http import JsonResponse, HttpResponse, FileResponse
import os, io
from .models import Documento, Prestamo
from PyPDF2 import PdfReader, PdfWriter
import zipfile
from docx import Document
from docx import Document as DocxDocument
import openpyxl
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from collections import defaultdict
from itertools import groupby
from operator import attrgetter
from django.utils import timezone
from datetime import timedelta



def comprimir_archivo(archivo):
    if archivo.name.endswith(('.jpg', '.jpeg', '.png')):
        # Comprimir imágenes
        img = Image.open(archivo)
        output = BytesIO()
        img.save(output, format='JPEG', quality=70)  # Reducir calidad para comprimir
        output.seek(0)
        return InMemoryUploadedFile(output, 'ImageField', f"{archivo.name.split('.')[0]}.jpg", 'image/jpeg', len(output.getvalue()), None)
    
    elif archivo.name.endswith('.pdf'):
        # Comprimir PDFs
        pdf_reader = PdfReader(archivo)
        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return InMemoryUploadedFile(output, 'FileField', archivo.name, 'application/pdf', len(output.getvalue()), None)

    elif archivo.name.endswith('.docx'):
        # Comprimir documentos Word
        doc = DocxDocument(archivo)
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        return InMemoryUploadedFile(output, 'FileField', archivo.name, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', len(output.getvalue()), None)

    elif archivo.name.endswith(('.xls', '.xlsx')):
        # Comprimir documentos Excel
        output = io.BytesIO()
        if archivo.name.endswith('.xlsx'):
            wb = openpyxl.load_workbook(archivo)
            wb.save(output)
        else:
            # Manejar archivos .xls si es necesario
            pass
        output.seek(0)
        return InMemoryUploadedFile(output, 'FileField', archivo.name, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', len(output.getvalue()), None)

    return archivo

@login_required
def subir_documento(request):
    form = DocumentoForm()
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.usuario = request.user  # Asignar el usuario que subió el documento
            
            # Convertir todos los campos relevantes a mayúsculas
            documento.nombre_archivo = form.cleaned_data['nombre_archivo'].upper()
            documento.detalles = form.cleaned_data['detalles'].upper()
            documento.estado = form.cleaned_data['estado'].upper()
            documento.numero_hojas = form.cleaned_data['numero_hojas']  # Suponiendo que este es un número
            documento.tipo_documentacion = form.cleaned_data['tipo_documentacion'].upper()
            documento.ambiente = form.cleaned_data['ambiente'].upper()
            documento.estante = form.cleaned_data['estante'].upper()
            documento.columna = form.cleaned_data['columna'].upper()
            documento.balda = form.cleaned_data['balda'].upper()
            documento.tipo = form.cleaned_data['tipo'].upper()
            documento.numero = form.cleaned_data['numero']  # Suponiendo que este es un número
            documento.gestion = form.cleaned_data['gestion'].upper()
            documento.responsable = form.cleaned_data['responsable'].upper()
            
            archivo = request.FILES.get('archivo')
            if archivo:
                print("Archivo recibido:", archivo.name)
                documento.archivo = comprimir_archivo(archivo)  # Suponiendo que tienes esta función
            else:
                print("No se recibió archivo.")
            documento.save()
            
            # Agregar un mensaje de éxito
            messages.success(request, 'El documento se subió con éxito.')
            return redirect('reporte_documento', documento.id)  # Redirige a la vista del reporte
            
    unidades = Unidad.objects.all().select_related('nombre_secretaria')
    
    context = {
        'form': form,
        'unidades': unidades,
        'nombre_archivo': form['nombre_archivo'],
        'archivo': form['archivo'],
        'estado': form['estado'],
        'numero_hojas': form['numero_hojas'],
        'tipo_documentacion': form['tipo_documentacion'],
        'ambiente': form['ambiente'],
        'estante': form['estante'],
        'columna': form['columna'],
        'balda': form['balda'],
        'detalles': form['detalles'],
        'tipo': form['tipo'],
        'numero': form['numero'],
        'gestion': form['gestion'],
        'responsable': form['responsable'],
    }
    
    return render(request, 'subir_documento.html', context)


def get_unidades(request, secretaria_id):
    unidades = Unidad.objects.filter(nombre_secretaria_id=secretaria_id)
    unidades_list = list(unidades.values('id', 'nombre_unidad'))
    return JsonResponse({'unidades': unidades_list})

@never_cache
@login_required
def lista_archivos(request):
    # Obtener los valores de los campos de búsqueda
    comprobante = request.GET.get('comprobante', '')
    gestion = request.GET.get('gestion', '')
    nombre = request.GET.get('nombre', '')

    # Filtrar documentos según los criterios proporcionados
    documentos = Documento.objects.all()

    if comprobante:
        documentos = documentos.filter(numero__icontains=comprobante)  # Filtrar por comprobante
    if gestion:
        documentos = documentos.filter(gestion__icontains=gestion)  # Filtrar por gestión
    if nombre:
        documentos = documentos.filter(nombre_archivo__icontains=nombre)  # Filtrar por nombre de archivo

    # Ordenar los documentos por 'detalles' y 'fecha_subida'
    documentos = documentos.order_by('detalles', 'fecha_subida')

    # Agrupar los documentos por 'detalles'
    documentos_agrupados = {
        detalle: list(documentos) for detalle, documentos in groupby(documentos, key=attrgetter('detalles'))
    }

    # Preparar el contexto
    context = {
        'documentos_agrupados': documentos_agrupados,
        'comprobante': comprobante,
        'gestion': gestion,
        'nombre': nombre,
    }

    return render(request, 'list_doc.html', context)

def vista_previa_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    
    context = {
        'documento': documento
    }
    
    return render(request, 'vista_previa.html', context)

@never_cache
@login_required
def gestionar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudPrestamo, id=solicitud_id)
    
    if request.method == 'POST':
        form = GestionSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('lista_solicitudes')  # Redirigir a una lista de solicitudes
    
    else:
        form = GestionSolicitudForm(instance=solicitud)
    
    return render(request, 'gestionar_solicitud.html', {'form': form, 'solicitud': solicitud})

@never_cache
@login_required
def lista_solicitudes(request): 
    # Filtrar solicitudes según el estado
    solicitudes_pendientes = Prestamo.objects.filter(estado_solicitud='pendiente')
    solicitudes_aprobadas = Prestamo.objects.filter(estado_solicitud='aprobado')
    solicitudes_rechazadas = Prestamo.objects.filter(estado_solicitud='rechazado') # Pasar las solicitudes al contexto
    context = {
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aprobadas': solicitudes_aprobadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
    }
    return render(request, 'lista_solicitudes.html', context)

@never_cache
@login_required
def lista_prestamos_pendientes(request):
    # Préstamos pendientes de devolución
    prestamos_pendientes = Prestamo.objects.filter(estado_prestamo=False, estado_solicitud='aprobado')
   
    # Préstamos ya devueltos
    prestamos_devueltos = Prestamo.objects.filter(estado_prestamo=True, estado_solicitud='aprobado')
   
    # Pasar ambas listas al template
    return render(request, 'lista_prestamos_pendientes.html', {
        'prestamos_pendientes': prestamos_pendientes,
        'prestamos_devueltos': prestamos_devueltos
    })


def registrar_devolucion_modal(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    if request.method == 'POST':
        form = DevolucionForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()  # Guarda la devolución
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render_to_string('partial_devolucion_form.html', {'form': form}, request)})
    
    else:
        form = DevolucionForm(instance=prestamo)
        html_form = render_to_string('partial_devolucion_form.html', {'form': form}, request)
        return JsonResponse({'html': html_form})
    
@never_cache
@login_required 
def buscar_documentos(request):
    comprobante = request.GET.get('comprobante', '')
    gestion = request.GET.get('gestion', '')
    nombre = request.GET.get('nombre', '')

    resultados = Documento.objects.all()

    # Filtrado de resultados
    if comprobante or gestion or nombre:
        if comprobante:
            resultados = resultados.filter(numero__icontains=comprobante)
        if gestion:
            resultados = resultados.filter(gestion__icontains=gestion)
        if nombre:
            resultados = resultados.filter(nombre_archivo__icontains=nombre)

    context = {
        'resultados': resultados,
        'comprobante': comprobante,
        'gestion': gestion,
        'nombre': nombre,
    }

    return render(request, 'buscar_documentos.html', context)


@login_required
def reporte_documento(request, documento_id):
    # Obtener el documento subido por su ID
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Pasar el documento al contexto
    context = {
        'documento': documento
    }
    
    # Renderizar la plantilla del reporte
    return render(request, 'reporte_documento.html', context)

@never_cache
@login_required
def lista_reportes(request):
    filtro = request.GET.get('filtro', 'dia')
    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)
    documentos = Documento.objects.all()

    if filtro == 'dia':
        documentos = documentos.filter(fecha_subida__date=timezone.now().date())
    elif filtro == 'semana':
        documentos = documentos.filter(fecha_subida__gte=timezone.now() - timedelta(weeks=1))
    elif filtro == 'mes':
        documentos = documentos.filter(fecha_subida__gte=timezone.now() - timedelta(days=30))
    elif filtro == 'rango' and fecha_inicio and fecha_fin:
        fecha_inicio = timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = timezone.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        documentos = documentos.filter(fecha_subida__date__range=(fecha_inicio, fecha_fin))

    documentos = documentos.order_by('-fecha_subida')
    return render(request, 'lista_reportes.html', {'documentos': documentos, 'filtro': filtro})

login_required
def descargar_reporte(request, documento_id):
    # Obtener el documento por ID
    documento = Documento.objects.get(id=documento_id)
   
    # Crear un nuevo documento de Word
    doc = Document()

    # Título del documento
    doc.add_heading('Reporte del Documento Subido', level=1)

    # Añadir contenido del documento
    doc.add_paragraph(f"Nombre del archivo: {documento.nombre_archivo}")
    doc.add_paragraph(f"Detalles: {documento.detalles}")
    doc.add_paragraph(f"Estado: {documento.estado}")
    doc.add_paragraph(f"Número de Hojas: {documento.numero_hojas}")
    doc.add_paragraph(f"Tipo de Documentación: {documento.tipo_documentacion}")
    
    # Ubicación
    doc.add_paragraph("Ubicación:")
    doc.add_paragraph(f"  Ambiente: {documento.ambiente}")
    doc.add_paragraph(f"  Estante: {documento.estante}")
    doc.add_paragraph(f"  Columna: {documento.columna}")
    doc.add_paragraph(f"  Balda: {documento.balda}")
    
    doc.add_paragraph(f"Tipo: {documento.tipo}")
    doc.add_paragraph(f"Número: {documento.numero}")
    doc.add_paragraph(f"Gestión: {documento.gestion}")
    doc.add_paragraph(f"Responsable: {documento.responsable}")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{documento.nombre_archivo}.docx"'

    # Guardar el documento en la respuesta
    doc.save(response)

    return response

def descargar_documento(request, documento_id):
    # Obtener el documento por su ID
    documento = get_object_or_404(Documento, id=documento_id)

    # Abrir el archivo en modo lectura binaria
    file_path = documento.archivo.path  # Supongo que tu modelo Documento tiene un campo llamado archivo
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)

    # Establecer el nombre del archivo para la descarga
    response['Content-Disposition'] = f'attachment; filename="{documento.nombre_archivo}"'

    return response
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_unidades

urlpatterns = [
    path('subir_documento/', views.subir_documento, name='subir_documento'),
    path('get_unidades/<int:secretaria_id>/', views.get_unidades, name='get_unidades'),
    path('lista-archivos/', views.lista_archivos, name='lista_archivos'),
    path('vista_previa_documento/<int:documento_id>/', views.vista_previa_documento, name='vista_previa_documento'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/<int:solicitud_id>/', views.gestionar_solicitud, name='gestionar_solicitud'),
    path('prestamos/pendientes/', views.lista_prestamos_pendientes, name='lista_prestamos_pendientes'),
    path('gestionar_solicitud/<int:solicitud_id>/', views.gestionar_solicitud, name='gestionar_solicitud'),
    path('prestamo/devolucion/modal/<int:prestamo_id>/', views.registrar_devolucion_modal, name='registrar_devolucion_modal'),
    path('buscar_documentos/', views.buscar_documentos, name='buscar_documentos'),
    path('reporte-documento/<int:documento_id>/', views.reporte_documento, name='reporte_documento'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('descargar-reporte/<int:documento_id>/', views.descargar_reporte, name='descargar_reporte'),
    path('descargar_documento/<int:documento_id>/', views.descargar_documento, name='descargar_documento'),
    path('gestionar-gestion/', views.gestionar_gestion, name='gestionar_gestion'),
    path('cerrar-gestion/<int:gestion_id>/', views.cerrar_gestion, name='cerrar_gestion'),
    path('solicitar-prestamo/', include('userPersonal.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

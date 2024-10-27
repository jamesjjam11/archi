# tasks.py
from celery import shared_task
from datetime import datetime, timedelta
from .models import Bitacora

@shared_task
def limpiar_bitacora():
    limite_fecha = datetime.now() - timedelta(days=90)
    Bitacora.objects.filter(timestamp__lt=limite_fecha).delete()

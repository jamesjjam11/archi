import os
from celery import Celery

# Establece el módulo de configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webArchi.settings')

# Crea una instancia de Celery
app = Celery('webArchi')

# Carga la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga las tareas de todos los módulos registrados
app.autodiscover_tasks()
